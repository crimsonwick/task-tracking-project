from rest_framework import permissions
from django.contrib.auth import authenticate
from api.users.models import AccessLevel
from oauth2_provider.models import AccessToken


class IsOauthAuthenticatedSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.META.get('HTTP_AUTHORIZATION', '').startswith('Bearer'):
            if not hasattr(request, 'user') or request.user.is_anonymous:
                user = authenticate(request=request)
                if user:
                    if user.role.code == AccessLevel.CEO_CODE:
                        request.user = request._cached_user = user
                        return True
                    return False

        else:
            try:
                access_token = request.COOKIES.get('u-at',None)  # sending in header as Cookie with param u-at=token? used for ajax,jquery
                if access_token:
                    request.user = AccessToken.objects.get(token=access_token).user
                    request.user.access_token = access_token
                    request.data['created_by'] = request.user.id
                    return True
                else:
                    return False
            except AccessToken.DoesNotExist:
                return False

class IsOauthAuthenticatedSoftwareEngineer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.META.get("HTTP_AUTHORIZATION", "").startswith("Bearer"):
            if not hasattr(request, "user") or request.user.is_anonymous:
                user = authenticate(request=request)
                if user:
                    if user.role.code == AccessLevel.SOFTWARE_ENGINEER_CODE:
                        request.user = request._cached_user = user
                        # request.data['created_by'] = request.user.id
                        return True
                    else:
                        return False
        else:
            try:
                access_token = request.COOKIES.get('u-at', None)
                if access_token:
                    request.user = AccessToken.objects.get(token=access_token).user
                    request.user.access_token = access_token
                    request.data['created_by'] = request.user.id
                    return True
                else:
                    return False
            except AccessToken.DoesNotExist:
                return False

class IsOauthAuthenticatedTeamManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.META.get("HTTP_AUTHORIZATION", "").startswith("Bearer"):
            if not hasattr(request, "user") or request.user.is_anonymous:
                user = authenticate(request=request)
                if user:
                    if user.role.code == AccessLevel.TEAM_MANAGER_CODE:
                        request.user = request._cached_user = user
                        # request.data['created_by'] = request.user.id
                        return True
                    else:
                        return False
        else:
            try:
                access_token = request.COOKIES.get('u-at', None)
                if access_token:
                    request.user = AccessToken.objects.get(token=access_token).user
                    request.user.access_token = access_token
                    request.data['created_by'] = request.user.id
                    return True
                else:
                    return False
            except AccessToken.DoesNotExist:
                return False