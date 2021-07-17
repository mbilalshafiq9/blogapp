from django.contrib import admin

# Register your models here.
from home.models import Blog, Category, Comment

admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Comment)