# Generated by Django 3.1 on 2020-08-30 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0012_auto_20200830_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='slug',
            field=models.SlugField(default='.s>borDo.gimoal', unique=True),
        ),
    ]
