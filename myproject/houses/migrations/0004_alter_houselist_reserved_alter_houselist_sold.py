# Generated by Django 4.2.7 on 2023-11-09 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0003_rename_reserved_houselist_reserved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='houselist',
            name='reserved',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='houselist',
            name='sold',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
