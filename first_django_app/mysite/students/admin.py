from django.contrib import admin

from .models import Student, Group, Teacher

admin.site.register([Student, Group, Teacher])