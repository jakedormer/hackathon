# Generated by Django 3.1.1 on 2020-09-20 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_auto_20200917_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeOptionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='sizeguide',
            name='name',
            field=models.CharField(default='hi', max_length=100),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AttributeOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=255)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.attributeoptiongroup')),
            ],
        ),
        migrations.AddField(
            model_name='attribute',
            name='option_group',
            field=models.ForeignKey(blank=True, help_text='Select an option group if using type "Option" or "Multi Option"', null=True, on_delete=django.db.models.deletion.CASCADE, to='product.attributeoptiongroup', verbose_name='Option Group'),
        ),
    ]
