# Generated by Django 3.1.2 on 2020-11-21 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_vendor_free_shipping'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='api_access_token',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='platform',
        ),
        migrations.AddField(
            model_name='vendor',
            name='platform',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.platform'),
        ),
        migrations.DeleteModel(
            name='APICredential',
        ),
    ]
