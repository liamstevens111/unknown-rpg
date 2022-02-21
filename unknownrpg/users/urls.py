from django.urls import path
from .apis import UserRegisterApi

urlpatterns = [
    path('create/', UserRegisterApi.as_view(), name='register'),
]
