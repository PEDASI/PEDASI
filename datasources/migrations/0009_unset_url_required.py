# Generated by Django 2.0.8 on 2018-10-29 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasources', '0008_datasource__connector_string'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasource',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
