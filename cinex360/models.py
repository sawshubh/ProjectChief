from django.db import models
from cwf.models import BaseModel


class Movie(BaseModel):
    STATUS_CHOICES = [
        ('Released', 'Released'),
        ('Post Production', 'Post Production'),
        ('In Production', 'In Production'),
        ('Planned', 'Planned'),
        ('Canceled', 'Canceled'),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('mr', 'Marathi'),
        ('fr', 'French'),
        ('es', 'Spanish'),
        ('ja', 'Japanese'),
        ('ko', 'Korean'),
        ('fi', 'Finnish'),
        ('other', 'Other'),
    ]

    imdb_id = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    original_title = models.CharField(max_length=255, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    tagline = models.CharField(max_length=500, null=True, blank=True)
    status  = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Released')
    release_date = models.CharField(max_length=20, null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    original_language  = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    spoken_languages = models.JSONField(default=list, blank=True)
    budget  = models.BigIntegerField(null=True, blank=True)
    revenue = models.BigIntegerField(null=True, blank=True)
    vote_average = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)
    imdb_rating  = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, db_index=True)
    imdb_votes = models.IntegerField(null=True, blank=True)
    popularity = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, db_index=True)
    poster_path  = models.CharField(max_length=255, null=True, blank=True)
    trailer_url  = models.URLField(null=True, blank=True)
    genres = models.JSONField(default=list, blank=True)
    cast = models.JSONField(default=list, blank=True)
    producers  = models.JSONField(default=list, blank=True)
    writers  = models.JSONField(default=list, blank=True)
    production_companies  = models.JSONField(default=list, blank=True)
    production_countries  = models.JSONField(default=list, blank=True)
    director = models.TextField(null=True, blank=True, db_index=True)
    director_of_photography = models.TextField(null=True, blank=True)
    music_composer = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering  = ['-imdb_rating']
        indexes = [
            models.Index(fields=['imdb_rating', 'popularity']),
            models.Index(fields=['status', 'original_language']),
        ]