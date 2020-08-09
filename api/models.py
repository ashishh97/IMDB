from django.db import models

# Create your models here.


class Director(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'director'


class Genre(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'genre'


class Movie(models.Model):
    name = models.CharField(max_length=200)
    popularity = models.FloatField()
    imdb_score = models.FloatField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie'


class MovieGenreRel(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_genre_rel'
