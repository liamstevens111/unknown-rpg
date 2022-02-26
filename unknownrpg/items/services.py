from .models import ItemTemplate, Item
from characters.models import Character


def item_create(*, character: Character, item_template: ItemTemplate) -> Item:
    if character.has_space:
        item = Item(character=character, template=item_template,
                    name=item_template.name, container=Item.INVENTORY)
        item.full_clean()
        item.save()
        return item
    return None


def item_shop_list():
    items = ItemTemplate.objects.filter(is_purchasable=True)
    return items
