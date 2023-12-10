from django.urls import path
from .views import (
    CreateTaskView,
    CreateAndAssignTaskView,
    ListingTaskView,
    ChangeStatusSweView,
    ChangeStatusTmView,
    ChangeTimeEstimationTmView,
)

urlpatterns = [
    path('create', CreateTaskView.as_view()),
    path('assign', CreateAndAssignTaskView.as_view()),
    path('', ListingTaskView.as_view()),
    path('<int:pk>', ListingTaskView.as_view()),
    path('changeStatus', ChangeStatusSweView.as_view()),
    path('changeStatusManager',ChangeStatusTmView.as_view()),
    path('changeTimeEstimation', ChangeTimeEstimationTmView.as_view()),
]