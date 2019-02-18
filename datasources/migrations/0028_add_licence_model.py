# Generated by Django 2.0.8 on 2019-01-30 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasources', '0027_add_push_granted'),
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('short_name', models.CharField(blank=True, max_length=63)),
                ('version', models.CharField(max_length=63)),
                ('url', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='license',
            unique_together={('name', 'version')},
        ),
        migrations.AddField(
            model_name='datasource',
            name='license',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='datasources', to='datasources.License'),
        ),
    ]