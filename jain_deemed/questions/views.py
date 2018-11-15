from django.shortcuts import render
from .models import Questions
from rest_framework import generics
from .serializers import QuestionSerializer

from rest_framework.response import Response
from rest_framework import status

from rounds.models import File

class QuestionList(generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()
    """
		Have to add exceptions with status code
    """
    def get_queryset(self):
        user = self.request.user.id
        level = self.request.query_params.get('level')

        if level:
        	level_id = Questions.objects.filter(level=level).values_list('id', flat=True).first()
        	
        	submited = File.objects.filter(level=level_id, owner=user)
        	print(level_id,'submited',submited, submited.count())
        	if submited.count() < 1:
	        	qs = Questions.objects.filter(level=level)
	        	return qs
        
        #return Response({'error': str("j")}, status=status.HTTP_408_REQUEST_TIMEOUT, content_type='application/json')

        #return Purchase.objects.filter(purchaser=user)