# Generated by Django 3.1.1 on 2020-10-07 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0034_auto_20201006_1722'),
    ]

    operations = [
        migrations.RenameField(
            model_name='size',
            old_name='value',
            new_name='name',
        ),
    ]
