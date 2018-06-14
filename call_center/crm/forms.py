from django import forms
from .models import Call, Client
from users.models import User
import requests
from django.conf import settings


class EditCallForm(forms.ModelForm):

    class Meta:
        model = Call
        fields = ('type_task', 'description_task', 'executor_task', 'task_completed_identifier', 'client')


class EditClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('surname', 'name', 'patronymic', 'coment')


class ChoicePhoneForm(forms.ModelForm):

    phone_number_local = forms.ChoiceField(choices = [])

    def __init__(self, *args, **kwargs):
        super(ChoicePhoneForm, self).__init__(*args, **kwargs)
        self.fields['phone_number_local'].choices = free_phone_numbers()

    class Meta:
        model = User
        fields = ('phone_number_local',)


def lock_phone_numbers():
    lock_num =  User.objects.exclude(phone_number_local="")
    return [user.phone_number_local for user in lock_num]

def groups_phone_numbers():
    url = settings.GROUP_PHONE_NUMBER_URL
    phones_json = requests.get(url, verify=False).json()
    return phones_json[settings.NAME_GROUP_PHONE_NUMBER].split('-')

def free_phone_numbers():
    num = list(set(groups_phone_numbers()) - set(lock_phone_numbers()))
    return zip(num, num)