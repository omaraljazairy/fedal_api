"""Spanglish app views urls."""
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views
urlpatterns = [
    path('formsubmit/', views.FormsubmitsView.as_view()),
    path('multimedia/', views.MultmediaListView.as_view()),
    path('multimedia/post/', views.MultimediaCreateView.as_view()),
    path('multimedia/detail/<int:pk>/', views.MultimediaDetailView.as_view()),
]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)