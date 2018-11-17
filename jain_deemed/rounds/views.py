from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from .models import FileUpload, File
from .serializers import FileUploadSerializer, FileSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
		if file_obj.count() < 1:
			if file_serializer.is_valid():
			  file_serializer.save(owner=owner)
			  return Response(file_serializer.data, status=status.HTTP_201_CREATED)
			else:
			  return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"response": "Already Submited"})		  
					  