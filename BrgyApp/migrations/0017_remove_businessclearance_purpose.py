# Generated by Django 4.2.3 on 2023-08-19 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BrgyApp', '0016_business_citizenship'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessclearance',
            name='purpose',
        ),
    ]