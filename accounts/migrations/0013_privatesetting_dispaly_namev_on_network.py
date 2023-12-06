# Generated by Django 4.2.7 on 2023-12-05 07:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_customuser_skype_remove_customuser_snapchat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatesetting',
            name='dispaly_namev_on_network',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)]),
        ),
    ]