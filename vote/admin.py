from django.contrib import admin
from vote.models import Topic, Choice
# Register your models here.
admin.site.register(Topic)
admin.site.register(Choice)