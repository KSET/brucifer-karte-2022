import os
import shutil
import smtplib
import socket
import tempfile
from datetime import date, datetime
from io import BytesIO
from unittest import mock
from zoneinfo import ZoneInfo

from django.contrib.auth.models import User as DjangoUser
from django.core.cache import cache
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import BrucosiFormResponse, Guests, Lineup, Mailer, Users
from .roles import Role
from .services import classify_mail_error, derive_fer_email

LIST_URL = '/api/forms/'
SUBMIT_URL = LIST_URL


def valid_payload(**overrides):
    payload = {
        'name': 'Ivan',
        'surname': 'Horvat',
        'jmbag': '0036123456',
        'gdpr_accepted': True,
    }
    payload.update(overrides)
    return payload


class BrucosiFormTests(APITestCase):
    def setUp(self):
        cache.clear()

    def login_as(self, role):
        email = f'{role}@kset.org'
        Users.objects.create(email=email, privilege=role)
        self.client.force_authenticate(DjangoUser.objects.create(username=email))

    def test_anonymous_submit_ignores_status(self):
        res = self.client.post(SUBMIT_URL, valid_payload(status='redeemed'), format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(BrucosiFormResponse.objects.get().status, 'invalid')

    def test_submit_strips_whitespace(self):
        res = self.client.post(SUBMIT_URL, valid_payload(name='  Ivan ', jmbag=' 0036123456 '), format='json')
        self.assertEqual(res.status_code, 201)
        row = BrucosiFormResponse.objects.get()
        self.assertEqual((row.name, row.jmbag), ('Ivan', '0036123456'))

    def test_invalid_submissions_rejected(self):
        for bad in (
            {'jmbag': '123'},
            {'jmbag': 'abcdefghij'},
            {'gdpr_accepted': False},
            {'name': '   '},
        ):
            with self.subTest(bad=bad):
                res = self.client.post(SUBMIT_URL, valid_payload(**bad), format='json')
                self.assertEqual(res.status_code, 400)
        self.assertEqual(BrucosiFormResponse.objects.count(), 0)

    def test_duplicate_jmbag_allowed(self):
        self.client.post(SUBMIT_URL, valid_payload(), format='json')
        self.client.post(SUBMIT_URL, valid_payload(name='Marko'), format='json')
        self.assertEqual(BrucosiFormResponse.objects.filter(jmbag='0036123456').count(), 2)

    def test_list_anonymous(self):
        self.assertEqual(self.client.get(LIST_URL).status_code, 401)

    def test_list_role_none(self):
        self.login_as(Role.NONE)
        self.assertEqual(self.client.get(LIST_URL).status_code, 403)

    def test_list_role_tickets(self):
        self.login_as(Role.TICKETS)
        self.assertEqual(self.client.get(LIST_URL).status_code, 200)

    def test_no_update_or_delete(self):
        self.client.post(SUBMIT_URL, valid_payload(), format='json')
        row = BrucosiFormResponse.objects.get()
        self.login_as(Role.ADMIN)
        url = f'{LIST_URL}{row.id}/'
        self.assertEqual(self.client.put(url, valid_payload(), format='json').status_code, 405)
        self.assertEqual(self.client.delete(url).status_code, 405)
        self.assertEqual(self.client.patch(url, {'status': 'redeemed'}, format='json').status_code, 405)

    @override_settings(REST_FRAMEWORK={
        'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication'],
        'NUM_PROXIES': 1,
    })
    def test_throttle_ignores_spoofed_forwarded_for(self):
        statuses = [
            self.client.post(
                SUBMIT_URL, valid_payload(), format='json',
                HTTP_X_FORWARDED_FOR=f'10.0.0.{i}, 1.2.3.4',
            ).status_code
            for i in range(101)
        ]
        self.assertEqual(statuses[-1], 429)


DB_TABLES_URL = '/api/db/tables/'


class DbBrowserTests(APITestCase):
    ROWS_URL = DB_TABLES_URL + 'bruc_users/'

    def login_as(self, role):
        email = f'{role}@kset.org'
        user = Users.objects.create(email=email, privilege=role)
        self.client.force_authenticate(DjangoUser.objects.create(username=email))
        return user

    def assert_denied(self, expected=(403,)):
        for url in (DB_TABLES_URL, self.ROWS_URL, DB_TABLES_URL + 'nope/'):
            with self.subTest(url=url):
                res = self.client.get(url)
                self.assertIn(res.status_code, expected)
                self.assertNotIn('rows', getattr(res, 'data', None) or {})

    def test_anonymous_denied(self):
        self.assert_denied(expected=(401, 403))

    def test_non_admin_roles_denied(self):
        for role in (Role.NONE, Role.TICKETS, Role.ENTRY, Role.ENTRY_TICKETS):
            with self.subTest(role=role):
                self.login_as(role)
                self.assert_denied()

    def test_authenticated_without_users_row_denied(self):
        self.client.force_authenticate(DjangoUser.objects.create(username='ghost@kset.org'))
        self.assert_denied()

    def test_django_superuser_without_admin_role_denied(self):
        email = 'super@kset.org'
        Users.objects.create(email=email, privilege=Role.TICKETS)
        self.client.force_authenticate(
            DjangoUser.objects.create(username=email, is_staff=True, is_superuser=True))
        self.assert_denied()

    def test_demoted_admin_loses_access_immediately(self):
        user = self.login_as(Role.ADMIN)
        self.assertEqual(self.client.get(self.ROWS_URL).status_code, 200)
        user.privilege = Role.TICKETS
        user.save()
        self.assert_denied()

    def test_real_jwt_non_admin_denied_admin_allowed(self):
        for role, expected in ((Role.TICKETS, 403), (Role.ADMIN, 200)):
            with self.subTest(role=role):
                email = f'jwt-{role}@kset.org'
                Users.objects.create(email=email, privilege=role)
                token = RefreshToken.for_user(DjangoUser.objects.create(username=email)).access_token
                self.client.force_authenticate(None)
                self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
                self.assertEqual(self.client.get(self.ROWS_URL).status_code, expected)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer not-a-token')
        self.assertEqual(self.client.get(self.ROWS_URL).status_code, 401)

    def test_read_only_for_admin(self):
        self.login_as(Role.ADMIN)
        for method in ('post', 'put', 'patch', 'delete'):
            with self.subTest(method=method):
                self.assertEqual(getattr(self.client, method)(self.ROWS_URL, {}).status_code, 405)

    def test_responses_not_cacheable(self):
        self.login_as(Role.ADMIN)
        for url in (DB_TABLES_URL, self.ROWS_URL):
            with self.subTest(url=url):
                cache_control = self.client.get(url)['Cache-Control']
                self.assertIn('no-store', cache_control)
                self.assertIn('private', cache_control)

    def test_admin_lists_tables(self):
        self.login_as(Role.ADMIN)
        res = self.client.get(DB_TABLES_URL)
        self.assertEqual(res.status_code, 200)
        tables = {t['table'] for t in res.data}
        self.assertIn('bruc_guests', tables)
        self.assertTrue(all(t.startswith('bruc_') for t in tables))

    def test_admin_reads_rows(self):
        self.login_as(Role.ADMIN)
        res = self.client.get(self.ROWS_URL)
        self.assertEqual(res.status_code, 200)
        self.assertIn('email', res.data['columns'])
        self.assertEqual(res.data['pk'], 'id')
        self.assertEqual(res.data['total'], 1)
        self.assertEqual(res.data['rows'][0]['email'], 'admin@kset.org')
        self.assertFalse(res.data['truncated'])

    def test_unknown_or_non_bruc_table_404(self):
        self.login_as(Role.ADMIN)
        for table in ('nope', 'auth_user', 'django_session'):
            with self.subTest(table=table):
                self.assertEqual(self.client.get(DB_TABLES_URL + table + '/').status_code, 404)


def make_jpeg(size=(4000, 3000), name='photo.jpg', orientation=None):
    img = Image.new('RGB', size, (200, 50, 50))
    buf = BytesIO()
    if orientation:
        exif = img.getexif()
        exif[0x0112] = orientation
        img.save(buf, format='JPEG', exif=exif)
    else:
        img.save(buf, format='JPEG')
    return SimpleUploadedFile(name, buf.getvalue(), content_type='image/jpeg')


class LineupImageTests(TestCase):
    def setUp(self):
        self.media = tempfile.mkdtemp()
        self.override = override_settings(MEDIA_ROOT=self.media)
        self.override.enable()

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.media, ignore_errors=True)

    def test_upload_converted_to_resized_webp(self):
        item = Lineup.objects.create(name='Band', image=make_jpeg())
        self.assertTrue(item.image.name.endswith('.webp'))
        with Image.open(item.image.path) as img:
            self.assertEqual(img.format, 'WEBP')
            self.assertEqual(img.size, (2000, 1500))

    def test_exif_orientation_applied(self):
        item = Lineup.objects.create(name='Band', image=make_jpeg(orientation=6))
        with Image.open(item.image.path) as img:
            self.assertLess(img.width, img.height)

    def test_editing_other_fields_does_not_reencode(self):
        item = Lineup.objects.create(name='Band', image=make_jpeg())
        name, mtime = item.image.name, os.path.getmtime(item.image.path)
        item = Lineup.objects.get(pk=item.pk)
        item.visible = True
        item.save()
        self.assertEqual(item.image.name, name)
        self.assertEqual(os.path.getmtime(item.image.path), mtime)

    def test_replacing_image_deletes_old_file(self):
        item = Lineup.objects.create(name='Band', image=make_jpeg(name='a.jpg'))
        old_path = item.image.path
        item.image = make_jpeg(name='b.jpg')
        item.save()
        self.assertFalse(os.path.exists(old_path))
        self.assertTrue(os.path.exists(item.image.path))

    def test_delete_without_image(self):
        item = Lineup.objects.create(name='Band')
        item.delete()
        self.assertFalse(Lineup.objects.filter(pk=item.pk).exists())


class DeriveFerEmailTests(TestCase):
    def test_fer_jmbag(self):
        self.assertEqual(derive_fer_email('Ivan', 'Horvat', '0036123456'), 'ih12345@fer.hr')

    def test_transfer_jmbag(self):
        self.assertEqual(derive_fer_email('Ivan', 'Horvat', '0246012345'), 'ih024601234@fer.hr')

    def test_diacritics_and_whitespace(self):
        self.assertEqual(derive_fer_email(' Čedo ', 'Šimić', ' 0036123456 '), 'cs12345@fer.hr')

    def test_blank_parts(self):
        for args in (('', 'Horvat', '0036123456'), ('Ivan', ' ', '0036123456'), ('Ivan', 'Horvat', '')):
            with self.subTest(args=args):
                self.assertIsNone(derive_fer_email(*args))


class ClassifyMailErrorTests(TestCase):
    def test_categories(self):
        cases = (
            (smtplib.SMTPRecipientsRefused({'a@fer.hr': (550, b'user unknown')}), 'adresa odbijena'),
            (smtplib.SMTPRecipientsRefused({'a@fer.hr': (450, b'try later')}), 'Brevo privremeno odbija slanje, pokušaj ponovno'),
            (smtplib.SMTPAuthenticationError(535, b'auth failed'), 'greška u autentikaciji mail servera'),
            (ConnectionRefusedError(), 'mail server nedostupan'),
            (socket.timeout(), 'mail server nedostupan'),
            (smtplib.SMTPServerDisconnected(), 'mail server nedostupan'),
            (smtplib.SMTPSenderRefused(421, b'too many messages', 'noreply@kset.org'), 'Brevo privremeno odbija slanje, pokušaj ponovno'),
            (smtplib.SMTPDataError(554, b'account suspended'), 'Brevo odbio poruku'),
            (ValueError('boom'), 'nepoznata greška'),
        )
        for exc, expected in cases:
            with self.subTest(exc=repr(exc)):
                self.assertEqual(classify_mail_error(exc), expected)

def guests_url(guest, action):
    return f'/api/guests/{guest.id}/{action}/'


@override_settings(BREVO_WEBHOOK_TOKEN='secret-token')
class GuestSaleTests(APITestCase):
    def setUp(self):
        self.guest = Guests.objects.create(jmbag='0036123456', tag='Brucoši')
        BrucosiFormResponse.objects.create(name='Ivan', surname='Horvat', jmbag='0036123456', gdpr_accepted=True)

    def login_as(self, role):
        email = f'{role}@kset.org'
        Users.objects.get_or_create(email=email, defaults={'privilege': role})
        self.client.force_authenticate(DjangoUser.objects.get_or_create(username=email)[0])

    def sell(self, **body):
        return self.client.post(guests_url(self.guest, 'sell'), body, format='json')

    def test_tickets_user_can_sell(self):
        self.login_as(Role.TICKETS)
        res = self.sell()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data['mail_sent'])
        self.assertEqual(res.data['email'], 'ih12345@fer.hr')
        self.guest.refresh_from_db()
        self.assertTrue(self.guest.bought)
        self.assertEqual((self.guest.name, self.guest.surname), ('Ivan', 'Horvat'))
        self.assertEqual(len(self.guest.confCode), 36)
        self.assertIsNotNone(self.guest.boughtTicketTime)
        self.assertEqual(self.guest.mailStatus, 'sent')
        self.assertTrue(self.guest.mailMessageId)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['ih12345@fer.hr'])
        self.assertEqual(Mailer.objects.count(), 1)

    def test_second_sell_conflicts(self):
        self.login_as(Role.ENTRY_TICKETS)
        self.assertEqual(self.sell().status_code, 200)
        code = Guests.objects.get(pk=self.guest.pk).confCode
        self.assertEqual(self.sell().status_code, 409)
        self.assertEqual(Guests.objects.get(pk=self.guest.pk).confCode, code)
        self.assertEqual(len(mail.outbox), 1)

    def test_permissions(self):
        cases = (
            (Role.NONE, 'sell', 403),
            (Role.ENTRY, 'sell', 403),
            (Role.TICKETS, 'unsell', 403),
            (Role.TICKETS, 'resend-mail', 403),
            (Role.ENTRY_TICKETS, 'unsell', 403),
        )
        for role, action, expected in cases:
            with self.subTest(role=role, action=action):
                self.login_as(role)
                res = self.client.post(guests_url(self.guest, action), {}, format='json')
                self.assertEqual(res.status_code, expected)
        self.login_as(Role.TICKETS)
        self.assertEqual(self.client.get('/api/guests/failed-mails/').status_code, 403)

    def test_non_admin_cannot_fill_blank_name(self):
        BrucosiFormResponse.objects.all().delete()
        self.login_as(Role.TICKETS)
        res = self.sell(name='Netko', surname='Drugi')
        self.assertEqual(res.status_code, 400)
        self.assertFalse(Guests.objects.get(pk=self.guest.pk).bought)

    def test_non_admin_can_fix_prefilled_name(self):
        self.login_as(Role.TICKETS)
        res = self.sell(name='Ivo')
        self.assertEqual(res.status_code, 200)
        self.guest.refresh_from_db()
        self.assertEqual((self.guest.name, self.guest.surname), ('Ivo', 'Horvat'))

    def test_non_admin_picks_between_duplicate_submissions(self):
        BrucosiFormResponse.objects.create(name='Marko', surname='Horvat', jmbag='0036123456', gdpr_accepted=True)
        self.login_as(Role.TICKETS)
        self.assertEqual(self.sell(surname='Horvat').status_code, 400)
        self.assertEqual(self.sell(name='Marko').status_code, 200)
        self.assertEqual(Guests.objects.get(pk=self.guest.pk).name, 'Marko')

    def test_admin_can_fill_blank_name(self):
        BrucosiFormResponse.objects.all().delete()
        self.login_as(Role.ADMIN)
        self.assertEqual(self.sell(name='Ana', surname='Anić').status_code, 200)
        self.assertEqual(mail.outbox[0].to, ['aa12345@fer.hr'])

    def test_only_brucosi_can_be_sold(self):
        self.guest.tag = 'kset VIP'
        self.guest.save()
        self.login_as(Role.TICKETS)
        self.assertEqual(self.sell().status_code, 400)

    def test_form_status_redeemed_and_reset(self):
        BrucosiFormResponse.objects.create(name='Ivan', surname='Horvat', jmbag='0036123456', gdpr_accepted=True)
        self.login_as(Role.TICKETS)
        self.sell()
        self.assertEqual(set(BrucosiFormResponse.objects.values_list('status', flat=True)), {'redeemed'})
        self.login_as(Role.ADMIN)
        res = self.client.post(guests_url(self.guest, 'unsell'), {}, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(set(BrucosiFormResponse.objects.values_list('status', flat=True)), {'invalid'})
        self.guest.refresh_from_db()
        self.assertEqual((self.guest.bought, self.guest.confCode, self.guest.boughtTicketTime), (False, '', None))

    def test_unsell_after_entry_conflicts(self):
        self.login_as(Role.TICKETS)
        self.sell()
        Guests.objects.filter(pk=self.guest.pk).update(entered=True)
        self.login_as(Role.ADMIN)
        self.assertEqual(self.client.post(guests_url(self.guest, 'unsell'), {}, format='json').status_code, 409)
        self.assertTrue(Guests.objects.get(pk=self.guest.pk).bought)

    def test_mail_failure_keeps_sale(self):
        self.login_as(Role.TICKETS)
        refused = smtplib.SMTPRecipientsRefused({'ih12345@fer.hr': (550, b'no such user')})
        with mock.patch('bruc.services.EmailMultiAlternatives.send', side_effect=refused), \
                self.assertLogs('bruc.services', 'ERROR'):
            res = self.sell()
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.data['mail_sent'])
        self.assertEqual(res.data['mail_error'], 'adresa odbijena')
        self.guest.refresh_from_db()
        self.assertTrue(self.guest.bought)
        self.assertEqual((self.guest.mailStatus, self.guest.mailError), ('failed', 'adresa odbijena'))
        self.assertEqual(Mailer.objects.count(), 0)

    def test_mail_server_down(self):
        self.login_as(Role.TICKETS)
        with mock.patch('bruc.services.EmailMultiAlternatives.send', side_effect=ConnectionRefusedError()), \
                self.assertLogs('bruc.services', 'ERROR'):
            res = self.sell()
        self.assertEqual(res.data['mail_error'], 'mail server nedostupan')

    def test_brevo_rate_limit(self):
        self.login_as(Role.TICKETS)
        limited = smtplib.SMTPDataError(421, b'4.7.0 Too many messages')
        with mock.patch('bruc.services.EmailMultiAlternatives.send', side_effect=limited), \
                self.assertLogs('bruc.services', 'ERROR'):
            res = self.sell()
        self.assertFalse(res.data['mail_sent'])
        self.assertEqual(res.data['mail_error'], 'Brevo privremeno odbija slanje, pokušaj ponovno')
        self.assertTrue(Guests.objects.get(pk=self.guest.pk).bought)

    def test_admin_resend_and_failed_list(self):
        self.login_as(Role.TICKETS)
        with mock.patch('bruc.services.EmailMultiAlternatives.send', side_effect=smtplib.SMTPServerDisconnected()), \
                self.assertLogs('bruc.services', 'ERROR'):
            self.sell()
        self.login_as(Role.ADMIN)
        res = self.client.get('/api/guests/failed-mails/')
        self.assertEqual([g['id'] for g in res.data], [self.guest.id])

        res = self.client.post(guests_url(self.guest, 'resend-mail'), {'name': 'Ivo'}, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data['mail_sent'])
        self.assertEqual(res.data['email'], 'ih12345@fer.hr')
        self.assertEqual(Guests.objects.get(pk=self.guest.pk).name, 'Ivo')
        self.assertEqual(self.client.get('/api/guests/failed-mails/').data, [])

    def test_resend_unsold_rejected(self):
        self.login_as(Role.ADMIN)
        self.assertEqual(self.client.post(guests_url(self.guest, 'resend-mail'), {}, format='json').status_code, 400)

    def test_webhook_wrong_token(self):
        res = self.client.post('/api/brevo/webhook/wrong/', {'event': 'hard_bounce'}, format='json')
        self.assertEqual(res.status_code, 404)

    @override_settings(BREVO_WEBHOOK_TOKEN='')
    def test_webhook_disabled_without_token(self):
        self.assertEqual(self.client.post('/api/brevo/webhook/x/', {}, format='json').status_code, 404)

    def test_webhook_bounce_by_message_id(self):
        self.login_as(Role.TICKETS)
        self.sell()
        message_id = Guests.objects.get(pk=self.guest.pk).mailMessageId
        self.client.force_authenticate(None)
        res = self.client.post('/api/brevo/webhook/secret-token/', [
            {'event': 'delivered', 'message-id': message_id},
            {'event': 'hard_bounce', 'message-id': message_id, 'email': 'other@fer.hr'},
        ], format='json')
        self.assertEqual(res.status_code, 200)
        self.guest.refresh_from_db()
        self.assertEqual((self.guest.mailStatus, self.guest.mailError), ('bounced', 'mail se vratio (trajna greška)'))

    def test_webhook_bounce_by_email_fallback(self):
        self.login_as(Role.TICKETS)
        self.sell()
        self.client.force_authenticate(None)
        self.client.post('/api/brevo/webhook/secret-token/',
                         {'event': 'blocked', 'email': 'IH12345@fer.hr'}, format='json')
        self.assertEqual(Guests.objects.get(pk=self.guest.pk).mailStatus, 'bounced')

    def test_webhook_stale_message_id_ignored(self):
        self.login_as(Role.TICKETS)
        self.sell()
        self.client.force_authenticate(None)
        self.client.post('/api/brevo/webhook/secret-token/',
                         {'event': 'hard_bounce', 'email': 'ih12345@fer.hr', 'message-id': '<old@x>'}, format='json')
        self.assertEqual(Guests.objects.get(pk=self.guest.pk).mailStatus, 'sent')

    def test_webhook_soft_bounce_cleared_by_delivered(self):
        self.login_as(Role.TICKETS)
        self.sell()
        message_id = Guests.objects.get(pk=self.guest.pk).mailMessageId
        self.client.force_authenticate(None)
        url = '/api/brevo/webhook/secret-token/'
        self.client.post(url, {'event': 'soft_bounce', 'message-id': message_id}, format='json')
        self.assertEqual(Guests.objects.get(pk=self.guest.pk).mailStatus, 'bounced')
        self.client.post(url, {'event': 'delivered', 'message-id': message_id}, format='json')
        self.guest.refresh_from_db()
        self.assertEqual((self.guest.mailStatus, self.guest.mailError), ('delivered', ''))

    def test_webhook_delivered(self):
        self.login_as(Role.TICKETS)
        self.sell()
        message_id = Guests.objects.get(pk=self.guest.pk).mailMessageId
        self.client.force_authenticate(None)
        self.client.post('/api/brevo/webhook/secret-token/',
                         {'event': 'delivered', 'message-id': message_id}, format='json')
        self.assertEqual(Guests.objects.get(pk=self.guest.pk).mailStatus, 'delivered')

    def test_webhook_delivered_keeps_hard_bounce(self):
        self.login_as(Role.TICKETS)
        self.sell()
        message_id = Guests.objects.get(pk=self.guest.pk).mailMessageId
        self.client.force_authenticate(None)
        self.client.post('/api/brevo/webhook/secret-token/', [
            {'event': 'hard_bounce', 'message-id': message_id},
            {'event': 'delivered', 'message-id': message_id},
        ], format='json')
        self.assertEqual(Guests.objects.get(pk=self.guest.pk).mailStatus, 'bounced')

    def test_bulk_mailer_uses_helper(self):
        self.login_as(Role.TICKETS)
        self.sell()
        guest = Guests.objects.get(pk=self.guest.pk)
        self.login_as(Role.ADMIN)
        res = self.client.post('/api/mailer/send_mail/', {'emails': [{
            'subject': 's', 'message': 'm', 'template': 'guest_email',
            'name': guest.name, 'confCode': guest.confCode, 'to_mail': 'ignored@x.hr',
        }]}, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(mail.outbox[-1].to, ['ih12345@fer.hr'])
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(Mailer.objects.count(), 2)  # one log row per send

    def test_bulk_mailer_unknown_conf_code_fails(self):
        self.login_as(Role.ADMIN)
        res = self.client.post('/api/mailer/send_mail/', {'emails': [{
            'subject': 's', 'message': 'm', 'template': 'guest_email',
            'name': 'X', 'confCode': 'not-a-real-code', 'to_mail': 'x@x.hr',
        }]}, format='json')
        self.assertEqual(res.status_code, 500)
        self.assertEqual(len(mail.outbox), 0)

    def test_ticket_mail_has_inline_qr(self):
        self.login_as(Role.TICKETS)
        self.sell()
        msg = mail.outbox[-1]
        html = msg.alternatives[0][0]
        self.assertIn('src="cid:ticket-qr@brucifer"', html)
        self.assertNotIn('qrserver', html)
        mime = msg.message()
        self.assertEqual(mime.get_content_subtype(), 'related')
        images = [part for part in mime.walk() if part.get_content_type() == 'image/png']
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0]['Content-ID'], '<ticket-qr@brucifer>')
        self.assertTrue(images[0].get_payload(decode=True).startswith(b'\x89PNG'))

    def search(self, jmbag):
        return self.client.get('/api/guests/search-brucosi/', {'jmbag': jmbag})

    def test_search_single_match_returns_guest_and_submissions(self):
        self.login_as(Role.TICKETS)
        BrucosiFormResponse.objects.create(name='Ana', surname='Anić', jmbag='0036999999', gdpr_accepted=True)
        res = self.search('0036123')
        self.assertEqual(res.data['count'], 1)
        self.assertEqual([g['id'] for g in res.data['guests']], [self.guest.pk])
        self.assertEqual([s['name'] for s in res.data['submissions']], ['Ivan'])

    def test_search_is_prefix_only(self):
        self.login_as(Role.TICKETS)
        self.assertEqual(self.search('123456').data['count'], 0)

    def test_search_multiple_matches_returns_count_only(self):
        self.login_as(Role.TICKETS)
        Guests.objects.create(jmbag='0036123999', tag='Brucoši')
        Guests.objects.create(jmbag='0036123888', tag='kset VIP')
        res = self.search('0036123')
        self.assertEqual((res.data['count'], res.data['guests'], res.data['submissions']), (2, [], []))

    def test_today_stats_zagreb_day_and_tag(self):
        zg = ZoneInfo('Europe/Zagreb')
        Guests.objects.create(tag='Brucoši', bought=True, boughtTicketTime=datetime(2026, 10, 1, 9, 0, tzinfo=zg))
        Guests.objects.create(tag='Brucoši', bought=True, boughtTicketTime=datetime(2026, 10, 1, 23, 30, tzinfo=zg))
        Guests.objects.create(tag='Brucoši', bought=True, boughtTicketTime=datetime(2026, 10, 2, 0, 30, tzinfo=zg))
        Guests.objects.create(tag='kset VIP', bought=True, boughtTicketTime=datetime(2026, 10, 1, 10, 0, tzinfo=zg))
        Guests.objects.create(tag='Brucoši', bought=True, mailStatus='bounced')
        self.login_as(Role.TICKETS)
        with mock.patch('bruc.views.timezone.localdate', return_value=date(2026, 10, 1)):
            res = self.client.get('/api/guests/today-stats/')
        self.assertEqual(res.data['date'], '2026-10-01')
        self.assertEqual(
            (res.data['totalEntries'], res.data['ticketsBefore12'], res.data['ticketsAfter12'], res.data['failedMails']),
            (2, 1, 1, 1))
