# Generated by Django 2.0.5 on 2018-05-30 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20180530_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='call',
            name='groups_phone_numbers',
        ),
    ]
