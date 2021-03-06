# Generated by Django 3.1.1 on 2020-10-08 20:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='APICredential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nonce', models.CharField(blank=True, max_length=200, null=True)),
                ('access_token', models.CharField(blank=True, max_length=200, null=True)),
                ('storefront_access_token', models.CharField(blank=True, max_length=200, null=True)),
                ('categories', models.CharField(blank=True, max_length=500, null=True)),
                ('scopes', models.CharField(blank=True, max_length=500, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True, unique=True)),
                ('storefront_endpoint', models.CharField(blank=True, max_length=200, null=True)),
                ('sales_channel_endpoint', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('display_name', models.CharField(max_length=30)),
                ('platform', models.ManyToManyField(through='dashboard.APICredential', to='dashboard.Platform')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_vendor', models.BooleanField(null=True)),
                ('email_pref', models.BooleanField(default=False)),
                ('sms_pref', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.vendor')),
            ],
        ),
        migrations.AddField(
            model_name='apicredential',
            name='platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.platform'),
        ),
        migrations.AddField(
            model_name='apicredential',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.vendor'),
        ),
        migrations.AlterUniqueTogether(
            name='apicredential',
            unique_together={('vendor', 'platform')},
        ),
    ]
