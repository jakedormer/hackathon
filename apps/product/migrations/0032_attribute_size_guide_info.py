# Generated by Django 3.1.1 on 2020-10-05 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_auto_20201005_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='size_guide_info',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
    ]
