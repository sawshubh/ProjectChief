from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display  = [
        'title', 'director', 'original_language',
        'imdb_rating', 'vote_average', 'status', 'release_date'
    ]
    list_filter   = ['status', 'original_language']
    search_fields = ['title', 'original_title', 'director', 'imdb_id']
    readonly_fields = ['created_at', 'updated_at']
    ordering      = ['-imdb_rating']

    fieldsets = [
        ('Basic Info', {
            'fields': [
                'title', 'original_title', 'overview',
                'tagline', 'status', 'release_date', 'runtime'
            ]
        }),
        ('Language', {
            'fields': ['original_language', 'spoken_languages']
        }),
        ('Ratings', {
            'fields': [
                'imdb_id', 'imdb_rating', 'imdb_votes',
                'vote_average', 'vote_count', 'popularity'
            ]
        }),
        ('Financials', {
            'fields': ['budget', 'revenue']
        }),
        ('Media', {
            'fields': ['poster_path', 'trailer_url']
        }),
        ('Cast & Crew', {
            'fields': [
                'director', 'director_of_photography',
                'music_composer', 'cast', 'writers',
                'producers'
            ]
        }),
        ('Production', {
            'fields': ['genres', 'production_companies', 'production_countries']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at']
        }),
    ]