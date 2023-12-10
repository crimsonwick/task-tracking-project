import oauth2_provider.views as oauth2_views
from django.urls import re_path, path, include

urlpatterns = [
    re_path(r'^oauth/authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    re_path(r'^oauth/token/$', oauth2_views.TokenView.as_view(), name="token"),
    re_path(r'^oauth/revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
    path('user/', include('api.users.urls')),
    path('task/', include('api.task.urls')),
]