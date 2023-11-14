from django.contrib import admin
# Register your models here.
from .models import CustomUser
# Register your models here.
# admin.site.register(Post) 
admin.site.register(CustomUser) 
# admin.site.register(Like)
# admin.site.register(Comment)