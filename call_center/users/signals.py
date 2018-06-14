from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.conf import settings
from .models import User


@receiver(user_logged_out)
def del_used_phone(user, **kwargs):
    logout_user = User.objects.get(username=user)
    logout_user.phone_number_local = ''
    logout_user.save()
