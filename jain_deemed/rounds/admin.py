from django.contrib import admin

# Register your models here.
from .models import FileUpload, File, Photo

admin.site.register(File)
#admin.site.register(Photo)