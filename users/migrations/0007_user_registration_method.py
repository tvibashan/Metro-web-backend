# Generated by Django 5.0 on 2023-12-11 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_userprofile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='registration_method',
            field=models.CharField(choices=[('email', 'Email'), ('google', 'Google')], default='email', max_length=10),
        ),
    ]
