from django.db.models import F
from django.core.exceptions import ValidationError

from .models import Character

from items.services import item_create
from items.models import ItemTemplate, Item

ITEM_NOT_PURCHASABLE = '{item} is not purchasable'
CHARACTER_NO_INVENTORY_SPACE = 'Character inventory is full'
CHARACTER_ITEM_PURCHASE_INSUFFICIENT_GOLD = '{gold} is required to purchase {item}'
CHARACTER_ITEM_EQUIP_INSUFFICIENT_LEVEL = 'level {item_level} is required to equip {item}'
CHARACTER_INVENTORY_ITEM_NOT_PRESENT = '{item} does not exist in inventory'
CHARACTER_EQUIPMENT_ITEM_NOT_PRESENT = '{item} not currently equipped'


def character_create(*, user: str, name: str) -> Character:
    character = Character(user=user, name=name)

    character.level = 1
    character.gold = 0
    character.current_xp = 0

    character.full_clean()
    character.save()


def character_list_equipment(*, character: Character):
    return character.items.filter(container='equipment')


def character_list_inventory(*, character: Character):
    return character.items.filter(container='inventory')


def has_item(*, character: Character, item: Item, container):
    return item.character == character and item.container == container


def item_buy(*, character: Character, item_template: ItemTemplate):
    if not item_template.is_purchasable:
        raise ValidationError(ITEM_NOT_PURCHASABLE.format(item=item_template))

    if not character.gold >= item_template.value:
        raise ValidationError(CHARACTER_ITEM_PURCHASE_INSUFFICIENT_GOLD.format(
            gold=item_template.value, item=item_template))

    item_create(character=character, item_template=item_template)
    character.gold = F('gold') - item_template.value
    character.save()


def item_sell(*, character: Character, item: Item):
    if not has_item(character=character, item=item, container=Item.INVENTORY):
        raise ValidationError(
            CHARACTER_INVENTORY_ITEM_NOT_PRESENT.format(item=item))

    item.delete()
    character.gold = F('gold') + item.template.value
    character.save()


def item_equip(*, character: Character, item: Item):
    if not character.level >= item.level_requirement:
        raise ValidationError(CHARACTER_ITEM_EQUIP_INSUFFICIENT_LEVEL.format(
            item_level=item.level_requirement, item=item))

    if not has_item(character=character, item=item, container=Item.INVENTORY):
        raise ValidationError(
            CHARACTER_INVENTORY_ITEM_NOT_PRESENT.format(item=item))

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
    if not has_item(character=character, item=item, container=Item.EQUIPMENT):
        raise ValidationError(
            CHARACTER_EQUIPMENT_ITEM_NOT_PRESENT.format(item=item))

    if not character.has_space:
        raise ValidationError(CHARACTER_NO_INVENTORY_SPACE)

    item.container = Item.INVENTORY
    item.save()
