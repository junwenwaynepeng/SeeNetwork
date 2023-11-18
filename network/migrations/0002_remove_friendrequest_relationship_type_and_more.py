# Generated by Django 4.2.7 on 2023-11-17 03:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendrequest',
            name='relationship_type',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='relationship_type',
        ),
        migrations.AddField(
            model_name='relationship',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('confirm', 'confirm')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_relationships', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_relationships', to=settings.AUTH_USER_MODEL),
        ),
    ]