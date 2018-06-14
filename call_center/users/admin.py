from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
# admin.site.register(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('position', 'send_email',
                           'phone_number', 'phone_number_local')}),
    ) + UserAdmin.fieldsets
