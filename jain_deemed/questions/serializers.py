from rest_framework import serializers
from .models import Questions
from rounds.models import File


class QuestionSerializer(serializers.ModelSerializer):
	is_submited = serializers.SerializerMethodField() 
	def get_is_submited(self, obj):
		user = self.context["user_id"]
		submited = File.objects.filter(level=obj.id, owner=user)
		if submited.count() >= 1:
			return True          
		return False
	def get_extra_data(self, instance):
		return "something"
	class Meta():
		model = Questions
		fields = ('level', 'question_1', 'question_2', 'hint_1', 'hint_2', 'hint_3', 'is_submited')

	


