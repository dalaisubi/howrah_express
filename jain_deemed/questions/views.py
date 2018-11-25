from django.shortcuts import render
from .models import Questions, Level
from rest_framework import generics
from .serializers import QuestionSerializer, LoginLevelSerializer, AllTaskSerializers
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status

import datetime
from pytz import timezone 

from rounds.models import File

class QuestionList(generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()
    
    def get_queryset(self):
        user = self.request.user.id
        level = None        
        qs = Questions.objects.all()
        if 'level_of_contest' in self.request.session:
            level = self.request.session['level_of_contest']      
        
        print("eligible_for_level ------")
        if 'eligible_for_level' in self.request.session:
            print("eligible_for_level =====")
            level_id = Level.objects.get(id=level).id
            qs = Questions.objects.filter(level=int(level_id))
            if qs.count() == 1:
                return qs              
        return qs   

    def get_serializer_context(self):
        level = None
        if 'level_of_contest' in self.request.session:
            level = self.request.session['level_of_contest']
        return {"user_id": self.request.user.id, "level_of_contest": level} 


class LoginAsLevel(APIView):
    serializer_class = LoginLevelSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginLevelSerializer(data=data)
        request.session['eligible_for_level'] = False
        request.session['level_of_contest'] = None
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            new_data['eligible_for_level'] = True
            request.session['eligible_for_level'] = True
            request.session['level_of_contest'] = new_data['level']
            if 'password' in new_data:
                new_data.pop('password')    
            return HttpResponseRedirect('/api/question/level/get/')    
            #return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                


class AllTaskView(generics.ListAPIView):
    queryset = Questions.objects.all()
    serializer_class = AllTaskSerializers 

    def get_queryset(self):        
        level = None        
        qs = Questions.objects.all()          
        return qs   

    def get_serializer_context(self):
        user = self.request.user.id
        return {"user_id": self.request.user.id} 

class DetailTaskView(generics.RetrieveAPIView):
    queryset = Questions.objects.all()  