from django.urls import path
from api.users.views import (
    SignupView,
    LoginView,
    LogoutView,
    ApproveUserView,
    EnableUserView,
    UserListingView,
    CreateEmployeeView,
)

urlpatterns = [
    path('signup', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('approve/<int:pk>', ApproveUserView.as_view()),
    path('enable/<int:pk>', EnableUserView.as_view()),
    path('', UserListingView.as_view()),
    path('<int:pk>', UserListingView.as_view()),
    path('createEmployee', CreateEmployeeView.as_view()),
]