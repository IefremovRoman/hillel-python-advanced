from django.contrib import admin

from .models import Group, Student, Teacher

admin.site.register([Student, Group, Teacher])
