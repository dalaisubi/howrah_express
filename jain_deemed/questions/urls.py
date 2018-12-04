from django.conf.urls import url
from .views import QuestionList, LevelLoginAsParticipant, AllTaskView, LevelLoginAsJudge



urlpatterns = [
	url(r'^level/get/$', QuestionList.as_view(), name='get-question'),
	url(r'^level/login/$', LevelLoginAsParticipant.as_view(), name='level_login_as_participant'),
	url(r'^get_all_task/$'  ,AllTaskView.as_view(), name='get_all_task' ),
	url(r'^level/judge/$', LevelLoginAsJudge.as_view(), name='level_login_as_judge')
]