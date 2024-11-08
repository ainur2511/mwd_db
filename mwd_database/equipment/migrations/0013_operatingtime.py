# Generated by Django 4.2 on 2023-09-26 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0012_remove_equipmenttype_vendor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperatingTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('circulation', models.IntegerField(max_length=999, verbose_name='Часы циркуляции за рейс')),
                ('meters', models.IntegerField(max_length=5000, verbose_name='Часы циркуляции за рейс')),
                ('screw_up', models.SmallIntegerField(max_length=10, verbose_name='Свинчиваний')),
                ('operating_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата/время добавления')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.equipment', verbose_name='Оборудование')),
            ],
        ),
    ]
