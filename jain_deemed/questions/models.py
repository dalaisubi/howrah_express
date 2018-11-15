from django.db import models

# Create your models here.

class Questions(models.Model):
	level = models.CharField(max_length=7, unique=True, blank=False, null=False)
	question_1 = models.CharField(max_length=4444, blank=False, null=False)
	question_2 = models.CharField(max_length=4444, blank=True, null=True)
	hint_1 = models.CharField(max_length=600, blank=True, null=True)
	hint_2 = models.CharField(max_length=600, blank=True, null=True)
	hint_3 = models.CharField(max_length=600, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.level