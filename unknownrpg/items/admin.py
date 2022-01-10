from django.contrib import admin

from .models import Item, ItemTemplate


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level_requirement', 'min_damage',
                    'max_damage', 'min_armour', 'max_armour', 'value', 'type')
    list_display_links = ('name',)


admin.site.register(ItemTemplate, ItemAdmin)
admin.site.register(Item, ItemAdmin)
