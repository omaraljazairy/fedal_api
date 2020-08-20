from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin
from .models import ClietAPIKey

@admin.register(ClietAPIKey)
class ClientAPIKeyModelAdmin(APIKeyModelAdmin):
    list_display = [*APIKeyModelAdmin.list_display, "client__name"]
    search_fields = [*APIKeyModelAdmin.search_fields, "client__name"]
