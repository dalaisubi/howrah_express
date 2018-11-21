from django.conf.urls import url
from .views import QuestionList, LoginAsLevel



urlpatterns = [
	url(r'^get/$', QuestionList.as_view(), name='get-question'),
	url(r'^level/login/$', LoginAsLevel.as_view(), name='level_login'),
]