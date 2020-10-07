# Generated by Django 3.1.1 on 2020-10-05 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0028_auto_20201002_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sizeguideitem',
            name='attribute',
        ),
        migrations.AddField(
            model_name='sizeguideitem',
            name='attribute',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.attribute'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='sizeguideitem',
            name='size',
        ),
        migrations.AddField(
            model_name='sizeguideitem',
            name='size',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.size'),
            preserve_default=False,
        ),
    ]