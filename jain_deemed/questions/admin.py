from django.contrib import admin
from .models import Questions, Level, LevelForJudge
# Register your models here.
admin.site.register(Questions)
admin.site.register(Level)
admin.site.register(LevelForJudge)