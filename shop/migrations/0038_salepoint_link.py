# Generated by Django 4.2.6 on 2024-05-07 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0037_overviewcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='salepoint',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
