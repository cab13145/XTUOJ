from django.conf.urls import url,include
from contest import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('contest', views.ContestView)
routers.register('contestcomment', views.ContestCommentView)
routers.register('contestannouncement', views.ContestAnnouncementView)
routers.register('contestproblem', views.ContestProblemView)
routers.register('acmboard', views.ACMContestBoardView)
routers.register('oiboard', views.OIContestBoardView)
routers.register('contestparticipant', views.ContestParticipantView)

urlpatterns = [
    url('',include(routers.urls)),
]
