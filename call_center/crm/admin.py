from django.contrib import admin
from .models import Client, Call, LogCall

# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'surname', 'name', 'patronymic', ]
    list_filter = ['phone_number', 'surname', 'name', 'patronymic', ]


class CallAdmin(admin.ModelAdmin):
    list_display = ['date_call', 'disposition',
                    'client', 'login_name', 'executor_task']
    list_filter = ['date_call', 'disposition',
                   'client', 'login_name', 'executor_task']


class LogCallAdmin(admin.ModelAdmin):
    list_display = ['log_time', 'call', 'user_changed_record', ]
    list_filter = ['log_time', 'call', 'user_changed_record', ]


admin.site.register(Client, ClientAdmin)
admin.site.register(Call, CallAdmin)
admin.site.register(LogCall, LogCallAdmin)
