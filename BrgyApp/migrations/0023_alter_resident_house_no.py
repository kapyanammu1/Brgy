# Generated by Django 4.2.3 on 2023-08-20 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BrgyApp', '0022_alter_resident_house_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='house_no',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='BrgyApp.household'),
            preserve_default=False,
        ),
    ]
