from django.contrib import admin

from . models import InstitutionProfile, InstitutionUser, Department, Session
# Register your models here.
admin.site.register(InstitutionProfile)
admin.site.register(InstitutionUser)
admin.site.register(Department)
admin.site.register(Session)