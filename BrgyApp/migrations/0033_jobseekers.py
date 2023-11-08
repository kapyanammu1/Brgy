# Generated by Django 4.2.3 on 2023-11-08 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BrgyApp', '0032_alter_household_house_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobSeekers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BrgyApp.resident')),
            ],
        ),
    ]
