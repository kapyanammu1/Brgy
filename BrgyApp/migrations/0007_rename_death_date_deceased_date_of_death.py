# Generated by Django 4.2.3 on 2023-08-03 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BrgyApp', '0006_alter_household_house_no'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deceased',
            old_name='death_date',
            new_name='date_of_death',
        ),
    ]
