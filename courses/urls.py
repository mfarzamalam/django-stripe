from django.urls import path, include
from .views import CourseListView, CourseDetailView, LessonDetailView

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('<slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('<course_slug>/<lesson_slug>/', LessonDetailView.as_view(), name='lesson_detail'),
]