from django.contrib import admin
from .models import Record, Listening, Musician

# Register your models here.

admin.site.register(Record)
admin.site.register(Listening)
admin.site.register(Musician)
