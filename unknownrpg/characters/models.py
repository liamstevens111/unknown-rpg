from django.db import models
from django.conf import settings
from items.models import Item

from django.core.exceptions import ValidationError 
from django.db.models.functions import Lower

class Character(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    level = models.IntegerField()
    gold = models.IntegerField()
    current_hp = models.IntegerField()
    current_xp = models.IntegerField()

    equipment = models.ManyToManyField(
        Item, through='CharacterEquipment', related_name='equipment_character')
    inventory = models.ManyToManyField(
        Item, through='CharacterInventory', related_name='inventory_character')
    
    class Meta:
        constraints = [
                models.UniqueConstraint(Lower('name'), name='unique_lower_character_name')
            ]

    def __str__(self):
        return self.name
    


class CharacterInventory(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Character Inventory'


class CharacterEquipment(models.Model):
    WEAPON = 'weapon'
    ARMOUR = 'armour'
    HELMET = 'helmet'
    NECKLACE = 'necklace'
    BRACELET = 'bracelet'
    RING = 'ring'

    SLOT_TYPE_CHOICES = (
        (WEAPON, 'Weapon'),
        (ARMOUR, 'Armour'),
        (HELMET, 'Helmet'),
        (NECKLACE, 'Necklace'),
        (BRACELET, 'Bracelet'),
        (RING, 'Ring'),
    )

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    slot = models.CharField('slot', max_length=20, choices=SLOT_TYPE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('character', 'slot'), name='unique_character_slot')
        ]
        verbose_name_plural = 'Character Equipment'
    

    def clean(self):
        super().clean()

        if self.slot != self.item.type:
            raise ValidationError('The item type and slot are different')
