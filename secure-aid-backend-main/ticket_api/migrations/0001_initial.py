# Generated by Django 4.0.1 on 2022-01-11 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Medical', 'Medical'), ('Legal', 'Legal'), ('Finacial', 'Finacial')], max_length=255)),
                ('need_by_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Awaiting', 'Awaiting'), ('In-Progess', 'In-Progess'), ('Complete', 'Complete')], default='Awaiting', max_length=255)),
                ('sponsor_comments', models.TextField(blank=True, null=True)),
                ('provider_comments', models.TextField(blank=True, null=True)),
                ('aid_provider_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Provider_in_Ticket', to=settings.AUTH_USER_MODEL)),
                ('aid_recipient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Recipient_in_Ticket', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]