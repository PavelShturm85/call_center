# Generated by Django 2.0.5 on 2018-07-18 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_logcall_user_changed_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_number',
            field=models.CharField(max_length=12, unique=True, verbose_name='Номер телефона с которого звонили'),
        ),
    ]