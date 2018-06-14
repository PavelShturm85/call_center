from django.contrib import admin
from .models import Client, Call, LogCall

# Register your models here.
admin.site.register(Client)
admin.site.register(Call)
admin.site.register(LogCall)
