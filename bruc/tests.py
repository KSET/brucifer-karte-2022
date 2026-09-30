from django.contrib.auth.models import User as DjangoUser
from django.core.cache import cache
from django.test import override_settings
from rest_framework.test import APITestCase

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
