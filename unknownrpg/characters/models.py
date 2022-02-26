from django.db import models
from django.conf import settings
from common.models import BaseModel

from django.core.exceptions import ValidationError
from django.db.models.functions import Lower

from .constants import max_inventory_size, level_xp_requirements
from .formulas import max_hp_from_character_level


class Character(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    level = models.IntegerField()
    gold = models.IntegerField()
    current_xp = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'), name='unique_lower_character_name')
        ]

    def __str__(self):
        return self.name

    @property
    def max_hp(self):
        return max_hp_from_character_level(level=self.level)

    @property
    def required_xp(self):
        return level_xp_requirements.get(self.level + 1, None)

    @property
    def free_spaces(self):
        return max_inventory_size - self.items.filter(container='inventory').count()

    @property
    def has_space(self):
        return self.free_spaces > 0

    def gain_xp(self, value):
        if self.required_xp is None or value <= 0:
            return

        self.current_xp += value

        while self.required_xp is not None and self.current_xp >= self.required_xp:
            self.current_xp -= self.required_xp
            self.level += 1
        else:
            if self.required_xp is None:
                self.current_xp = 0

        self.save()
