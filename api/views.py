from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import filters
from django.db import transaction
from datetime import datetime, date, timedelta
from django.utils.datastructures import MultiValueDictKeyError
import pytz
from api.models import *
import os
from login.helpers import login_status
from api.models import *


@api_view(['POST'])
def add_movies(request):
    try:
        flag, user_data = login_status(request)
        if flag:
            if user_data['user_type'] == "admin":
                with transaction.atomic():
                    for data in request.data:
                        print(data)
                        movie = Movie.objects.filter(name=data['name'])
                        if len(movie) > 0:
                            continue
                            # return Response(status=status.HTTP_409_CONFLICT,
                            #                 data={"message": f"Movie with name {data['name']} "
                            #                                  "already "
                            #                                  "exists.", "success": False})
                        else:
                            obj, created = Director.objects.get_or_create(name=data['director'])
                            data['director'] = obj
                            data['popularity'] = data.pop('99popularity')
                            genre_data = data.pop('genre')
                            movie = Movie.objects.create(**data)
                            for genre in genre_data:
                                obj, created = Genre.objects.get_or_create(name=genre)
                                MovieGenreRel.objects.create(movie_id=movie.id, genre_id=obj.id)
                    return Response(status=status.HTTP_201_CREATED, data={"message": "Movies created", 'success': True})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED,
                                data={"message": "Cannot access", "success": False})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED,
                            data={"message": "Invalid Tokens", "success": False})
    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={"message": "Invalid Token", "success": False})


@api_view(["DELETE"])
def delete_movies(request):
    try:
        flag, user_data = login_status(request)
        if flag:
            if user_data['user_type'] == "admin":
                data = request.data
                movie = Movie.objects.filter(name=data['name'])
                if len(movie) == 0:
                    return Response(status=status.HTTP_204_NO_CONTENT,
                                    data={"message": "No Movie present with this name",
                                          "success": True})
                else:
                    Movie.objects.filter(name=data['name']).delete()
                    return Response(status=status.HTTP_200_OK,
                                    data={"message": "Movie deleted successfully",
                                          "success": False})

            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED,
                                data={"message": "Cannot access", "success": False})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED,
                            data={"message": "Invalid Token", "success": False})
    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={"message": "Invalid Token", "success": False})


@api_view(['PUT'])
def edit_movie(request):
    try:
        flag, user_data = login_status(request)
        if flag:
            if user_data['user_type'] == "admin":
                data = request.data
                try:
                    movie = Movie.objects.get(name=data['name'])
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND,
                                    data={"message": "No movie with this name present", "success": False})
                else:
                    with transaction.atomic():
                        if 'genre' in data:
                            for genre in data['genre']:
                                obj, created = Genre.objects.get_or_create(name=genre.strip())
                                MovieGenreRel.objects.create(movie_id=movie.id, genre_id=obj.id)
                        if 'director' in data:
                            print(data)
                            obj, created = Director.objects.update_or_create(name=data['director'].strip())
                            movie.director = obj
                            print(data)
                        movie.imdb_score = data['imdb_score']
                        movie.popularity = data['99popularity']
                        movie.save()
                        return Response(status=status.HTTP_200_OK, data={"message": "Movie updated", "success": True})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED,
                                data={"message": "Cannot access", "success": False})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED,
                            data={"message": "Invalid Token", "success": False})

    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={"message": "Invalid Token", "success": False})


@api_view(["GET"])
def search_movies(request):
    movie = request.GET['search']
    if movie:
        matched_movies = Movie.objects.filter(Q(name__icontains=movie)).values(
            'name', 'imdb_score', 'popularity', 'director__name')
        if matched_movies:
            for movies in matched_movies:
                movie_obj = Movie.objects.get(name=movies['name'])
                genre_queryset = MovieGenreRel.objects.filter(movie_id=movie_obj.id).values()
                genre_list = list()
                for data in genre_queryset:
                    qs = Genre.objects.filter(id=data['genre_id']).values()
                    genre_list.append(qs[0]['name'])
                movies['genre'] = genre_list
                movies['99popularity'] = movies.pop('popularity')
                movies['director'] = movies.pop('director__name')

            return Response(status=status.HTTP_200_OK, data=matched_movies)
        else:
            return Response(status=status.HTTP_200_OK, data={"message": "No results found", "success": True})
    else:
        return Response(status.HTTP_400_BAD_REQUEST)
