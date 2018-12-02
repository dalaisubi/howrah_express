from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from .models import FileUpload, File ,Photo
from .serializers import FileUploadSerializer, FileSerializer, TestSerializer, PhotoSerializer, FileListSerializer

from questions.models import Questions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import datetime
from pytz import timezone 



from rest_framework import generics
from rest_framework.permissions import AllowAny


class FileUploadViewSet(ModelViewSet):
    
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(owner=self.request.user,
                       datafile=self.request.data.get('datafile'))
        return serializer


class FileView(APIView):
	queryset = File.objects.all()
	parser_classes = (MultiPartParser, FormParser)
	serializer_class = FileSerializer
	def post(self, request, *args, **kwargs):
		owner=self.request.user
		file_obj = File.objects.filter(owner=owner.id, level=self.request.data['level'])
		file_serializer = FileSerializer(data=self.request.data)
		level = self.request.data['level']
		ist = timezone('Asia/Kolkata')
		now = datetime.datetime.now(ist)
		day = Questions.objects.get(level=level).day
		
		if now < day: 
			if file_obj.count() < 1:
				if file_serializer.is_valid():
				  file_serializer.save(owner=owner)
				  return Response(file_serializer.data, status=status.HTTP_201_CREATED)
				else:
				  return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({"response": "Already Submited"})
		else:
			return Response({"response": "This task is expired"})		  
					  

class TestAPI(generics.ListCreateAPIView):
	queryset = File.objects.all()
	serializer_class = TestSerializer
	permission_classes = (AllowAny,)


class PhotoViewSet(ModelViewSet):
    serializer_class = FileListSerializer
    parser_classes = (MultiPartParser, FormParser,)
    queryset=Photo.objects.all()
