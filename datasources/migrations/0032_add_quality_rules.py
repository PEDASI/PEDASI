# Generated by Django 2.0.13 on 2019-04-10 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasources', '0031_default_connector_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='QualityCriterion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(default=1)),
                ('metadata_field', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='datasources.MetadataField')),
            ],
        ),
        migrations.CreateModel(
            name='QualityLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveSmallIntegerField()),
                ('threshold', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QualityRuleset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('short_name', models.CharField(blank=True, max_length=63, unique=True)),
                ('version', models.CharField(max_length=63)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='qualityruleset',
            unique_together={('name', 'version')},
        ),
        migrations.AddField(
            model_name='qualitylevel',
            name='ruleset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='levels', to='datasources.QualityRuleset'),
        ),
        migrations.AddField(
            model_name='qualitycriterion',
            name='quality_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criteria', to='datasources.QualityLevel'),
        ),
        migrations.AlterUniqueTogether(
            name='qualitylevel',
            unique_together={('ruleset', 'level')},
        ),
        migrations.AlterUniqueTogether(
            name='qualitycriterion',
            unique_together={('quality_level', 'metadata_field')},
        ),
    ]
