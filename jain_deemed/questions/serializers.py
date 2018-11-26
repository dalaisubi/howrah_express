from rest_framework import serializers
from .models import Questions, Level
from rounds.models import File
from django.db.models import Q
from django.core.exceptions import ValidationError
import datetime
from pytz import timezone 


class QuestionSerializer(serializers.ModelSerializer):
	Status = serializers.SerializerMethodField()
	timestamp = serializers.SerializerMethodField()
	timeleft = serializers.SerializerMethodField()
	def get_Status(self, obj):
		user = self.context["user_id"]
		level = Questions.objects.get(id=obj.id).level
		submited = File.objects.filter(level=level, owner=user)
		ist = timezone('Asia/Kolkata')
		now = datetime.datetime.now(ist)
		day = Questions.objects.get(id=obj.id).day
		if submited.count() >= 1:
			return "submited"
		elif now > day:
			return "expired"	          
		return "unlocked"
	def get_timestamp(self, obj):
		ist = timezone('Asia/Kolkata')
		now = datetime.datetime.now(ist).timestamp()
		return now	

	def get_timeleft(self, obj):
		miniute = obj.time_in_min
		hour = obj.time_in_hr

		print( 'time_in_hr----')
		return 'nn'	
	class Meta():
		model = Questions
		fields = ('id','level','title', 'timestamp', 'timeleft', 'day','event', 'question_1', 'question_2', 'hint_1', 'hint_2', 'hint_3', 'time_in_hr', 'time_in_min', 'Status')

	
class LoginLevelSerializer(serializers.ModelSerializer):
	level = serializers.CharField(allow_blank=True, required=False)
	password = serializers.CharField(allow_blank=True, required=False)
	class Meta:
		model = Level
		fields = [
			'level',
			'password',			
		]

		extra_kwargs = {'password': 
					   		{'write_only': True}
					   	}

	def validate(self , data):
		level = data.get('level', None)
		password = data.get('password', None)
		level_obj = None
		if not level:
			raise ValidationError('A level is required.')

		level1 = Level.objects.filter (
				id=level
			)		
		if level1.exists() and level1.count() == 1:
			level_obj = level1
		else:
			raise ValidationError("Invalid level.")	

		if level_obj and password:
			password = Level.objects.filter(
				Q(password__exact=password) & Q(id=level)
				)
			if password.exists():
				eligible_for_level = True
				
			else:
				raise ValidationError("Incorrect password please try again.")

		return data


class AllTaskSerializers(serializers.ModelSerializer):
	Status = serializers.SerializerMethodField()
	def get_Status(self, obj):
		user = self.context["user_id"]
		submited = File.objects.filter(level=obj.id, owner=user)
		ist = timezone('Asia/Kolkata')
		now = datetime.datetime.now(ist)
		day = Questions.objects.get(id=obj.id).day
		if submited.count() >= 1:
			return "submited"
		elif now > day:
			return "expired"	          
		return "locked"

	class Meta:
		model = Questions
		fields = ('id','level', 'title', 'event', 'day', 'Status')		