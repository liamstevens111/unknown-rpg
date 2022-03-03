from typing import Optional
from .models import BaseUser
from characters.services import character_create


def user_create(*, email: str, character_name: str, is_active: bool = True, is_admin: bool = False, password: Optional[str] = None) -> BaseUser:
    user = BaseUser.objects.create_user(
        email=email, is_active=is_active, is_admin=is_admin, password=password)

    character_create(user=user, name=character_name)

    return user
