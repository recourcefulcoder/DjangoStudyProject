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
