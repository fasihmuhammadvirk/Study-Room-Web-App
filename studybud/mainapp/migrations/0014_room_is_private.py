# Generated by Django 4.2.3 on 2024-03-29 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_rename_requested_participants_room_request_to_join_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]