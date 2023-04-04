from rest_framework import permissions, status
from rest_framework.exceptions import APIException

from api.databaseModels.ApiKey import ApiKey
from api.enums.apikeycodes import ApiKeyStatus


class ApiKeyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        authorization = request.META.get('HTTP_AUTHORIZATION', None)
        if not authorization:
            raise MissingAPIKeyException()
        key = ApiKey.objects.filter(key=authorization, status=ApiKeyStatus.ACTIVE.value).exists()
        if not key:
            raise InvalidApiKeyException()
        return True


class InvalidApiKeyException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'response_code': status.HTTP_403_FORBIDDEN, 'message': 'Invalid authentication credentials'}


class MissingAPIKeyException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        'response_code': status.HTTP_403_FORBIDDEN,
        'message': 'Authentication credentials were not provided'
    }
