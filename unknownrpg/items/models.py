from django.db import models
from django.db.models import Q
from common.models import BaseModel
from characters.models import Character


class ItemTemplate(BaseModel):
    WEAPON = 'weapon'
    ARMOUR = 'armour'
    HELMET = 'helmet'
    NECKLACE = 'necklace'
    BRACELET = 'bracelet'
    RING = 'ring'

    ITEM_TYPE_CHOICES = (
        (WEAPON, 'Weapon'),
        (ARMOUR, 'Armour'),
        (HELMET, 'Helmet'),
        (NECKLACE, 'Necklace'),
        (BRACELET, 'Bracelet'),
        (RING, 'Ring'),
    )

    name = models.CharField('name', max_length=30, unique=True)
    level_requirement = models.IntegerField()
    min_damage = models.IntegerField()
    max_damage = models.IntegerField()
    min_armour = models.IntegerField()
    max_armour = models.IntegerField()
    value = models.IntegerField()
    is_purchasable = models.BooleanField(
        default=False, verbose_name='Is purchasable')
    # image = Field to store Image?
    type = models.CharField(max_length=20,
                            choices=ITEM_TYPE_CHOICES, default=WEAPON)

    def __str__(self):
        return self.name


class Item(BaseModel):
    INVENTORY = 'inventory'
    EQUIPMENT = 'equipment'

    CONTAINER_CHOICES = (
        (INVENTORY, 'Inventory'),
        (EQUIPMENT, 'Equipment'),
    )

    character = models.ForeignKey(
        Character, related_name='items', on_delete=models.CASCADE)
    template = models.ForeignKey(ItemTemplate, on_delete=models.CASCADE)
    name = models.CharField('name', max_length=30, unique=False)
    container = models.CharField(
        max_length=20, choices=CONTAINER_CHOICES, default=INVENTORY)

    has_bonuses = models.BooleanField(default=False)
    bonus_min_damage = models.IntegerField(default=0)
    bonus_max_damage = models.IntegerField(default=0)
    bonus_min_armour = models.IntegerField(default=0)
    bonus_max_armour = models.IntegerField(default=0)
    bonus_value = models.IntegerField(default=0)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=('character', 'container_type'), condition=Q(container_type='equipment'), name='unique_character_equipped_item_type')
    #     ]

    @ property
    def min_damage(self):
        return self.template.min_damage + self.bonus_min_damage

    @ property
    def max_damage(self):
        return self.template.max_damage + self.bonus_max_damage

    @ property
    def min_armour(self):
        return self.template.min_armour + self.bonus_min_armour

    @ property
    def max_armour(self):
        return self.template.max_armour + self.bonus_max_armour

    @ property
    def type(self):
        return self.template.type

    @ property
    def value(self):
        return self.template.value + self.bonus_value

    @ property
    def level_requirement(self):
        return self.template.level_requirement

    def __str__(self):
        return self.name
