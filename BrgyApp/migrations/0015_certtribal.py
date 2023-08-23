# Generated by Django 4.2.3 on 2023-08-18 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BrgyApp', '0014_rename_certindegency_certindigency'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertTribal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tribe', models.CharField(max_length=100)),
                ('purpose', models.CharField(max_length=100)),
                ('clearance_type', models.CharField(max_length=100)),
                ('or_no', models.CharField(max_length=50)),
                ('or_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('or_date', models.DateField()),
                ('ctc', models.CharField(max_length=50)),
                ('ctc_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ctc_date', models.DateField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('mother', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mother', to='BrgyApp.resident')),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resident', to='BrgyApp.resident')),
            ],
        ),
    ]