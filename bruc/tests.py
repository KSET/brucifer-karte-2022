import os
import shutil
import smtplib
import socket
import tempfile
import unicodedata
from datetime import date, datetime, timedelta
from io import BytesIO
from unittest import mock
from zoneinfo import ZoneInfo

from django.conf import settings
from django.contrib.auth.models import User as DjangoUser
from django.core.cache import cache
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.db.models import F
from django.test import TestCase, override_settings
from django.utils import timezone
from PIL import Image
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import BrucosiFormResponse, Guests, Lineup, Mailer, Sponsors, Users, Visibility
from .roles import Role
from .search import fold, search_key
from .services import add_sponsor_guest, classify_mail_error, derive_fer_email
from .views import FormThrottle, RefreshThrottle, SponsorPortalTokenThrottle

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
        self.assertEqual(BrucosiFormResponse.objects.get().status, 'pending')

    def test_submit_strips_whitespace(self):
        res = self.client.post(SUBMIT_URL, valid_payload(name='  Ivan ', jmbag=' 0036123456 '), format='json')
        self.assertEqual(res.status_code, 201)
        row = BrucosiFormResponse.objects.get()
        self.assertEqual((row.name, row.jmbag), ('Ivan', '0036123456'))

    def test_invalid_submissions_rejected(self):
        for bad in (
            {'jmbag': '123'},
            {'jmbag': 'abcdefghij'},
            {'jmbag': '٠٠٣٦١٢٣٤٥٦'},
            {'gdpr_accepted': False},
            {'name': '   '},
            {'name': '1van'},
            {'name': '<b>'},
            {'surname': "'Horvat"},
            {'name': 'Émile', 'jmbag': '0036999999'},
        ):
            with self.subTest(bad=bad):
                res = self.client.post(SUBMIT_URL, valid_payload(**bad), format='json')
                self.assertEqual(res.status_code, 400)
        self.assertEqual(BrucosiFormResponse.objects.count(), 0)

    def test_names_with_diacritics_spaces_hyphens_allowed(self):
        res = self.client.post(SUBMIT_URL, valid_payload(name='Ana Marija', surname="Đurić-O'Neil"), format='json')
        self.assertEqual(res.status_code, 201)

    def test_duplicate_jmbag_allowed(self):
        self.client.post(SUBMIT_URL, valid_payload(), format='json')
        self.client.post(SUBMIT_URL, valid_payload(name='Marko'), format='json')
        self.assertEqual(BrucosiFormResponse.objects.filter(jmbag='0036123456').count(), 2)

    def test_no_read_update_or_delete(self):
        self.client.post(SUBMIT_URL, valid_payload(), format='json')
        row = BrucosiFormResponse.objects.get()
        self.login_as(Role.ADMIN)
        self.assertEqual(self.client.get(LIST_URL).status_code, 405)
        url = f'{LIST_URL}{row.id}/'
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.put(url, valid_payload(), format='json').status_code, 404)
        self.assertEqual(self.client.delete(url).status_code, 404)
        self.assertEqual(self.client.patch(url, {'status': 'redeemed'}, format='json').status_code, 404)

    def test_throttle_per_jmbag(self):
        statuses = [self.client.post(SUBMIT_URL, valid_payload(), format='json').status_code for _ in range(6)]
        self.assertEqual(statuses, [201] * 5 + [429])
        res = self.client.post(SUBMIT_URL, valid_payload(jmbag='0036654321'), format='json')
        self.assertEqual(res.status_code, 201)

    def test_jmbag_throttle_does_not_lock_out_other_ips(self):
        for _ in range(6):
            self.client.post(SUBMIT_URL, valid_payload(), format='json', REMOTE_ADDR='6.6.6.6')
        res = self.client.post(SUBMIT_URL, valid_payload(), format='json', REMOTE_ADDR='1.2.3.4')
        self.assertEqual(res.status_code, 201)

    def test_non_object_body_rejected(self):
        self.assertEqual(self.client.post(SUBMIT_URL, [], format='json').status_code, 400)

    @override_settings(REST_FRAMEWORK={
        'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication'],
        'NUM_PROXIES': 1,
    })
    @mock.patch.object(FormThrottle, 'rate', '3/hour')
    def test_throttle_ignores_spoofed_forwarded_for(self):
        statuses = [
            self.client.post(
                SUBMIT_URL, valid_payload(jmbag=f'003612345{i}'), format='json',
                HTTP_X_FORWARDED_FOR=f'10.0.0.{i}, 1.2.3.4',
            ).status_code
            for i in range(4)
        ]
        self.assertEqual(statuses, [201, 201, 201, 429])


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


class LineupScheduleTests(APITestCase):
    ZG = ZoneInfo('Europe/Zagreb')

    def setUp(self):
        Users.objects.create(email='admin@kset.org', privilege=Role.ADMIN)
        self.client.force_authenticate(DjangoUser.objects.create(username='admin@kset.org'))
        self.item = Lineup.objects.create(name='Band', visible=True)
        self.url = f'/api/lineup/{self.item.id}/'

    def test_admin_sets_times_and_public_exposes_them(self):
        start = datetime(2026, 11, 7, 23, 30, tzinfo=self.ZG)
        end = datetime(2026, 11, 8, 0, 45, tzinfo=self.ZG)
        res = self.client.patch(
            self.url, {'startTime': start.isoformat(), 'endTime': end.isoformat()}, format='json')
        self.assertEqual(res.status_code, 200, res.data)
        self.item.refresh_from_db()
        self.assertEqual(self.item.startTime, start)
        self.assertEqual(self.item.endTime, end)

        self.client.force_authenticate(None)
        res = self.client.get('/api/public/lineup/')
        self.assertEqual(res.status_code, 200)
        rows = res.data['results'] if isinstance(res.data, dict) else res.data
        row = next(r for r in rows if r['name'] == 'Band')
        self.assertEqual(datetime.fromisoformat(row['startTime']), start)
        self.assertEqual(datetime.fromisoformat(row['endTime']), end)

    def test_end_before_start_rejected(self):
        start = datetime(2026, 11, 7, 22, 0, tzinfo=self.ZG)
        res = self.client.patch(
            self.url,
            {'startTime': start.isoformat(), 'endTime': (start - timedelta(minutes=30)).isoformat()},
            format='json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('endTime', res.data)
        res = self.client.patch(
            self.url, {'startTime': start.isoformat(), 'endTime': start.isoformat()}, format='json')
        self.assertEqual(res.status_code, 400)

        # Only endTime sent: validated against the stored startTime.
        Lineup.objects.filter(pk=self.item.pk).update(startTime=start)
        res = self.client.patch(
            self.url, {'endTime': (start - timedelta(hours=1)).isoformat()}, format='json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('endTime', res.data)
        self.item.refresh_from_db()
        self.assertIsNone(self.item.endTime)

    def test_blank_multipart_clears_times(self):
        start = datetime(2026, 11, 7, 22, 0, tzinfo=self.ZG)
        Lineup.objects.filter(pk=self.item.pk).update(
            startTime=start, endTime=start + timedelta(hours=1))
        res = self.client.patch(self.url, {'startTime': '', 'endTime': ''}, format='multipart')
        self.assertEqual(res.status_code, 200, res.data)
        self.item.refresh_from_db()
        self.assertIsNone(self.item.startTime)
        self.assertIsNone(self.item.endTime)

    def test_stage_saved_and_validated(self):
        res = self.client.patch(self.url, {'stage': 'kino'}, format='json')
        self.assertEqual(res.status_code, 200, res.data)
        self.item.refresh_from_db()
        self.assertEqual(self.item.stage, 'kino')

        res = self.client.patch(self.url, {'stage': 'bina'}, format='json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('stage', res.data)

        res = self.client.patch(self.url, {'stage': ''}, format='json')
        self.assertEqual(res.status_code, 200, res.data)
        self.item.refresh_from_db()
        self.assertEqual(self.item.stage, '')


class DeriveFerEmailTests(TestCase):
    def test_fer_jmbag(self):
        self.assertEqual(derive_fer_email('Ivan', 'Horvat', '0036123456'), 'ih12345@fer.hr')

    def test_transfer_jmbag(self):
        self.assertEqual(derive_fer_email('Ivan', 'Horvat', '0246012345'), 'ih024601234@fer.hr')
        self.assertEqual(derive_fer_email('Ivan', 'Horvat', '0035123456'), 'ih003512345@fer.hr')

    def test_official_examples(self):
        self.assertEqual(derive_fer_email('Ivo', 'Horvat', '0036324986'), 'ih32498@fer.hr')
        self.assertEqual(derive_fer_email('Željka', 'Čižmek', '2000987654'), 'zc200098765@fer.hr')

    def test_diacritics_and_whitespace(self):
        self.assertEqual(derive_fer_email(' Čedo ', 'Šimić', ' 0036123456 '), 'cs12345@fer.hr')

    def test_unusable_parts(self):
        for args in (('1van', 'Horvat', '0036123456'), ('Ivan', '<b>', '0036123456'),
                     ('Ivan', 'Horvat', '٠٠٣٦١٢٣٤٥٦'), ('Ivan', 'Horvat', '0036')):
            with self.subTest(args=args):
                self.assertIsNone(derive_fer_email(*args))

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

class SponsorPortalTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.sponsor = Sponsors.objects.create(
            name='Acme', slug='acme-slug', visible=True, email='boss@acme.hr', guestCap=2, guestsEnabled=1)
        self.base = f'/api/sponsor-portal/{self.sponsor.access_token}/'

    def set_deadline(self, delta):
        Visibility.objects.update_or_create(name='SPONSORS_INPUT_TIME', defaults={'time': timezone.now() + delta})

    def add(self, name='Ana Anić'):
        return self.client.post(self.base + 'guests/', {'name': name}, format='json')

    def guest_url(self, guest_id):
        return f'{self.base}guests/{guest_id}/'

    def test_token_is_long_and_random(self):
        other = Sponsors.objects.create(name='Other', slug='other')
        self.assertGreaterEqual(len(self.sponsor.access_token), 40)
        self.assertNotEqual(self.sponsor.access_token, other.access_token)

    def test_unknown_token_404(self):
        self.assertEqual(self.client.get('/api/sponsor-portal/nope/').status_code, 404)
        self.assertEqual(self.client.post('/api/sponsor-portal/nope/guests/', {}).status_code, 404)

    def test_get_shape(self):
        self.add()
        res = self.client.get(self.base)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(set(res.data), {'name', 'image', 'guestCap', 'open', 'deadline', 'guests'})
        self.assertTrue(res.data['open'])
        self.assertEqual(res.data['guests'], [{'id': res.data['guests'][0]['id'], 'name': 'Ana Anić', 'entered': False}])

    def test_add_edit_delete(self):
        res = self.add(name='  Ana Anić ')
        self.assertEqual(res.status_code, 201)
        guest = Guests.objects.get(pk=res.data['id'])
        self.assertEqual((guest.name, guest.sponsor), ('Ana Anić', self.sponsor))
        self.assertEqual(guest.tag, 'acme-slug VIP - Sponzor - Acme')
        self.assertTrue(guest.bought)

        res = self.client.patch(self.guest_url(guest.id), {'name': 'Ana Horvat'}, format='json')
        self.assertEqual(res.status_code, 200)
        guest.refresh_from_db()
        self.assertEqual(guest.name, 'Ana Horvat')

        self.assertEqual(self.client.delete(self.guest_url(guest.id)).status_code, 204)
        self.assertFalse(Guests.objects.filter(pk=guest.pk).exists())

    def test_name_required(self):
        self.assertEqual(self.add(name='').status_code, 400)
        self.assertEqual(self.add(name='   ').status_code, 400)
        guest_id = self.add().data['id']
        self.assertEqual(self.client.patch(self.guest_url(guest_id), {'name': ''}, format='json').status_code, 400)

    def test_cap(self):
        self.add()
        self.add()
        self.assertEqual(self.add().status_code, 409)
        self.assertEqual(self.sponsor.guests.count(), 2)

    def test_no_cap_when_blank_or_zero(self):
        for cap in (None, 0):
            with self.subTest(cap=cap):
                Sponsors.objects.filter(pk=self.sponsor.pk).update(guestCap=cap)
                for _ in range(3):
                    self.assertEqual(self.add().status_code, 201)

    def test_closed_states(self):
        guest_id = self.add().data['id']
        cases = (
            (0, None, False, False),
            (1, -timedelta(hours=1), False, True),
            (1, timedelta(hours=1), True, True),
            (2, -timedelta(hours=1), True, False),
        )
        for enabled, delta, is_open, has_deadline in cases:
            with self.subTest(enabled=enabled, delta=delta):
                Sponsors.objects.filter(pk=self.sponsor.pk).update(guestsEnabled=enabled)
                Visibility.objects.filter(name='SPONSORS_INPUT_TIME').delete()
                if delta is not None:
                    self.set_deadline(delta)
                res = self.client.get(self.base)
                self.assertEqual(res.data['open'], is_open)
                self.assertEqual(res.data['deadline'] is not None, has_deadline)
                expected = (201, 200) if is_open else (403, 403)
                self.assertEqual(self.add().status_code, expected[0])
                patch = self.client.patch(self.guest_url(guest_id), {'name': 'X'}, format='json')
                self.assertEqual(patch.status_code, expected[1])
                if not is_open:
                    self.assertEqual(self.client.delete(self.guest_url(guest_id)).status_code, 403)
                Guests.objects.exclude(pk=guest_id).delete()

    def test_cannot_touch_other_sponsors_guest(self):
        other = Sponsors.objects.create(name='Other', slug='other')
        foreign = Guests.objects.create(name='Foreign', sponsor=other)
        self.assertEqual(self.client.patch(self.guest_url(foreign.id), {'name': 'X'}, format='json').status_code, 404)
        self.assertEqual(self.client.delete(self.guest_url(foreign.id)).status_code, 404)
        self.assertNotIn('Foreign', [g['name'] for g in self.client.get(self.base).data['guests']])

    def test_admin_list_shows_link_and_counts(self):
        Users.objects.create(email='admin@kset.org', privilege=Role.ADMIN)
        self.client.force_authenticate(DjangoUser.objects.create(username='admin@kset.org'))
        self.add()
        listed = self.client.get('/api/sponsors/').data[0]
        self.assertEqual(listed['link'], f'https://brucifer.kset.org/sponzori/{self.sponsor.access_token}')
        self.assertEqual((listed['guestsAdded'], listed['guestsEntered']), (1, 0))
        self.assertNotIn('access_token', listed)

    def test_admin_cannot_write_token(self):
        Users.objects.create(email='admin@kset.org', privilege=Role.ADMIN)
        self.client.force_authenticate(DjangoUser.objects.create(username='admin@kset.org'))
        self.client.patch(f'/api/sponsors/{self.sponsor.id}/', {'access_token': 'guessable'}, format='json')
        self.sponsor.refresh_from_db()
        self.assertNotEqual(self.sponsor.access_token, 'guessable')

    def test_hidden_sponsor_portal_still_works(self):
        Sponsors.objects.filter(pk=self.sponsor.pk).update(visible=False)
        self.assertEqual(self.client.get(self.base).status_code, 200)
        self.assertEqual(self.add().status_code, 201)

    def test_sponsor_deleted_mid_request(self):
        Sponsors.objects.filter(pk=self.sponsor.pk).delete()
        with self.assertRaises(Sponsors.DoesNotExist):
            add_sponsor_guest(self.sponsor, 'Ana')

    def test_throttle_is_per_token(self):
        other = Sponsors.objects.create(name='Other', slug='other')
        with mock.patch.object(SponsorPortalTokenThrottle, 'rate', '1/hour'):
            self.assertEqual(self.client.get(self.base).status_code, 200)
            self.assertEqual(self.client.get(self.base).status_code, 429)
            self.assertEqual(self.client.get(f'/api/sponsor-portal/{other.access_token}/').status_code, 200)

    def login_admin(self):
        Users.objects.create(email='admin@kset.org', privilege=Role.ADMIN)
        self.client.force_authenticate(DjangoUser.objects.create(username='admin@kset.org'))

    def test_admin_resending_tag_keeps_fk(self):
        self.login_admin()
        guest = Guests.objects.get(pk=self.add().data['id'])
        res = self.client.patch(f'/api/guests/{guest.id}/', {'name': 'VIP2', 'tag': guest.tag}, format='json')
        self.assertEqual(res.status_code, 200)
        guest.refresh_from_db()
        self.assertEqual((guest.name, guest.sponsor), ('VIP2', self.sponsor))

    def test_admin_sponsor_tag_links_fk_past_cap(self):
        self.login_admin()
        self.add()
        self.add()
        res = self.client.post('/api/guests/', {'name': 'X', 'tag': self.sponsor.guest_tag}, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Guests.objects.get(pk=res.data['id']).sponsor, self.sponsor)

        res = self.client.post('/api/guests/bulk-import/', [{'name': 'Y', 'tag': self.sponsor.guest_tag}], format='json')
        self.assertIn(res.status_code, (200, 201))
        self.assertEqual(self.sponsor.guests.count(), 4)

        plain = Guests.objects.create(name='P', tag='Brucoši')
        res = self.client.patch(f'/api/guests/{plain.id}/', {'tag': self.sponsor.guest_tag}, format='json')
        self.assertEqual(res.status_code, 200)
        plain.refresh_from_db()
        self.assertEqual(plain.sponsor, self.sponsor)

    def test_admin_retag_unlinks_sponsor_guest(self):
        self.login_admin()
        guest = Guests.objects.get(pk=self.add().data['id'])
        res = self.client.patch(f'/api/guests/{guest.id}/', {'tag': 'Brucoši', 'surname': 'S'}, format='json')
        self.assertEqual(res.status_code, 200)
        guest.refresh_from_db()
        self.assertIsNone(guest.sponsor)

    def test_admin_unknown_sponsor_tag_rejected(self):
        self.login_admin()
        res = self.client.post('/api/guests/', {'name': 'X', 'tag': 'nope VIP - Sponzor - Nope'}, format='json')
        self.assertEqual(res.status_code, 400)

    def test_save_without_name_skips_old_name_query(self):
        with self.assertNumQueries(1):
            self.sponsor.save(update_fields=['order'])

    def test_rename_retags_guests_only_on_name_change(self):
        self.login_admin()
        guest = Guests.objects.get(pk=self.add().data['id'])
        Guests.objects.filter(pk=guest.pk).update(tag='hand edited')
        self.client.patch(f'/api/sponsors/{self.sponsor.id}/', {'guestsEnabled': 2}, format='json')
        guest.refresh_from_db()
        self.assertEqual(guest.tag, 'hand edited')

        self.client.patch(f'/api/sponsors/{self.sponsor.id}/', {'name': 'Acme2'}, format='json')
        guest.refresh_from_db()
        self.assertEqual(guest.tag, 'acme-slug VIP - Sponzor - Acme2')

    def test_entered_guest_is_locked(self):
        guest_id = self.add().data['id']
        Guests.objects.filter(pk=guest_id).update(entered=True)
        self.assertEqual(self.client.patch(self.guest_url(guest_id), {'name': 'X'}, format='json').status_code, 409)
        self.assertEqual(self.client.delete(self.guest_url(guest_id)).status_code, 409)
        self.assertEqual(Guests.objects.get(pk=guest_id).name, 'Ana Anić')

    def test_unknown_token_not_throttled_per_token(self):
        with mock.patch.object(SponsorPortalTokenThrottle, 'rate', '1/hour'):
            for _ in range(3):
                self.assertEqual(self.client.get('/api/sponsor-portal/nope/').status_code, 404)

    def test_admin_cannot_change_slug(self):
        Users.objects.create(email='admin@kset.org', privilege=Role.ADMIN)
        self.client.force_authenticate(DjangoUser.objects.create(username='admin@kset.org'))
        self.client.patch(f'/api/sponsors/{self.sponsor.id}/', {'slug': 'new'}, format='json')
        self.sponsor.refresh_from_db()
        self.assertEqual(self.sponsor.slug, 'acme-slug')

    def test_missing_guest_404(self):
        self.assertEqual(self.client.patch(self.guest_url(999999), {'name': 'X'}, format='json').status_code, 404)
        self.assertEqual(self.client.delete(self.guest_url(999999)).status_code, 404)

    def test_migration_backfill(self):
        from importlib import import_module
        from django.apps import apps as django_apps
        backfill = import_module('bruc.migrations.0091_sponsor_guests_fk_and_token').backfill
        old = Guests.objects.create(name='Old', tag='acme-slug VIP - Sponzor - Acme')
        unrelated = Guests.objects.create(name='Bruc', tag='Brucoši')
        blank = Sponsors.objects.create(name='Blank', slug='')
        blank_guest = Guests.objects.create(name='B', tag='VIP - Sponzor - Blank')
        long_token = Sponsors.objects.create(name='Long', slug='long')
        Sponsors.objects.filter(pk=long_token.pk).update(access_token='x' * 100)
        token = self.sponsor.access_token
        backfill(django_apps, None)
        for obj in (old, unrelated, blank, blank_guest, long_token, self.sponsor):
            obj.refresh_from_db()
        self.assertEqual(old.sponsor, self.sponsor)
        self.assertIsNone(unrelated.sponsor)
        self.assertEqual(self.sponsor.access_token, token)
        self.assertEqual(blank_guest.sponsor, blank)
        self.assertTrue(blank.slug)
        self.assertEqual(blank_guest.tag, blank.guest_tag)
        self.assertLessEqual(len(long_token.access_token), 64)


def guests_url(guest, action):
    return f'/api/guests/{guest.id}/{action}/'


@override_settings(BREVO_WEBHOOK_TOKEN='secret-token', TICKET_MAIL_ASYNC=False)
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

    def login_with_jwt(self, role):
        email = f'jwt-{role}@kset.org'
        user = Users.objects.create(email=email, privilege=role)
        token = RefreshToken.for_user(DjangoUser.objects.create(username=email)).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return user

    def test_deleted_user_with_live_token_is_denied(self):
        user = self.login_with_jwt(Role.TICKETS)
        self.assertEqual(self.client.get('/api/guests/').status_code, 200)
        user.delete()
        self.assertEqual(self.client.get('/api/guests/').status_code, 403)
        self.assertEqual(self.sell().status_code, 403)
        self.guest.refresh_from_db()
        self.assertFalse(self.guest.bought)

    def test_demoted_seller_with_live_token_cannot_sell(self):
        user = self.login_with_jwt(Role.TICKETS)
        user.privilege = Role.ENTRY
        user.save()
        self.assertEqual(self.client.get('/api/guests/').status_code, 200)
        self.assertEqual(self.sell().status_code, 403)
        self.guest.refresh_from_db()
        self.assertFalse(self.guest.bought)

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
        self.assertEqual(set(BrucosiFormResponse.objects.values_list('status', flat=True)), {'pending'})
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
        self.guest.refresh_from_db()
        self.assertTrue(self.guest.bought)
        self.assertEqual((self.guest.mailStatus, self.guest.mailError), ('failed', 'adresa odbijena'))
        self.assertEqual(Mailer.objects.count(), 0)

    def test_mail_server_down(self):
        self.login_as(Role.TICKETS)
        with mock.patch('bruc.services.EmailMultiAlternatives.send', side_effect=ConnectionRefusedError()), \
                self.assertLogs('bruc.services', 'ERROR'):
            self.sell()
        self.assertEqual(Guests.objects.get(pk=self.guest.pk).mailError, 'mail server nedostupan')

    def test_brevo_rate_limit(self):
        self.login_as(Role.TICKETS)
        limited = smtplib.SMTPDataError(421, b'4.7.0 Too many messages')
        with mock.patch('bruc.services.EmailMultiAlternatives.send', side_effect=limited), \
                self.assertLogs('bruc.services', 'ERROR'):
            self.sell()
        guest = Guests.objects.get(pk=self.guest.pk)
        self.assertEqual((guest.mailStatus, guest.mailError), ('failed', 'Brevo privremeno odbija slanje, pokušaj ponovno'))
        self.assertTrue(guest.bought)

    @override_settings(TICKET_MAIL_ASYNC=True)
    def test_sell_sends_mail_in_background(self):
        self.login_as(Role.TICKETS)
        with mock.patch('bruc.services.threading.Thread') as thread:
            res = self.sell()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['guest']['mailStatus'], 'pending')
        thread.return_value.start.assert_called_once()
        self.assertEqual(len(mail.outbox), 0)

    def test_stale_pending_mail_counts_as_failed(self):
        now = timezone.now()
        stale = Guests.objects.create(tag='Brucoši', bought=True, mailStatus='pending',
                                      boughtTicketTime=now - timedelta(minutes=10))
        Guests.objects.create(tag='Brucoši', bought=True, mailStatus='pending', boughtTicketTime=now)
        self.login_as(Role.ADMIN)
        res = self.client.get('/api/guests/failed-mails/')
        self.assertEqual([g['id'] for g in res.data], [stale.id])

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

    def test_mail_outcome_dropped_if_unsold_during_send(self):
        def unsell_mid_send(*args, **kwargs):
            Guests.objects.filter(pk=self.guest.pk).update(bought=False, confCode='', mailStatus='none')
        self.login_as(Role.TICKETS)
        with mock.patch('bruc.services.EmailMultiAlternatives.send', side_effect=unsell_mid_send), \
                self.assertLogs('bruc.services', 'WARNING'):
            self.sell()
        guest = Guests.objects.get(pk=self.guest.pk)
        self.assertEqual((guest.bought, guest.mailStatus), (False, 'none'))

    def test_resend_while_pending_conflicts(self):
        Guests.objects.filter(pk=self.guest.pk).update(
            bought=True, confCode='abc', name='Ivan', surname='Horvat',
            mailStatus='pending', boughtTicketTime=timezone.now())
        self.login_as(Role.ADMIN)
        res = self.client.post(guests_url(self.guest, 'resend-mail'), {}, format='json')
        self.assertEqual(res.status_code, 409)
        self.assertEqual(len(mail.outbox), 0)

        Guests.objects.filter(pk=self.guest.pk).update(boughtTicketTime=timezone.now() - timedelta(minutes=10))
        res = self.client.post(guests_url(self.guest, 'resend-mail'), {}, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

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


GOOGLE_AUTH_URL = '/api/auth/google/'
REFRESH_URL = '/api/auth/token/refresh/'
LOGOUT_URL = '/api/auth/logout/'


class GuestCheckInTests(APITestCase):
    def setUp(self):
        self.guest = Guests.objects.create(name='Ivan', tag='Brucoši', bought=True)

    def login_as(self, role):
        email = f'{role}@kset.org'
        Users.objects.get_or_create(email=email, defaults={'privilege': role})
        self.client.force_authenticate(DjangoUser.objects.get_or_create(username=email)[0])

    def post(self, action):
        return self.client.post(guests_url(self.guest, action), {}, format='json')

    def test_check_in(self):
        self.login_as(Role.ENTRY)
        res = self.post('check-in')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data['guest']['entered'])
        self.guest.refresh_from_db()
        self.assertTrue(self.guest.entered)

    def test_second_check_in_conflicts_and_stays_entered(self):
        self.login_as(Role.ENTRY_TICKETS)
        self.assertEqual(self.post('check-in').status_code, 200)
        res = self.post('check-in')
        self.assertEqual(res.status_code, 409)
        self.assertTrue(res.data['guest']['entered'])
        self.guest.refresh_from_db()
        self.assertTrue(self.guest.entered)

    def test_undo_check_in(self):
        self.login_as(Role.ENTRY)
        self.post('check-in')
        res = self.post('undo-check-in')
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.data['guest']['entered'])
        self.assertEqual(self.post('check-in').status_code, 200)

    def test_permissions(self):
        for role in (Role.NONE, Role.TICKETS):
            for action in ('check-in', 'undo-check-in'):
                with self.subTest(role=role, action=action):
                    self.login_as(role)
                    self.assertEqual(self.post(action).status_code, 403)
        self.guest.refresh_from_db()
        self.assertFalse(self.guest.entered)


class AuthCookieTests(APITestCase):
    EMAIL = 'admin@kset.org'

    def setUp(self):
        cache.clear()
        Users.objects.create(email=self.EMAIL, name='Admin', privilege=Role.ADMIN)
        self.client.defaults['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

    @mock.patch('bruc.views.id_token.verify_oauth2_token')
    def login(self, verify):
        verify.return_value = {'email': self.EMAIL, 'email_verified': True, 'hd': 'kset.org', 'name': 'Admin'}
        return self.client.post(GOOGLE_AUTH_URL, {'token': 'google-id-token'}, format='json')

    def refresh_cookie(self, res):
        return res.cookies[settings.AUTH_REFRESH_COOKIE]

    def test_login_sets_httponly_cookie_and_hides_refresh(self):
        res = self.login()
        self.assertEqual(res.status_code, 200)
        self.assertIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.data['user']['role'], Role.ADMIN)
        cookie = self.refresh_cookie(res)
        self.assertTrue(cookie['httponly'])
        self.assertEqual(cookie['path'], settings.AUTH_REFRESH_COOKIE_PATH)
        self.assertEqual(cookie['samesite'], 'Strict')

    @mock.patch('bruc.views.id_token.verify_oauth2_token')
    def test_outside_domain_with_privilege_can_login(self, verify):
        Users.objects.create(email='someone@gmail.com', privilege=Role.ENTRY)
        verify.return_value = {'email': 'someone@gmail.com', 'email_verified': True, 'name': 'Someone'}
        res = self.client.post(GOOGLE_AUTH_URL, {'token': 'google-id-token'}, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['user']['role'], Role.ENTRY)

    @mock.patch('bruc.views.id_token.verify_oauth2_token')
    def test_outside_domain_without_privilege_rejected(self, verify):
        verify.return_value = {'email': 'stranger@gmail.com', 'email_verified': True, 'name': 'Stranger'}
        res = self.client.post(GOOGLE_AUTH_URL, {'token': 'google-id-token'}, format='json')
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.data['code'], 'no_privileges')
        self.assertEqual(Users.objects.get(email='stranger@gmail.com').privilege, Role.NONE)
        self.assertNotIn(settings.AUTH_REFRESH_COOKIE, res.cookies)

    @mock.patch('bruc.views.id_token.verify_oauth2_token', side_effect=ValueError('bad token'))
    def test_invalid_google_token_rejected(self, _):
        res = self.client.post(GOOGLE_AUTH_URL, {'token': 'forged'}, format='json')
        self.assertEqual(res.status_code, 400)
        self.assertNotIn(settings.AUTH_REFRESH_COOKIE, res.cookies)

    def test_refresh_rotates_cookie_and_old_one_is_rejected(self):
        old = self.refresh_cookie(self.login()).value
        res = self.client.post(REFRESH_URL)
        self.assertEqual(res.status_code, 200)
        self.assertIn('access', res.data)
        self.assertNotEqual(self.refresh_cookie(res).value, old)

        self.client.cookies[settings.AUTH_REFRESH_COOKIE] = old
        self.assertEqual(self.client.post(REFRESH_URL).status_code, 401)

    def test_login_without_role_gets_no_session(self):
        Users.objects.filter(email=self.EMAIL).update(privilege=Role.NONE)
        res = self.login()
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.data['code'], 'no_privileges')
        self.assertNotIn('access', res.data)
        self.assertNotIn(settings.AUTH_REFRESH_COOKIE, res.cookies)

    def test_refresh_returns_user(self):
        self.login()
        self.assertEqual(self.client.post(REFRESH_URL).data['user']['role'], Role.ADMIN)

    def test_cookie_endpoints_require_xhr_header(self):
        self.login()
        del self.client.defaults['HTTP_X_REQUESTED_WITH']
        self.assertEqual(self.client.post(REFRESH_URL).status_code, 403)
        self.assertEqual(self.client.post(LOGOUT_URL).status_code, 403)

    def test_refreshed_access_token_works(self):
        self.login()
        access = self.client.post(REFRESH_URL).data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertEqual(self.client.get('/api/me/').data['role'], Role.ADMIN)

    def test_refresh_without_cookie_is_401(self):
        self.assertEqual(self.client.post(REFRESH_URL).status_code, 401)

    def test_logout_revokes_refresh_token(self):
        token = self.refresh_cookie(self.login()).value
        res = self.client.post(LOGOUT_URL)
        self.assertEqual(res.status_code, 204)
        self.assertEqual(self.refresh_cookie(res).value, '')

        self.client.cookies[settings.AUTH_REFRESH_COOKIE] = token
        self.assertEqual(self.client.post(REFRESH_URL).status_code, 401)

    def test_refresh_ends_session_of_user_without_rights(self):
        for change in ('demote', 'delete'):
            with self.subTest(change=change):
                Users.objects.update_or_create(email=self.EMAIL, defaults={'privilege': Role.ADMIN})
                token = self.refresh_cookie(self.login()).value
                users = Users.objects.filter(email=self.EMAIL)
                if change == 'demote':
                    users.update(privilege=Role.NONE)
                else:
                    users.delete()

                res = self.client.post(REFRESH_URL)
                self.assertEqual(res.status_code, 401)
                self.assertEqual(self.refresh_cookie(res).value, '')

                # revoked for good, even if the role comes back
                Users.objects.update_or_create(email=self.EMAIL, defaults={'privilege': Role.ADMIN})
                self.client.cookies[settings.AUTH_REFRESH_COOKIE] = token
                self.assertEqual(self.client.post(REFRESH_URL).status_code, 401)

    @mock.patch('bruc.views.id_token.verify_oauth2_token')
    def test_login_rejects_cross_site_posts(self, verify):
        verify.return_value = {'email': self.EMAIL, 'email_verified': True, 'hd': 'kset.org', 'name': 'Admin'}
        res = self.client.post(GOOGLE_AUTH_URL, {'token': 'google-id-token'})
        self.assertEqual(res.status_code, 415)
        self.assertNotIn(settings.AUTH_REFRESH_COOKIE, res.cookies)

        del self.client.defaults['HTTP_X_REQUESTED_WITH']
        res = self.client.post(GOOGLE_AUTH_URL, {'token': 'google-id-token'}, format='json')
        self.assertEqual(res.status_code, 403)
        self.assertNotIn(settings.AUTH_REFRESH_COOKIE, res.cookies)

    def test_relogin_revokes_previous_refresh_token(self):
        old = self.refresh_cookie(self.login()).value
        self.assertNotEqual(self.refresh_cookie(self.login()).value, old)

        self.client.cookies[settings.AUTH_REFRESH_COOKIE] = old
        self.assertEqual(self.client.post(REFRESH_URL).status_code, 401)

    def test_login_db_error_is_400(self):
        with mock.patch.object(DjangoUser.objects, 'get_or_create', side_effect=IntegrityError):
            res = self.login()
        self.assertEqual(res.status_code, 400)
        self.assertNotIn(settings.AUTH_REFRESH_COOKIE, res.cookies)

    def test_refresh_ends_session_of_deactivated_user(self):
        self.login()
        DjangoUser.objects.filter(username=self.EMAIL).update(is_active=False)
        res = self.client.post(REFRESH_URL)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(self.refresh_cookie(res).value, '')

    def test_login_rejects_deactivated_user(self):
        DjangoUser.objects.create(username=self.EMAIL, email=self.EMAIL, is_active=False)
        res = self.login()
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.data['code'], 'no_privileges')
        self.assertNotIn('access', res.data)
        self.assertNotIn(settings.AUTH_REFRESH_COOKIE, res.cookies)

    def test_login_token_db_error_is_400(self):
        with mock.patch('bruc.views.RefreshToken.for_user', side_effect=IntegrityError):
            res = self.login()
        self.assertEqual(res.status_code, 400)
        self.assertNotIn(settings.AUTH_REFRESH_COOKIE, res.cookies)

    def test_concurrent_refresh_loser_is_rejected(self):
        self.login()
        # another request blacklisted the token between our blacklist check and our write
        with mock.patch('bruc.views.RefreshToken.blacklist', return_value=(None, False)):
            res = self.client.post(REFRESH_URL)
        self.assertEqual(res.status_code, 401)
        self.assertNotIn(settings.AUTH_REFRESH_COOKIE, res.cookies)

    def test_refresh_db_error_is_503(self):
        self.login()
        with mock.patch('bruc.views.RefreshToken.for_user', side_effect=IntegrityError):
            res = self.client.post(REFRESH_URL)
        self.assertEqual(res.status_code, 503)
        self.assertNotIn(settings.AUTH_REFRESH_COOKIE, res.cookies)

    def test_me_matches_refresh_payload(self):
        self.login()
        data = self.client.post(REFRESH_URL).data
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {data['access']}")
        me = self.client.get('/api/me/').data
        self.assertEqual(me, data['user'])
        self.assertNotIn('id', me)

    def test_refresh_is_throttled(self):
        self.login()
        with mock.patch.object(RefreshThrottle, 'rate', '1/minute'):
            self.assertEqual(self.client.post(REFRESH_URL).status_code, 200)
            self.assertEqual(self.client.post(REFRESH_URL).status_code, 429)

    def test_revocation_db_error_is_503(self):
        self.login()
        Users.objects.filter(email=self.EMAIL).update(privilege=Role.NONE)
        with mock.patch('bruc.views.RefreshToken.blacklist', side_effect=IntegrityError):
            res = self.client.post(REFRESH_URL)
        self.assertEqual(res.status_code, 503)
        self.assertNotIn(settings.AUTH_REFRESH_COOKIE, res.cookies)


class DiacriticSearchTests(APITestCase):
    def setUp(self):
        Guests.objects.create(name='Ivan', surname='Ćosić', tag='Brucoši')
        Guests.objects.create(name='Đuro', surname='Šimić', tag='Brucoši')
        Guests.objects.create(name='Djordje', surname='Cosic', tag='Gost')
        email = f'{Role.ADMIN}@kset.org'
        Users.objects.get_or_create(email=email, defaults={'privilege': Role.ADMIN})
        self.client.force_authenticate(DjangoUser.objects.get_or_create(username=email)[0])

    def search(self, term, **extra):
        res = self.client.get('/api/guests/', {'name_search': term, **extra})
        self.assertEqual(res.status_code, 200)
        return sorted(f"{g['name']} {g['surname']}" for g in res.data)

    def test_fold(self):
        self.assertEqual(fold('ČĆŠŽĐ čćšžđ'), 'ccszd ccszd')
        self.assertEqual(fold('Djuro'), fold('Đuro'))
        self.assertIsNone(fold(None))

    def test_ignores_diacritics_and_case(self):
        for term in ('cosic', 'ćosić', 'COSIC', 'Čosic'):
            with self.subTest(term=term):
                self.assertEqual(self.search(term), ['Djordje Cosic', 'Ivan Ćosić'])

    def test_dj_matches_đ(self):
        for term in ('djuro', 'duro', 'đuro', 'simic'):
            with self.subTest(term=term):
                self.assertEqual(self.search(term), ['Đuro Šimić'])
        self.assertEqual(self.search('đorđe'), ['Djordje Cosic'])

    def test_finds_everything_a_plain_search_finds(self):
        Guests.objects.create(name='Marko', surname='Djurdjević')
        self.assertEqual(self.search('jur'), ['Marko Djurdjević', 'Đuro Šimić'])
        self.assertEqual(self.search('rdjev'), ['Marko Djurdjević'])

    def test_every_term_must_match(self):
        self.assertEqual(self.search('cosic ivan'), ['Ivan Ćosić'])
        self.assertEqual(self.search('cosic marko'), [])

    def test_tag_filter_is_separate_from_search_text(self):
        # "cos" must not match every "Brucoši" guest through the tag
        self.assertEqual(self.search('cos', tag__icontains='Brucoši'), ['Ivan Ćosić'])
        self.assertEqual(self.search('cos'), ['Djordje Cosic', 'Ivan Ćosić'])

    def test_tag_filter_matches_part_of_the_tag(self):
        sponsor = Sponsors.objects.create(name='Pivo', slug='pivo')
        Guests.objects.create(name='Ana', surname='Horvat', tag=sponsor.guest_tag)
        self.assertEqual(self.search('', tag__icontains='VIP'), ['Ana Horvat'])
        self.assertEqual(self.search('ana', tag__icontains='Sponzor'), ['Ana Horvat'])

    def limited(self, term, limit, **extra):
        res = self.client.get('/api/guests/', {'name_search': term, 'limit': limit, **extra})
        self.assertEqual(res.status_code, 200)
        return [f"{g['name']} {g['surname']}" for g in res.data]

    def test_limit_returns_best_matches_first(self):
        Guests.objects.create(name='Ivana', surname='Babić', tag='Brucoši')
        Guests.objects.create(name='Ana', surname='Zorić', tag='Gost')
        Guests.objects.create(name='Marijana', surname='Anić', tag='Brucoši')
        # "Ana" starts with the term, so it beats names that only contain it
        self.assertEqual(self.limited('ana', 2), ['Ana Zorić', 'Marijana Anić'])
        self.assertEqual(self.limited('ana', 51), ['Ana Zorić', 'Marijana Anić', 'Ivana Babić'])
        self.assertEqual(self.limited('ana', 51, tag__icontains='Brucoši'), ['Marijana Anić', 'Ivana Babić'])
        self.assertEqual(self.limited('cosic ivan', 1), ['Ivan Ćosić'])
        Guests.objects.create(name='ANA', surname='ZEC')
        self.assertEqual(self.limited('ana', 2), ['ANA ZEC', 'Ana Zorić'])  # sorted ignoring case

    def test_diacritic_surnames_sort_with_their_base_letter(self):
        for surname in ('Zorić', 'Šarić', 'Sabo', 'Čović', 'Cvitan'):
            Guests.objects.create(name='Ana', surname=surname)
        self.assertEqual(self.limited('ana', 3), ['Ana Čović', 'Ana Cvitan', 'Ana Sabo'])

    def test_whole_name_in_one_field_sorts_with_the_rest(self):
        Guests.objects.create(name='Zora  Ivić')
        Guests.objects.create(name='Ivo', surname='Horvat')
        Guests.objects.create(surname='Ana Ivanković')
        self.assertEqual(self.limited('iv', 4), [' Ana Ivanković', 'Ivan Ćosić', 'Ivo Horvat', 'Zora  Ivić '])
        self.assertEqual(self.search('ivic zora'), ['Zora  Ivić '])

    def test_without_limit_everything_is_returned(self):
        res = self.client.get('/api/guests/')
        self.assertEqual(len(res.data), Guests.objects.count())

    def test_invalid_limit(self):
        for limit in ('0', 'abc', '201', '-1'):
            with self.subTest(limit=limit):
                res = self.client.get('/api/guests/', {'name_search': 'ana', 'limit': limit})
                self.assertEqual(res.status_code, 400)

    def test_decomposed_and_foreign_accents(self):
        # NFD text (č as c + combining caron) is what a paste from macOS can produce
        Guests.objects.create(name=unicodedata.normalize('NFD', 'Saša'), surname=unicodedata.normalize('NFD', 'Ćurić'))
        Guests.objects.create(name='Zoë', surname='Müller')
        Guests.objects.create(name='Lana', surname='Ðurić')  # eth, a lookalike of Đ
        for term in ('sasa', 'Saša', unicodedata.normalize('NFD', 'ćurić')):
            with self.subTest(term=term):
                self.assertEqual(self.search(term), [unicodedata.normalize('NFD', 'Saša Ćurić')])
        self.assertEqual(self.search('zoe muller'), ['Zoë Müller'])
        self.assertEqual(self.search('lana djuric'), ['Lana Ðurić'])

    def test_like_wildcards_are_literal(self):
        Guests.objects.create(name='100%', surname='a_b')
        self.assertEqual(self.search('%'), ['100% a_b'])
        self.assertEqual(self.search('_'), ['100% a_b'])

    def test_invisible_characters_are_ignored(self):
        Guests.objects.create(name='Mar\u00adko', surname='Pe\u200btrić')  # soft hyphen, zero-width space
        self.assertEqual(self.search('marko petric'), ['Mar\u00adko Pe\u200btrić'])
        self.assertEqual(self.search('ivan\u200b'), ['Ivan Ćosić'])

    def test_long_paste_is_not_a_server_error(self):
        res = self.client.get('/api/guests/', {'name_search': ' '.join(['cosic'] * 300), 'limit': 50})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)

    def test_key_separator_is_not_searchable(self):
        self.assertEqual(self.search('|'), [])

    def test_search_key_follows_every_write(self):
        res = self.client.post('/api/guests/bulk-import/', [{'name': 'Žana', 'surname': 'Đokić'}], format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(self.search('zana dokic'), ['Žana Đokić'])
        guest = Guests.objects.get(name='Žana')
        res = self.client.patch(f'/api/guests/{guest.id}/', {'surname': 'Šegvić'}, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.search('zana dokic'), [])
        self.assertEqual(self.search('segvic'), ['Žana Šegvić'])
        guest.refresh_from_db()
        guest.name = 'Čedna'
        guest.save(update_fields=['name'])
        self.assertEqual(self.search('cedna'), ['Čedna Šegvić'])
        self.assertNotIn('searchKey', res.data)

    def test_generic_search_is_not_folded(self):
        # exact slug lookups and tag counting must not merge 'djmag' with 'dmag' or 'Đak' with 'Dak'
        Lineup.objects.create(slug='djmag', name='DJ Mag')
        Lineup.objects.create(slug='dmag', name='D Mag')
        res = self.client.get('/api/lineup/', {'search': 'dmag', 'search_fields': 'slug'})
        self.assertEqual([l['slug'] for l in res.data], ['dmag'])
        Guests.objects.create(name='A', tag='Đak')
        Guests.objects.create(name='B', tag='Dak')
        res = self.client.get('/api/guests/', {'search': 'Dak', 'search_fields': 'tag'})
        self.assertEqual([g['name'] for g in res.data], ['B'])


@override_settings(TICKET_MAIL_ASYNC=False)
class SearchKeyWritePathsTests(APITestCase):
    """Every way a guest's name can be written must leave searchKey matching it, or the door can't find them."""

    def setUp(self):
        cache.clear()
        email = f'{Role.ADMIN}@kset.org'
        Users.objects.get_or_create(email=email, defaults={'privilege': Role.ADMIN})
        self.client.force_authenticate(DjangoUser.objects.get_or_create(username=email)[0])
        self.sponsor = Sponsors.objects.create(name='Acme', slug='acme', visible=True, guestCap=5, guestsEnabled=1)
        self.portal = f'/api/sponsor-portal/{self.sponsor.access_token}/guests/'

    def tearDown(self):
        stale = [g for g in Guests.objects.all() if g.searchKey != search_key(g.name, g.surname)]
        self.assertEqual(stale, [])

    def found(self, term):
        res = self.client.get('/api/guests/', {'name_search': term})
        return [f"{g['name']} {g['surname']}".strip() for g in res.data]

    def test_admin_create_and_edit(self):
        res = self.client.post('/api/guests/', {'name': 'Đuro', 'surname': 'Šimić', 'tag': 'Gost'}, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(self.found('djuro simic'), ['Đuro Šimić'])
        res = self.client.put(f"/api/guests/{res.data['id']}/", {'name': 'Žana', 'surname': 'Čolić', 'tag': 'Gost'},
                              format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.found('simic'), [])
        self.assertEqual(self.found('zana colic'), ['Žana Čolić'])

    def test_bulk_import(self):
        rows = [{'name': 'Ćiro', 'surname': 'Đokić'}, {'name': 'Šime', 'surname': 'Žic'}]
        self.assertEqual(self.client.post('/api/guests/bulk-import/', rows, format='json').status_code, 201)
        self.assertEqual(self.found('ciro dokic'), ['Ćiro Đokić'])
        self.assertEqual(self.found('sime zic'), ['Šime Žic'])

    def test_bulk_import_whole_name_in_one_field(self):
        rows = [{'name': 'Ana  Marić Bilić'}, {'surname': 'Ivo Šimić'}]
        self.assertEqual(self.client.post('/api/guests/bulk-import/', rows, format='json').status_code, 201)
        for term in ('ana', 'maric', 'bil', 'bilic ana'):
            with self.subTest(term=term):
                self.assertEqual(self.found(term), ['Ana  Marić Bilić'])
        self.assertEqual(self.found('simic ivo'), ['Ivo Šimić'])
        self.assertEqual(Guests.objects.get(surname='Ivo Šimić').searchKey, ' ivo simic\n ivo simic')

    def test_sponsor_portal_add_and_rename(self):
        res = self.client.post(self.portal, {'name': 'Đurđa Čačić'}, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(self.found('durda cacic'), ['Đurđa Čačić'])
        res = self.client.patch(f"{self.portal}{res.data['id']}/", {'name': 'Šima Žic'}, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.found('cacic'), [])
        self.assertEqual(self.found('sima'), ['Šima Žic'])

    def test_brucosi_ticket_sale_and_resend(self):
        guest = Guests.objects.create(jmbag='0036123456', tag='Brucoši')
        BrucosiFormResponse.objects.create(name='Čedo', surname='Šarić', jmbag='0036123456', gdpr_accepted=True)
        self.assertEqual(self.client.post(guests_url(guest, 'sell'), {}, format='json').status_code, 200)
        self.assertEqual(self.found('cedo saric'), ['Čedo Šarić'])
        res = self.client.post(guests_url(guest, 'resend-mail'), {'surname': 'Đorđević'}, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.found('saric'), [])
        self.assertEqual(self.found('cedo djordjevic'), ['Čedo Đorđević'])

    def test_bulk_update_fills_the_key(self):
        guest = Guests.objects.create(name='Ana')
        guest.name = 'Ćana'
        Guests.objects.bulk_update([guest], ['name'])
        self.assertEqual(self.found('cana'), ['Ćana'])

    def test_queryset_update_keys_every_row(self):
        Guests.objects.create(name='Ana', surname='Šarić', tag='X')
        Guests.objects.create(name='Iva', surname='Đokić', tag='X')
        Guests.objects.create(name='Eva', surname='Žic', tag='Y')
        self.assertEqual(Guests.objects.filter(tag='X').update(name='Ćana'), 2)
        self.assertEqual(self.found('cana saric'), ['Ćana Šarić'])
        self.assertEqual(self.found('cana dokic'), ['Ćana Đokić'])
        # the update changes the field it filters on, and F() differs per row
        Guests.objects.filter(name='Ćana').update(name=F('surname'))
        self.assertEqual(sorted(self.found('dokic')), ['Đokić Đokić'])
        with self.assertRaises(ValueError):
            Guests.objects.update(searchKey='x')
