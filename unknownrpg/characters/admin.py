from django.contrib import admin

from .models import CharacterInventory, CharacterEquipment, Character


class CharacterEquipmentInline(admin.TabularInline):
    model = CharacterEquipment
    # extra = 1


class CharacterInventoryInline(admin.TabularInline):
    model = CharacterInventory
    extra = 1


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'level',
                    'current_xp', 'gold')
    list_display_links = ('name',)
    inlines = (CharacterEquipmentInline, CharacterInventoryInline,)


admin.site.register(Character, CharacterAdmin)
