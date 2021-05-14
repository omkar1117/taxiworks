from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.admin import UserAdmin as UAdmin
from user.models import User, Otp, UserAddress, Address
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


class OTPAdmin(admin.ModelAdmin):
    model = Otp
    fields = ('__all__',)


class UserAddressAdmin(admin.ModelAdmin):
    model = UserAddress
    fields = ('user', 'address')


class AddressAdmin(admin.ModelAdmin):
    model = Address
    fields = ('address', 'state', 'postal_code', 'city',)


admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Otp, OTPAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
