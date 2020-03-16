"""Spanglish app views urls."""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^words/language/(?P<iso1>[a-z]{2})/$',
        views.WordListView.as_view(), name=views.WordListView.name),
    url(r'^$', views.ApiRoot.as_view(), name=views.ApiRoot.name),
]
