# Generated by Django 3.1.1 on 2020-10-06 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_auto_20201006_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sms_pref',
            field=models.BooleanField(default=False),
        ),
    ]