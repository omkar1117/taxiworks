from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _

from django.contrib.auth.admin import UserAdmin as UAdmin
from user.models import User
# Register your models here.


class UserAdmin(UAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'mobile', 'avatar')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_provider', 'is_rider', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, UserAdmin)
