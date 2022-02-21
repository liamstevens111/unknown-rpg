from django.core import exceptions as django_exceptions
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from .models import BaseUser
from .services import user_create

from unittest.util import _MAX_LENGTH
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


class UserRegisterApi(APIView):
    permission_classes = [permissions.AllowAny]

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(
            style={"input_type": "password"}, write_only=True)
        character_name = serializers.CharField(min_length=5, max_length=20)

        # class Meta:
        #     model = BaseUser
        #     fields = ('email', 'character_name', 'password')
        #     fields = tuple(User.REQUIRED_FIELDS) + ( "password",)
        #     # extra_kwargs = {'password': {'write_only': True}}

        def validate(self, attrs):
            user = BaseUser(email=attrs['email'], password=attrs['password'])
            password = attrs.get("password")

            try:
                validate_password(password, user)
            except django_exceptions.ValidationError as e:
                serializer_error = serializers.as_serializer_error(e)
                raise serializers.ValidationError(
                    {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
                )

            return attrs

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)
