# Generated by Django 4.2 on 2023-09-26 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0015_alter_operatingtime_meters'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operatingtime',
            old_name='equipment',
            new_name='equipment_type',
        ),
    ]