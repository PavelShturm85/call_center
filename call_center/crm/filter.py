import django_filters
from .models import Call
from django.db import models
from django import forms
from django_filters import filters
from django.utils import timezone


class CallsFilter(django_filters.FilterSet):
    date_call = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(
        attrs={'placeholder': 'DD.MM.YYYY', 'type': 'date', }))

    class Meta:
        model = Call
        fields = ['date_call', 'client__phone_number', 'disposition', 'login_name', 'client__surname',
                  'client__name', 'client__patronymic', 'executor_task', 'task_completed_identifier']

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },

        }
