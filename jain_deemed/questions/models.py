from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator

# Create your models here.
class Level(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	level = models.CharField(max_length=15, unique=True, blank=False, null=False)
	password = models.CharField(max_length=20, validators=[MinLengthValidator(8)])

	def __str__(self):
		return self.level



DAY_IN_EVENT_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
)

class Questions(models.Model):
	title = models.CharField(max_length=30, blank=False, null=False)
	day = models.DateTimeField(editable=True)
	level = models.ForeignKey(Level, to_field='id', on_delete=models.CASCADE, default=1, related_name='questions')
	file = models.FileField(upload_to='question/')
	question_1 = models.CharField(max_length=4444, blank=False, null=False)
	question_2 = models.CharField(max_length=4444, blank=True, null=True)
	hint_1 = models.CharField(max_length=600, blank=True, null=True)
	hint_2 = models.CharField(max_length=600, blank=True, null=True)
	hint_3 = models.CharField(max_length=600, blank=True, null=True)
	event = models.CharField(max_length=10, choices=DAY_IN_EVENT_CHOICES, default= 'Day-1', blank=False, null=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	time_in_hr = models.IntegerField(blank=False, null=False, choices=[(i, i) for i in range(0, 72)])
	time_in_min = models.IntegerField(blank=False, null=False, choices=[(i, i) for i in range(0, 61)])


	def __str__(self):
		return str(self.level) + "--" + str(self.id)


class LevelForJudge(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	level = models.ForeignKey(Questions, to_field='id', on_delete=models.CASCADE, default=1, related_name='levelquestions')
	password = models.CharField(max_length=20, validators=[MinLengthValidator(8)])

	def __str__(self):
		return str(self.level)
