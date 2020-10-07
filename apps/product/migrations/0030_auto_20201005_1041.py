# Generated by Django 3.1.1 on 2020-10-05 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_auto_20201005_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sizeguideitem',
            name='attribute',
        ),
        migrations.AddField(
            model_name='sizeguideitem',
            name='attribute',
            field=models.ManyToManyField(to='product.Attribute'),
        ),
        migrations.RemoveField(
            model_name='sizeguideitem',
            name='size',
        ),
        migrations.AddField(
            model_name='sizeguideitem',
            name='size',
            field=models.ManyToManyField(to='product.Size'),
        ),
    ]