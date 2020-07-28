"""Spanglish app views urls."""
from django.conf.urls import url
from django.urls import path
from . import views
# from rest_framework import routers

# router = routers.DefaultRouter()
urlpatterns = [
    path('formsubmit/', views.FormsubmitsView.as_view()),
    # url('form')
]