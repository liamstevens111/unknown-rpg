from django.contrib import admin

from .models import Item, ItemTemplate


class ItemTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level_requirement', 'min_damage',
                    'max_damage', 'min_armour', 'max_armour', 'value', 'type', 'is_purchasable')
    list_display_links = ('name',)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level_requirement', 'min_damage',
                    'max_damage', 'min_armour', 'max_armour', 'value', 'type', 'template')
    list_display_links = ('name',)


admin.site.register(ItemTemplate, ItemTemplateAdmin)
admin.site.register(Item)
