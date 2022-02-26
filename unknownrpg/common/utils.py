from django.shortcuts import get_object_or_404
from django.http import Http404

# Used to get domain object to pass to service to avoid passing ID to a service from application/API


def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None
