# Generated by Django 4.0.1 on 2022-01-12 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_api', '0001_initial'),
        ('chat_api', '0002_message_room_alter_message_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_room', to='ticket_api.ticket'),
        ),
    ]