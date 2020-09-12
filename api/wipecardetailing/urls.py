"""Spanglish app views urls."""
from django.conf.urls import url
from django.urls import path
from . import views
# from rest_framework import routers

# router = routers.DefaultRouter()
urlpatterns = [
    path('formsubmit/', views.FormsubmitsView.as_view()),
    path('multimedia/', views.MultmediaListView.as_view()),
    path('multimedia/post/', views.MultimediaCreateView.as_view()),
    path('multimedia/detail/<int:pk>/', views.MultimediaDetailView.as_view())
    # url('form')
]