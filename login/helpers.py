from functools import wraps
import jwt
from passlib.context import CryptContext
from login.models import *
from rest_framework import status
from rest_framework.response import Response

pwd_context = CryptContext(
    default="django_pbkdf2_sha256",
    schemes=["django_argon2", "django_bcrypt", "django_bcrypt_sha256",
             "django_pbkdf2_sha256", "django_pbkdf2_sha1",
             "django_disabled"])


def login_status(request):
    token = request.META.get('HTTP_IMDBAUTH')
    data = jwt.decode(token, 'imdb', algorithms=['HS256'])
    flag = UserDetail.objects.filter(email=data["email"],  user_type__name=data["user_type"]).count()
    if flag:
        return flag, data
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={"message": "Invalid Token", "success": False})

