from django.conf.urls import url
from .views import QuestionList



urlpatterns = [
	url(r'^question/$', QuestionList.as_view(), name='get-question'),
]