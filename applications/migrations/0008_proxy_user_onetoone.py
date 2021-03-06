# Generated by Django 2.0.8 on 2018-11-01 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0007_application_proxy_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='proxy_user',
            field=models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='application_proxy', to=settings.AUTH_USER_MODEL),
        ),
    ]
