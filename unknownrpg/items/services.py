from .models import ItemTemplate, Item

# Name or Item object?


def item_create(*, item_template: ItemTemplate) -> Item:
    item = Item(template=item_template, name=item_template.name)
    item.full_clean()
    item.save()
    return item


def item_shop_list():
    items = ItemTemplate.objects.filter(is_purchasable=True)
    return items
