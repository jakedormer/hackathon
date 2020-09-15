# Generated by Django 3.1.1 on 2020-09-06 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_apicredential_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='name',
            field=models.CharField(choices=[('shopify', 'Shopify'), ('woocommerce', 'WooCommerce')], max_length=30, null=True, unique=True),
        ),
    ]