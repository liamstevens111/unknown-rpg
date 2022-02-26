from django.contrib import admin

from .models import Character
from items.models import Item


class ItemInline(admin.TabularInline):
    model = Item


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'level',
                    'current_xp', 'gold')
    list_display_links = ('name',)
    inlines = (ItemInline,)


admin.site.register(Character, CharacterAdmin)
