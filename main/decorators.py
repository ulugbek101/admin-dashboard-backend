from functools import wraps
from rest_framework import status
from rest_framework.response import Response


def is_authenticated(f):
    """ Decorator to check if user is authenticated """

    @wraps(f)
    def inner(*args, **kwargs):
        user_is_authenticated = args[1].user.is_authenticated

        if not user_is_authenticated:
            return Response({'detail': 'Unauthorized'}, status=401)

        return f(*args, **kwargs)

    return inner


def is_superuser(f):
    """ Decorator to check if user is superuser """

    @wraps(f)
    def inner(*args, **kwargs):
        user_is_superuser = args[1].user.is_superuser

        if not user_is_superuser:
            return Response({'detail': 'You do not have enough permissions to perform this action'},
                            status=status.HTTP_403_FORBIDDEN)
        return f(*args, **kwargs)

    return inner
