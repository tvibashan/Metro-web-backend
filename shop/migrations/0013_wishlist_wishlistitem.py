# Generated by Django 4.2.6 on 2024-01-10 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0012_alter_booking_product_thumbnail_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_category', models.CharField(choices=[('V', 'Ventrata'), ('T', 'Tour CMS'), ('B', 'Bokun'), ('W', 'Wave3'), ('G', 'GLT')], max_length=20)),
                ('product_id', models.CharField(max_length=255)),
                ('product_title', models.CharField(blank=True, max_length=255, null=True)),
                ('product_image', models.CharField(blank=True, max_length=255, null=True)),
                ('product_duration', models.CharField(blank=True, max_length=255, null=True)),
                ('product_location', models.CharField(blank=True, max_length=255, null=True)),
                ('product_price', models.CharField(blank=True, max_length=255, null=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishitems', to='shop.wishlist')),
            ],
        ),
    ]
