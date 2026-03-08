import os
from django.core.management.base import BaseCommand
from cwf.utils.csv_importer import import_movies_csv


class Command(BaseCommand):
    help = 'Import movies from CSV into cinex360 tenant'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Full path to the CSV file')
        parser.add_argument('--schema', type=str, default='cinex360', help='Tenant schema name')
        parser.add_argument('--batch', type=int, default=1000, help='Batch size')

    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv_path']
        schema_name = kwargs['schema']
        batch_size = kwargs['batch']

        if not os.path.exists(csv_path):
            self.stderr.write(f'File not found: {csv_path}')
            return

        self.stdout.write(f'Starting import from {csv_path}')
        self.stdout.write(f'Schema: {schema_name} | Batch size: {batch_size}')

        result = import_movies_csv(csv_path, schema_name, batch_size)

        self.stdout.write(f'\n--- Import Complete ---')
        self.stdout.write(f'Success : {result["success"]} rows')
        self.stdout.write(f'Errors  : {result["errors"]} rows')

        if result['details']:
            self.stdout.write('\nFirst 20 errors:')
            for err in result['details']:
                self.stderr.write(err)