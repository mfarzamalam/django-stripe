from django.db import models
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from stripe_monthly.models import UserMembership
from .models import Course, Lesson


class CourseListView(ListView):
    model = Course


class CourseDetailView(DetailView):
    model = Course


class LessonDetailView(View):
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        
        course = Course.objects.filter(slug=course_slug).first()
        lesson = Lesson.objects.filter(course=course.pk, slug=lesson_slug)

        user_membership_type = UserMembership.objects.filter(user=request.user).first()
        user_membership_type = user_membership_type.membership.membership_type

        course_allowed_mem_type = course.allowed_membership.all()
        
        if course_allowed_mem_type.filter(membership_type=user_membership_type):
            context = {'lesson':lesson, 'allowed':course_allowed_mem_type}
        else:
            context = {'allowed':course_allowed_mem_type}

        return render(request, "courses/lesson_detail.html", context)