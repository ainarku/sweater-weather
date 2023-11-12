# Generated by Django 4.2.6 on 2023-11-12 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sweatherapp', '0005_remove_weatherdata_lat_remove_weatherdata_lon_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='weatherdata',
            name='temperature_unit',
            field=models.CharField(choices=[('C', 'Celsius'), ('F', 'Fahrenheit')], default='C', max_length=1),
        ),
    ]