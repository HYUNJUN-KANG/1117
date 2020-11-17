from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer

@api_view(['POST'])
def signup(request):
    password = request.data.get('password')
    password2 = request.data.get('password2')

    if password != password2:
        message = {
            error: '비밀번호가 틀립니다.'
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(password)
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)