from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context
from django.core import management
from tenants.models import Client


class Command(BaseCommand):
    help = 'Migrate only the relevant app for each tenant'

    def handle(self, *args, **kwargs):
        tenants = Client.objects.exclude(schema_name='public')

        for tenant in tenants:
            apps = tenant.get_tenant_apps()
            if not apps:
                continue

            self.stdout.write(f'\n--- Migrating {tenant.schema_name} ---')
            with schema_context(tenant.schema_name):
                for app in apps:
                    management.call_command(
                        'migrate', app,
                        '--database=default',
                        verbosity=1
                    )