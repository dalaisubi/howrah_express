from django.shortcuts import render
from .models import Questions, Level
from rest_framework import generics
from .serializers import QuestionSerializer, LoginLevelSerializer, AllTaskSerializers, LoginLevelAsJudgeSerializer
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
import datetime
from pytz import timezone 

from rounds.models import File
from django.http import JsonResponse


class QuestionList(generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()
    def get_queryset(self):
        user = self.request.user.id
        level = None        
        qs = None
        if 'level_of_contest' in self.request.session:
            level = self.request.session['level_of_contest']      
        
        if 'eligible_for_level' in self.request.session:
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


class LevelLoginAsParticipant(APIView):
    serializer_class = LoginLevelSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        request.session['eligible_for_level'] = False
        request.session['level_of_contest'] = None
        serializer = LoginLevelSerializer(data=data)
        
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            new_data['eligible_for_level'] = True
            request.session['eligible_for_level'] = True
            request.session['level_of_contest'] = new_data['level']
            if 'password' in new_data:
                new_data.pop('password')

            
            # A question set for a students according to level   
            ###### Start ####### 
            
            serializer_class = QuestionSerializer
            queryset = Questions.objects.all()
            if not(self.request.user.is_staff):
                user = self.request.user.id
                level = None        
                qs = None
                if 'level_of_contest' in self.request.session:
                    level = self.request.session['level_of_contest']      
                if 'eligible_for_level' in self.request.session:
                    level_id = Level.objects.get(id=level).id

                    qs = Questions.objects.filter(level=int(level_id)).values()
                    if qs.count() == 1:
                        for data in qs:
                            qs[0]['file'] = "https://jainuniversity.opeyy.com/media/" + qs[0]['file']
                        return Response(qs, status=status.HTTP_200_OK)              
            
            ##### End ####    
            
            return Response(
                {"errors": "hey, you can't access because you're no longer a participant"}, 
                status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                


class LevelLoginAsJudge(APIView):
    serializer_class = LoginLevelAsJudgeSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        request.session['eligible_for_level'] = False
        request.session['level_of_contest'] = None
        serializer = LoginLevelAsJudgeSerializer(data=data)
        
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            new_data['eligible_for_level'] = True
            request.session['eligible_for_level'] = True
            request.session['level_of_contest'] = new_data['level']
            if 'password' in new_data:
                new_data.pop('password')

            
            # A question set for a Judge according to level   
            ###### Start ####### 
            
            serializer_class = QuestionSerializer
            if self.request.user.is_staff:
                user = self.request.user.id
                level = None        
                qs = None
                if 'level_of_contest' in self.request.session:
                    level = self.request.session['level_of_contest']      
                if 'eligible_for_level' in self.request.session:
                    level_id = Level.objects.get(id=level).id

                    qs = Questions.objects.filter(level=int(level_id)).values()
                    ans = File.objects.filter(level=int(level_id)).values()
                    d={}
                    dlist=[]
                    
                    for data in ans:
                        team_name = User.objects.filter(id=int(data["owner_id"])).values_list('username', flat=True)
                        d['file'] = "https://jainuniversity.opeyy.com/media/"+data['file']
                        d['team_name'] = team_name[0]
                        d['remark'] = data['remark']
                        dlist.append(d.copy())
                    data = {
                        "quetion": qs,
                        "answer" : dlist
                    }
                    return Response(data, status=status.HTTP_200_OK)              
            
            ##### End ####    
            
            return Response(
                {"errors": "hey, you can't access because you're no longer a Judge"}, 
                status=status.HTTP_400_BAD_REQUEST
                )

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


class AnswerList(generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()
    # def get_queryset(self):
    #     user = self.request.user.id
    #     level = None        
    #     qs = None
    #     if 'level_of_contest' in self.request.session:
    #         level = self.request.session['level_of_contest']      
        
    #     if 'eligible_for_level' in self.request.session:
    #         level_id = Level.objects.get(id=level).id

    #         qs = Questions.objects.filter(level=int(level_id))
    #         if qs.count() == 1:
    #             return qs             
    #     return qs 

    # def get_serializer_context(self):
    #     level = None
    #     if 'level_of_contest' in self.request.session:
    #         level = self.request.session['level_of_contest']
    #     return {"user_id": self.request.user.id, "level_of_contest": level} 
