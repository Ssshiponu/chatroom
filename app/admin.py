from django.contrib import admin
from .models import Room, Topic, Msg

# Register your models here.

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Msg)