from enum import unique
from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from users.models import BaseUser
from users.services import user_create
from .forms import UserSignUpForm, UserEditForm


class CustomUserAdmin(UserAdmin):
    form = UserEditForm
    add_form = UserSignUpForm

    list_display = ('email', 'is_admin', 'is_active',
                    'is_staff', 'created_at', 'updated_at', 'character')
    list_select_related = ('character', )

    list_filter = ('is_active', 'is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Booleans', {'fields': ('is_active', 'is_admin')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')
                        }
         )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'character_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    readonly_fields = ("created_at", "updated_at")

admin.site.register(BaseUser, CustomUserAdmin)
admin.site.unregister(Group)
