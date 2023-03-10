from django.contrib import admin
from django.urls import path, include

from .views import home_view, dashboard_view, course_page_view
from .views import course_video_view
urlpatterns = [
    path('', home_view),
    path('dashboard/', dashboard_view),
    path('course-page/<int:sectionInstanceId>/', course_page_view),
    path('course-page/<int:sectionInstanceId>/video/<int:videoId>/', course_video_view)
]
