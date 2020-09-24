from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.http import HttpResponseNotFound
import json

def error404(request, exception):
   response_data = {}
   response_data['detail'] = 'Not found.'
   return HttpResponseNotFound(json.dumps(response_data), content_type="application/json")


schema_view = get_schema_view(
   openapi.Info(
      title="Fedal API",
      default_version='v3',
      description="Personal API for different personal projects",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="omar@fedal.nl"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
