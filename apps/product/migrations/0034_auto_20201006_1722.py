# Generated by Django 3.1.1 on 2020-10-06 17:22

from django.db import migrations


class Migration(migrations.Migration):

    atomic = False
    dependencies = [
        ('product', '0033_auto_20201005_1915'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='id',
            new_name='external_id',
        ),
    ]