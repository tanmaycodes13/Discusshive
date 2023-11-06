from django.contrib import admin
from core.models import Topic, Messages, Room

# Register your models here.

admin.site.register(Messages)
admin.site.register(Room)
admin.site.register(Topic)
