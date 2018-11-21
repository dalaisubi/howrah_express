from rest_framework import serializers
from .models import Questions, Level
from rounds.models import File
from django.db.models import Q
from django.core.exceptions import ValidationError


class QuestionSerializer(serializers.ModelSerializer):
	is_submited = serializers.SerializerMethodField()
	level_of_contest = serializers.SerializerMethodField() 
	def get_is_submited(self, obj):
		user = self.context["user_id"]
		submited = File.objects.filter(level=obj.id, owner=user)
		if submited.count() >= 1:
			return True          
		return False
	def get_level_of_contest(self, instance):
		return self.context['level_of_contest']
	class Meta():
		model = Questions
		fields = ('level_of_contest', 'question_1', 'question_2', 'hint_1', 'hint_2', 'hint_3', 'time_in_hr', 'time_in_min', 'is_submited')

	
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
				level__exact=level
			)		
		if level1.exists() and level1.count() == 1:
			level_obj = level1
		else:
			raise ValidationError("Invalid level.")	

		if level_obj and password:
			password = Level.objects.filter(
				Q(password__exact=password) & Q(level__exact=level)
				)
			if password.exists():
				eligible_for_level = True
			else:
				raise ValidationError("Incorrect password please try again.")

		return data