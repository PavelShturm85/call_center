# Generated by Django 2.0.5 on 2018-06-04 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180530_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number_local',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Внутренний номер'),
        ),
    ]
