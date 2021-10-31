from django.urls import reverse
from django.db import models
from django.utils import tree
from stripe_monthly.models import Memebership



class Course(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    allowed_membership = models.ManyToManyField(Memebership)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.slug})
    

class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video_url = models.CharField(max_length=100)
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title