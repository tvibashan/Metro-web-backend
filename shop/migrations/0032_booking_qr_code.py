# Generated by Django 4.2.6 on 2024-03-24 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_remove_booking_option_name_participant_option_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='images/qr_code/'),
        ),
    ]
