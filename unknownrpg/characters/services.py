from django.db.models import F

from .models import Character

from items.services import item_create
from items.models import ItemTemplate, Item

from characters.models import CharacterEquipment, CharacterInventory

# Internal


def character_create(*, user: str, name: str) -> Character:
    character = Character(user=user, name=name, level=1, gold=0, current_xp=0)
    character.full_clean()
    character.save()


def item_add(*, character: Character, item_template: ItemTemplate):
    if character.has_space:
        item = item_create(item_template=item_template)
        character.inventory.add(item)
        return True
    return False


# Internal


def item_buy(*, character: Character, item_template: ItemTemplate):
    # Maybe can do some checks here for when/where the purchase is being made, ie shop ID parameter to ensure they are in correct location
    if item_template.is_purchasable and character.gold >= item_template.value:
        if item_add(character=character, item_template=item_template):
            character.gold = F('gold') - item_template.value
            # character.full_clean()
            character.save()


def item_sell(*, character: Character, item: Item):
    # This gets and deletes the ItemInventory relation at once, then deletes the Item

    # character.inventory.through.objects.get(item=item).item.delete()
    # CharacterInventory.objects.get(character=character, item=item).item.delete()
    CharacterInventory.objects.get(character=character, item=item).delete()
    item.delete()

    character.gold = F('gold') + item.template.value
    # character.full_clean()
    character.save()


def item_equip(*, character: Character, item: Item):
    character_inventory = CharacterInventory.objects.select_related(
        'item').get(character=character, item=item)

    if character.level < character_inventory.item.template.level_requirement:
        return

    try:
        character_equipment = CharacterEquipment.objects.select_related(
            'item').get(character=character, slot=character_inventory.item.template.type)
    except CharacterEquipment.DoesNotExist:
        character_equipment = None

    # Current no item equipped in that slot
    if not character_equipment:
        character_equipment = CharacterEquipment(
            character=character, item=character_inventory.item, slot=character_inventory.item.template.type)

        character_inventory.delete()
        character_equipment.full_clean()
        character_equipment.save()
    else:
        character_equipment_item = character_equipment.item
        character_equipment.item = character_inventory.item
        character_inventory.item = character_equipment_item

        character_equipment.full_clean()
        character_inventory.full_clean()
        character_equipment.save()
        character_inventory.save()


def item_unequip(*, character: Character, item: Item):
    # Not passing in slot for now, don't need to?
    if character.has_space:
        character_equipment = CharacterEquipment.objects.select_related(
            'item').get(character=character, item=item)

        character_inventory = CharacterInventory(
            character=character, item=character_equipment.item)
        character_equipment.delete()
        character_inventory.full_clean()
        character_inventory.save()
