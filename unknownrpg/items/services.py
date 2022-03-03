from .models import ItemTemplate, Item
from characters.models import Character

from django.core.exceptions import ValidationError

CHARACTER_NO_INVENTORY_SPACE = 'Character inventory is full'


def item_create(*, character: Character, item_template: ItemTemplate) -> Item:
    if not character.has_space:
        raise ValidationError(CHARACTER_NO_INVENTORY_SPACE)

    item = Item(character=character, template=item_template,
                name=item_template.name, container=Item.INVENTORY)
    item.full_clean()
    item.save()

    return item


def item_shop_list():
    items = ItemTemplate.objects.filter(is_purchasable=True)
    return items
