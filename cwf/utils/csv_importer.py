import csv
import json
from django.db import connection


def parse_list_field(value):
    """Convert comma separated string to clean list."""
    if not value or value.strip() == "":
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_int(value):
    try:
        return int(float(value)) if value and value.strip() else None
    except (ValueError, TypeError):
        return None


def parse_decimal(value):
    try:
        return float(value) if value and value.strip() else None
    except (ValueError, TypeError):
        return None


def import_movies_csv(file_path, schema_name, batch_size=1000):
    """
    Import movies from CSV into a specific tenant schema.
    Returns a dict with success count, error count and errors.
    """
    from django_tenants.utils import schema_context
    from cinex360.models import Movie

    success_count = 0
    error_count = 0
    errors = []
    batch = []

    with schema_context(schema_name):
        # Clear existing data before import
        Movie.objects.all().delete()

        with open(file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for line_num, row in enumerate(reader, start=2):
                try:
                    movie = Movie(
                        imdb_id=row.get("imdb_id", "").strip() or None,
                        title=row.get("title", "").strip(),
                        original_title=row.get("original_title", "").strip() or None,
                        overview=row.get("overview", "").strip() or None,
                        tagline=row.get("tagline", "").strip() or None,
                        status=row.get("status", "Released").strip() or "Released",
                        release_date=row.get("release_date", "").strip() or None,
                        runtime=parse_int(row.get("runtime")),
                        original_language=row.get("original_language", "").strip()
                        or None,
                        spoken_languages=parse_list_field(
                            row.get("spoken_languages", "")
                        ),
                        budget=parse_int(row.get("budget")),
                        revenue=parse_int(row.get("revenue")),
                        vote_average=parse_decimal(row.get("vote_average")),
                        vote_count=parse_int(row.get("vote_count")),
                        imdb_rating=parse_decimal(row.get("imdb_rating")),
                        imdb_votes=parse_int(row.get("imdb_votes")),
                        popularity=parse_decimal(row.get("popularity")),
                        poster_path=row.get("poster_path", "").strip() or None,
                        genres=parse_list_field(row.get("genres", "")),
                        cast=parse_list_field(row.get("cast", "")),
                        director=row.get("director", "").strip() or None,
                        director_of_photography=row.get(
                            "director_of_photography", ""
                        ).strip()
                        or None,
                        writers=parse_list_field(row.get("writers", "")),
                        producers=parse_list_field(row.get("producers", "")),
                        music_composer=row.get("music_composer", "").strip() or None,
                        production_companies=parse_list_field(
                            row.get("production_companies", "")
                        ),
                        production_countries=parse_list_field(
                            row.get("production_countries", "")
                        ),
                    )
                    batch.append(movie)
                    success_count += 1

                    # Insert in batches
                    if len(batch) >= batch_size:
                        Movie.objects.bulk_create(batch, ignore_conflicts=True)
                        batch = []
                        print(f"Inserted {success_count} rows...")

                except Exception as e:
                    error_count += 1
                    errors.append(f"Line {line_num}: {str(e)}")

            # Insert remaining rows
            if batch:
                Movie.objects.bulk_create(batch, ignore_conflicts=True)
                print(f"Inserted {success_count} rows...")

    return {
        "success": success_count,
        "errors": error_count,
        "details": errors[:20],  # only return first 20 errors
    }
