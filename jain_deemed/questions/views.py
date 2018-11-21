from django.shortcuts import render
from .models import Questions, Level
from rest_framework import generics
from .serializers import QuestionSerializer, LoginLevelSerializer
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from rounds.models import File

class QuestionList(generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()
    
    def get_queryset(self):
        #print(self.request.session['eligible_for_level'], '-----', self.request.session['level_of_contest'])
        user = self.request.user.id
        level = None
        if self.request.session['level_of_contest']:
            level = self.request.session['level_of_contest']
        qs = Questions.objects.all()
        
        if self.request.session['eligible_for_level']:
            level_id = Level.objects.get(level__exact=level).id
            qs = Questions.objects.filter(level=int(level_id))
            if qs.count() == 1:
                return qs              
        return None   

    def get_serializer_context(self):
        return {"user_id": self.request.user.id, "level_of_contest": self.request.session['level_of_contest'] } 


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
            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                