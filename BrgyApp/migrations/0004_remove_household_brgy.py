# Generated by Django 4.2.3 on 2023-08-03 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BrgyApp', '0003_remove_solo_parent_resident_resident_pwd_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='household',
            name='brgy',
        ),
    ]
