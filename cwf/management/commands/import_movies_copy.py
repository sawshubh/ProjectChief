import os
from django.core.management.base import BaseCommand
from django.db import connection
from django_tenants.utils import schema_context
from cwf.utils.csv_preprocessor import preprocess_csv


class Command(BaseCommand):
    help = 'Import movies using PostgreSQL COPY — fastest method'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to raw CSV file')
        parser.add_argument('--schema', type=str, default='cinex360', help='Tenant schema')
        parser.add_argument('--skip-preprocess', action='store_true', help='Skip preprocessing if already done')

    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv_path']
        schema_name = kwargs['schema']
        skip_preprocess = kwargs['skip_preprocess']

        if not os.path.exists(csv_path):
            self.stderr.write(f'File not found: {csv_path}')
            return

        # Step 1 — Preprocess
        cleaned_path = csv_path.replace('.csv', '_cleaned.csv')

        if not skip_preprocess:
            self.stdout.write('Step 1 — Preprocessing CSV...')
            preprocess_csv(csv_path, cleaned_path)
        else:
            self.stdout.write('Skipping preprocessing...')
            cleaned_path = csv_path

        # Step 2 — PostgreSQL COPY
        self.stdout.write('\nStep 2 — Loading into PostgreSQL...')

        with schema_context(schema_name):
            with connection.cursor() as cursor:

                # Clear existing data
                cursor.execute('TRUNCATE Table cinex360_movie;')
                self.stdout.write('Cleared existing data...')

                # Reset sequence
                cursor.execute("SELECT setval(pg_get_serial_sequence('cinex360_movie', 'id'), 1, false);")

                # COPY command
                copy_sql = f"""
                    COPY cinex360_movie (
                        imdb_id, title, original_title, overview, tagline,
                        status, release_date, runtime, original_language,
                        spoken_languages, budget, revenue, vote_average,
                        vote_count, imdb_rating, imdb_votes, popularity,
                        poster_path, trailer_url, genres, "cast", director,
                        director_of_photography, writers, producers,
                        music_composer, production_companies,
                        production_countries, created_at, updated_at
                    )
                    FROM '{cleaned_path.replace(os.sep, '/')}'
                    WITH (
                        FORMAT csv,
                        HEADER true,
                        NULL '',
                        ENCODING 'UTF8'
                    );
                """

                cursor.execute(copy_sql)
                count = cursor.rowcount
                self.stdout.write(f'Loaded {count} rows!')

        self.stdout.write('\n--- Import Complete ---')
        self.stdout.write(f'Schema : {schema_name}')
        self.stdout.write(f'Rows   : {count}')