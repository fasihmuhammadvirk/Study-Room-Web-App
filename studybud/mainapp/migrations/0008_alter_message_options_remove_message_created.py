# Generated by Django 4.2.3 on 2024-03-21 14:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0007_alter_message_bodyimage"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="message",
            options={},
        ),
        migrations.RemoveField(
            model_name="message",
            name="created",
        ),
    ]
