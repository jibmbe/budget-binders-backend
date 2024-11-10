from django.contrib import admin

# Register your models here.
from .models import Book  
from .models import CustomUser

# Register the Book model with the admin site
admin.site.register(Book)
admin.site.register(CustomUser)