from django.contrib import admin
from .models import Announcement


# Register your models here.

myModel = [Announcement]
admin.site.register(myModel)
