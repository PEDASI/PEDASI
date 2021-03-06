import logging

from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError


logger = logging.getLogger(__name__)


class ProfilesConfig(AppConfig):
    name = 'profiles'

    @staticmethod
    def create_groups():
        """
        Create the necessary groups for Application and Data Source managers.
        """
        from django.contrib.auth.models import Group, Permission

        app_providers, created = Group.objects.get_or_create(
            name='Application Providers',
        )
        app_providers.permissions.add(
            Permission.objects.get(codename='add_application'),
            Permission.objects.get(codename='change_application'),
            Permission.objects.get(codename='delete_application')
        )

        data_providers, created = Group.objects.get_or_create(
            name='Data Providers',
        )
        data_providers.permissions.add(
            Permission.objects.get(codename='add_datasource'),
            Permission.objects.get(codename='change_datasource'),
            Permission.objects.get(codename='delete_datasource'),
        )

        try:
            data_providers.permissions.add(
                Permission.objects.get(codename='add_licence'),
                Permission.objects.get(codename='change_licence'),
                Permission.objects.get(codename='delete_licence')
            )

        except Permission.DoesNotExist:
            logger.warning('Licence permissions not found - please restart Django server')

    def ready(self):
        # Runs after app registry is populated - i.e. all models exist and are importable
        try:
            self.create_groups()
            logging.info('Loaded inline Group fixtures')

        except (OperationalError, ProgrammingError):
            logging.warning('Could not create Group fixtures, database has not been initialized')
