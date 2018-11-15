from rest_framework import serializers
from .models import Questions


class QuestionSerializer(serializers.ModelSerializer):
	class Meta():
		model = Questions
		fields = ('level', 'question_1', 'question_2', 'hint_1', 'hint_2', 'hint_3')


