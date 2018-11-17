from django.conf.urls import url
from .views import QuestionList



urlpatterns = [
	url(r'^get/$', QuestionList.as_view(), name='get-question'),
]