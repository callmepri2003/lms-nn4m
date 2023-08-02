from django.contrib import admin
from django.urls import path, include

from interview import views
from .views import interview_dashboard_view, live_class_view
from .views import select_question_view, view_question_view
from .views import add_feedback_view
from .views import interview_class_view, active_live_class_view


urlpatterns = [
    path('', interview_dashboard_view),
    path('live-class/create-meeting/', views.create_zoom_meeting, name='create-zoom-meeting'),
    path('live-class/', active_live_class_view),
    path('live-class/<str:live_class_id>/', live_class_view, name='live_class'),
    path('live-class/<str:live_class_id>/select-question/', select_question_view),
    path('live-class/<str:live_class_id>/feedback/', view_question_view),
    path('live-class/<str:live_class_id>/question/<int:group_index>/<int:question_index>/', view_question_view, name='view_question'),
    path('add_feedback/<int:live_class_id>/', add_feedback_view, name='add_feedback'),
    path('class/<str:class_id>/', interview_class_view)
]
