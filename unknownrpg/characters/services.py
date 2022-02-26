from django.db.models import F

from .models import Character

from items.services import item_create
from items.models import ItemTemplate, Item

# Internal


def character_create(*, user: str, name: str) -> Character:
    character = Character(user=user, name=name, level=1, gold=0, current_xp=0)
    character.full_clean()
    character.save()

# Internal


def item_buy(*, character: Character, item_template: ItemTemplate):
    # Maybe can do some checks here for when/where the purchase is being made, ie shop ID parameter to ensure they are in correct location
    if item_template.is_purchasable and character.gold >= item_template.value and character.has_space:
        item_create(character=character, item_template=item_template)
        character.gold = F('gold') - item_template.value
        character.save()


def item_sell(*, character: Character, item: Item):
    if item.character == character and item.container == Item.INVENTORY:
        item.delete()
        character.gold = F('gold') + item.template.value
        character.save()


def item_equip(*, character: Character, item: Item):
    if item.character == character and character.level >= item.level_requirement and item.container == Item.INVENTORY:
        try:
            equipped_item = character.items.get(
                container=Item.EQUIPMENT, template__type=item.type)
        except Item.DoesNotExist:
            equipped_item = None

        item.container = Item.EQUIPMENT

        if equipped_item:
            equipped_item.container = Item.INVENTORY
            equipped_item.save()
        item.save()


def item_unequip(*, character: Character, item: Item):
    if character.has_space and item.character == character and item.container == Item.EQUIPMENT:
        item.container = Item.INVENTORY
        item.save()
