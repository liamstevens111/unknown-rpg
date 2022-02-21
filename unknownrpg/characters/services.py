from .models import Character


def character_create(*, user: str, name: str) -> Character:
    character = Character(user=user, name=name, level=1, gold=0, current_xp=0)
    character.full_clean()
    character.save()
