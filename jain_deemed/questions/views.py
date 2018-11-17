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
    
    def get_queryset(self):
        user = self.request.user.id
        level = self.request.query_params.get('level')
        qs = Questions.objects.all()
        
        if level:
            qs = Questions.objects.filter(level=level)
            if qs.count() < 1:
                return None              
        return qs    

    def get_serializer_context(self):
        return {"user_id": self.request.user.id }         