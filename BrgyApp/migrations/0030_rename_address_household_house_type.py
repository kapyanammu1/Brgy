# Generated by Django 4.2.3 on 2023-10-26 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BrgyApp', '0029_rename_house_type_household_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='household',
            old_name='address',
            new_name='house_type',
        ),
    ]
