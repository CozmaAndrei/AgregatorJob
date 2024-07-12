from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.jobs_list, name='jobs_list'),
]