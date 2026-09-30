from django.contrib.auth.models import User as DjangoUser
from django.core.cache import cache
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import BrucosiFormResponse, Users
from .roles import Role

SUBMIT_URL = '/api/forms/brucosi-form-submit/'
LIST_URL = '/api/forms/'


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
        self.assertEqual(self.client.post(LIST_URL, valid_payload(), format='json').status_code, 405)

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
