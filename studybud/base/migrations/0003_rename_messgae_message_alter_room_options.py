# Generated by Django 4.2.3 on 2024-03-05 13:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("base", "0002_topic_room_host_messgae_room_topic"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Messgae",
            new_name="Message",
        ),
        migrations.AlterModelOptions(
            name="room",
            options={"ordering": ["-updated", "-created"]},
        ),
    ]