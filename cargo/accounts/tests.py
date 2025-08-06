from django.test import TestCase

from .forms import UserRegisterForm
from .models import CustomUser


class UserRegistrationAuthKeyTest(TestCase):
    def test_auth_key_generated_on_registration(self):
        form = UserRegisterForm(data={
            'gmail': 'test@example.com',
            'phone_number': '123456789',
            'first_name': 'John',
            'last_name': 'Doe',
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.auth_key)
        self.assertEqual(len(user.auth_key), 5)
        self.assertEqual(CustomUser.objects.count(), 1)
