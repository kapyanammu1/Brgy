# Generated by Django 4.2.3 on 2023-10-26 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BrgyApp', '0031_rename_house_type_household_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='house_no',
            field=models.CharField(max_length=100),
        ),
    ]
