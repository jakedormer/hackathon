# Generated by Django 3.1.1 on 2020-09-21 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_auto_20200915_1642'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apicredential',
            old_name='password',
            new_name='nonce',
        ),
        migrations.RemoveField(
            model_name='apicredential',
            name='username',
        ),
    ]
