# Generated by Django 2.0.8 on 2018-09-25 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasources', '0005_datasource_plugin_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasource',
            name='users_group',
            field=models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='users_group_requested',
            field=models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='auth.Group'),
        ),
    ]
