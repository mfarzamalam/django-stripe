from django.db import models
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Course, Lesson


class CourseListView(ListView):
    model = Course


class CourseDetailView(DetailView):
    model = Course