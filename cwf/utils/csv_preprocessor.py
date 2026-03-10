import csv
import json
import os
import re

def parse_list_field(value):
    if not value or value.strip() == '':
        return '[]'
    items = [item.strip() for item in value.split(',') if item.strip()]
    return json.dumps(items)


def parse_int(value):
    try:
        return str(int(float(value))) if value and value.strip() else ''
    except (ValueError, TypeError):
        return ''


def parse_decimal(value):
    try:
        return str(float(value)) if value and value.strip() else ''
    except (ValueError, TypeError):
        return ''


def is_spam(title):
    # skip rows with phone numbers, URLs, emojis, special unicode
    if re.search(r'\+\d[\d\s\-\(\)]{7,}', title):  # phone numbers
        return True
    if re.search(r'http|www|\.com|\.net', title, re.IGNORECASE):  # URLs
        return True
    if re.search(r'[\U00010000-\U0010ffff]', title):  # special unicode/emojis
        return True
    return False


def preprocess_csv(input_path, output_path):
    """
    Reads raw IMDB CSV and writes a cleaned CSV
    ready for PostgreSQL COPY command.
    """

    # Must match exact column order of cinex360_movie table
    output_columns = [
        'imdb_id',
        'title',
        'original_title',
        'overview',
        'tagline',
        'status',
        'release_date',
        'runtime',
        'original_language',
        'spoken_languages',
        'budget',
        'revenue',
        'vote_average',
        'vote_count',
        'imdb_rating',
        'imdb_votes',
        'popularity',
        'poster_path',
        'trailer_url',
        'genres',
        'cast',
        'director',
        'director_of_photography',
        'writers',
        'producers',
        'music_composer',
        'production_companies',
        'production_countries',
        'created_at',
        'updated_at',
    ]

    print(f'Preprocessing {input_path}...')
    row_count = 0
    error_count = 0

    with open(input_path, encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8', newline='') as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=output_columns)
        writer.writeheader()

        for line_num, row in enumerate(reader, start=2):
            try:
                title = row.get('title', '').strip()
                original_title = row.get('original_title', '').strip()
                title = title or original_title

                if not title or is_spam(title):
                    error_count += 1
                    continue

                imdb_rating = parse_decimal(row.get('imdb_rating'))
                if not imdb_rating:
                    error_count += 1
                    continue

                writer.writerow({
                    'imdb_id': row.get('imdb_id', '').strip() or '',
                    'title': row.get('title', '').strip(),
                    'original_title': row.get('original_title', '').strip() or '',
                    'overview': row.get('overview', '').strip() or '',
                    'tagline': row.get('tagline', '').strip() or '',
                    'status': row.get('status', 'Released').strip() or 'Released',
                    'release_date': row.get('release_date', '').strip() or '',
                    'runtime': parse_int(row.get('runtime')),
                    'original_language': row.get('original_language', '').strip() or '',
                    'spoken_languages': parse_list_field(row.get('spoken_languages', '')),
                    'budget': parse_int(row.get('budget')),
                    'revenue': parse_int(row.get('revenue')),
                    'vote_average': parse_decimal(row.get('vote_average')),
                    'vote_count': parse_int(row.get('vote_count')),
                    'imdb_rating': parse_decimal(row.get('imdb_rating')),
                    'imdb_votes': parse_int(row.get('imdb_votes')),
                    'popularity': parse_decimal(row.get('popularity')),
                    'poster_path': row.get('poster_path', '').strip() or '',
                    'trailer_url': row.get('trailer_url', '').strip() or '',
                    'genres': parse_list_field(row.get('genres', '')),
                    'cast': parse_list_field(row.get('cast', '')),
                    'director': row.get('director', '').strip() or '',
                    'director_of_photography': row.get('director_of_photography', '').strip() or '',
                    'writers': parse_list_field(row.get('writers', '')),
                    'producers': parse_list_field(row.get('producers', '')),
                    'music_composer': row.get('music_composer', '').strip() or '',
                    'production_companies': parse_list_field(row.get('production_companies', '')),
                    'production_countries': parse_list_field(row.get('production_countries', '')),
                    'created_at': 'NOW()',
                    'updated_at': 'NOW()',
                })
                row_count += 1

                if row_count % 100000 == 0:
                    print(f'Preprocessed {row_count} rows...')

            except Exception as e:
                error_count += 1
                print(f'Line {line_num} error: {str(e)}')

    print('\nPreprocessing complete!')
    print(f'Success: {row_count} rows')
    print(f'Errors: {error_count} rows')
    print(f'Output: {output_path}')

    return output_path