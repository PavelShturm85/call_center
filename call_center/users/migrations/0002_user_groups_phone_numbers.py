# Generated by Django 2.0.5 on 2018-05-30 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='groups_phone_numbers',
            field=models.CharField(blank=True, choices=[('0070', '0070'), ('0071', '0071'), ('0072', '0072'), ('0073', '0073'), ('0074', '0074')], max_length=4, null=True, verbose_name='Номер телефона оператора'),
        ),
    ]
