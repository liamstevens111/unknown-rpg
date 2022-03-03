from django.test import TestCase
from django.core.exceptions import ValidationError

from users.models import BaseUser
from users.services import user_create


class UserCreateTests(TestCase):
    def setUp(self):
        pass

    def test_user_with_capitalized_email_is_normalized(self):
        user = user_create(email='RANDOM_User@Email.Com',
                           password='SomePassw0rd12', character_name='RandomCharacterName')

        self.assertEqual('random_user@email.com', user.email)

        # with self.assertRaises(ValidationError):
        #     user_create(
        #         email='RANDOM_user@email.com'
        #     )

        # self.assertEqual(1, BaseUser.objects.count())
