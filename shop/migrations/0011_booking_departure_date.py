# Generated by Django 4.2.6 on 2024-01-10 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_participant_participant_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='departure_date',
            field=models.DateTimeField(blank=True, max_length=255, null=True),
        ),
    ]
