# Generated by Django 3.1.1 on 2020-09-08 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_product_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='code',
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
