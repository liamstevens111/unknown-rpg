from django.db import models


class ItemBase(models.Model):
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
    # image = Field to store Image?
    type = models.CharField('type', max_length=20,
                            choices=ITEM_TYPE_CHOICES, default=WEAPON)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ItemTemplate(ItemBase):
    pass


class Item(ItemBase):
    template = models.ForeignKey(ItemTemplate, on_delete=models.CASCADE)
