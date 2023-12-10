from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse_lazy
from parameterized import parameterized

from users import models


class TestCreateUser(TestCase):
    @parameterized.expand(
        [
            ("User", "Userov", "test@mail.com", "dad4hf844f", "dad4hf844f"),
            ("User", "Userov", "te.st@mail.com", "dad4hf844f", "dad4hf844f"),
        ],
    )
    def test_create_user_with_valid_data(
        self,
        first_name,
        last_name,
        email,
        password1,
        password2,
    ):
        objects_count = models.User.objects.count()

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password1": password1,
            "password2": password2,
        }

        Client().post(reverse_lazy("users:signup"), data=data)

        self.assertEqual(objects_count + 1, models.User.objects.count())

    @parameterized.expand(
        [
            ("", "Userov", "test@mail.com", "dad4hf844f", "dad4hf844f"),
            ("User", "Userov", "testmail.com", "dad4hf844f", "dad4hf844f"),
            ("User", "Userov", "", "dad4hf844f", "dad4hf844f"),
            ("User", "Userov", "test@mail.com", "", "dad4hf844f"),
            ("User", "Userov", "test@mail.com", "dad4hf844f", "dad4hf844fA"),
            ("User", "Userov", "test@mail.com", "User", "User"),
        ],
    )
    def test_create_user_with_invalid_data(
        self,
        first_name,
        last_name,
        email,
        password1,
        password2,
    ):
        objects_count = models.User.objects.count()

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password1": password1,
            "password2": password2,
        }

        Client().post(reverse_lazy("users:signup"), data=data)

        self.assertEqual(objects_count, models.User.objects.count())


class TestUsersProfileUnloggedViews(TestCase):
    def setUp(self):
        self.client = Client()

    @parameterized.expand(
        [
            ("users:companies",),
            ("users:create_company",),
        ],
    )
    def test_profile_endpoints_unlogged(self, url_name):
        response = self.client.get(reverse_lazy(url_name))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @parameterized.expand(
        [
            ("users:companies",),
            ("users:create_company",),
        ],
    )
    def test_profile_endpoints_unlogged_redirects(self, url_name):
        response = self.client.get(reverse_lazy(url_name), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_settings_endpoint_unlogged(self):
        response = self.client.get(reverse_lazy("users:profile"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_profile_settings_endpoint_unlogged_redirects(self):
        response = self.client.get(
            reverse_lazy("users:profile"),
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestUsersProfileView(TestCase):
    fixtures = ["fixtures/users.json"]

    def setUp(self):
        self.client = Client()
        logged = self.client.login(email="test@test.com", password="admin")
        self.assertTrue(
            logged,
            "user is not logged in, check password and email",
        )

    def tearDown(self):
        self.client.logout()

    def test_user_update_form_in_context(self):
        response = self.client.get(
            reverse_lazy(
                "users:profile",
            ),
        )
        self.assertIn("form", response.context)

    def test_create_company_form_in_context(self):
        response = self.client.get(reverse_lazy("users:create_company"))
        self.assertIn("form", response.context)
