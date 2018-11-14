from django.contrib import admin

# Register your models here.
from .models import FileUpload, File

admin.site.register(File)