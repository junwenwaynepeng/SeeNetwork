# Generated by Django 4.2.7 on 2023-11-27 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_privatesetting_display_cv_profilepagesetting_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilepagesetting',
            name='use_custom_page',
            field=models.BooleanField(default=False),
        ),
    ]
