from django.conf.urls import url
from .views import QuestionList, LoginAsLevel, AllTaskView



urlpatterns = [
	url(r'^level/get/$', QuestionList.as_view(), name='get-question'),
	url(r'^level/login/$', LoginAsLevel.as_view(), name='level_login'),
	url(r'^get_all_task/$'  ,AllTaskView.as_view(), name='get_all_task' )
]