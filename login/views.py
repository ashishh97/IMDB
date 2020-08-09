import string

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from login.models import *
from login.helpers import pwd_context
from datetime import datetime
import jwt
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
import random


@api_view(["POST"])
def create_user(request):
    try:
        # request.data._mutable = True
        data = request.data
        data['password'] = pwd_context.hash(data['password'])
        user_type = UserType.objects.get(name=data['user_type'])
        data['user_type_id'] = user_type.id
        data.pop('user_type')
        print(data)
        UserDetail.objects.create(**data)
        return Response(status=status.HTTP_200_OK, data={"data": data, "success": True})
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND, data={"message": str(e), "success": False})


@api_view(["POST"])
def login(request):
    try:
        data = request.data
        email = data['email']
        password = data['password']
        user_filter = UserDetail.objects.filter(email=email)
        if user_filter.count():
            user = user_filter.first()
            try:
                pwd_flag = pwd_context.verify(password, user.password)
            except Exception as e:
                print(e)
                pwd_flag = False
            if pwd_flag:
                token = jwt.encode({
                    'email': user.email,
                    'user_type': user.user_type.name
                },
                    'imdb', algorithm='HS256')
                data = {
                    "user_type": user.user_type.name,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "token": token
                }
                return Response(status=status.HTTP_200_OK, data={"data": data, "success": True})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED,
                                data={"message": "Password is incorrect", "success": False})

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED,
                            data={"message": "Username does not exist", "success": False})
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND, data={"message": str(e), "success": False})
