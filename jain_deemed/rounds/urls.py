from django.conf.urls import url
from .views import FileView, PhotoViewSet



urlpatterns = [
	url(r'^upload/$', FileView.as_view(), name='file-upload'),
	#url(r'^upload/test/$', PhotoViewSet, name='file-upload-test'),
]