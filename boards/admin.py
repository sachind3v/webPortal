from django.contrib import admin

# Register your models here. for viewable in admin interface
from .models import Board, Topic ,Post
admin.site.register({Post,Board,Topic})


