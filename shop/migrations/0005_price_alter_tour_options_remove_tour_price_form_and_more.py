# Generated by Django 4.2.6 on 2024-01-07 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_category_day_priceform_tour_tourschedule_tourimage_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AlterModelOptions(
            name='tour',
            options={'verbose_name': 'Tour', 'verbose_name_plural': 'Tours'},
        ),
        migrations.RemoveField(
            model_name='tour',
            name='price_form',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='tour_schedule',
        ),
        migrations.DeleteModel(
            name='PriceForm',
        ),
        migrations.AddField(
            model_name='price',
            name='tour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='shop.tour'),
        ),
    ]
