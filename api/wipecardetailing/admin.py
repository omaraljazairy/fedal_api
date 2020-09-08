from django.contrib import admin
from .models import Multimedia, Formsubmits

class MultimediaAdmin(admin.ModelAdmin):
    fields = ['title','type' ,'addedbyuser', 'added','link', 'socialmedianame']

class FormsubmitsAdmin(admin.ModelAdmin):
    fields = ['formname', 'companyname', 'customername', 'email', 'phonenumber', 'streetname',
    'housenumber', 'postcode', 'city', 'message', 'submitted', 'status']


admin.site.register(Multimedia, MultimediaAdmin)
admin.site.register(Formsubmits, FormsubmitsAdmin)