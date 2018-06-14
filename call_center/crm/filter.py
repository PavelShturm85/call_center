import django_filters
from .models import Call
from django.db import models
from django import forms
from django_filters import filters

class CallsFilter(django_filters.FilterSet):
    class Meta:
        model = Call
        fields = ['date_call', 'client__phone_number', 'disposition', 'login_name', 'client__surname', 'executor_task', 'task_completed_identifier'] 
        filters.LOOKUP_TYPES = [
            ('lte', 'До'), 
            ('gte', 'От'),
        ]
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.DateTimeField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                    'lookup_expr': ['lte', 'gte'],
                    'widget': forms.DateInput(format='%d.%m.%Y'),
                },
            },
        }
