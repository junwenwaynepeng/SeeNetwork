# Generated by Django 4.2.7 on 2023-11-28 08:21

from django.db import migrations
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_essentialskill_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essentialskill',
            name='description',
            field=martor.models.MartorField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='selfdefinedcontent',
            name='content',
            field=martor.models.MartorField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='selfintroduction',
            name='self_introduction',
            field=martor.models.MartorField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='detail',
            field=martor.models.MartorField(blank=True, null=True),
        ),
    ]
