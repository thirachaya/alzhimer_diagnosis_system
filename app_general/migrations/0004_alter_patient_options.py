# Generated by Django 5.1.1 on 2024-09-23 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_general', '0003_patient_patient_prefix_alter_patient_patient_idcard'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patient',
            options={'verbose_name': 'Patient', 'verbose_name_plural': 'Patients'},
        ),
    ]
