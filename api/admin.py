from django.contrib import admin
from api.models import *

# Register your models here.

admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(MovieGenreRel)
