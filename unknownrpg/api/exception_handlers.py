from rest_framework.views import exception_handler
from django.http import Http404
from django.core.exceptions import ValidationError as DjangoValidationError, PermissionDenied

from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, context)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {
            "detail": response.data
        }

    return response
