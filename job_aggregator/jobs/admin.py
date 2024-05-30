from django.contrib import admin
from .models import Jobs
from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.register(Jobs)

# Register your models here.
