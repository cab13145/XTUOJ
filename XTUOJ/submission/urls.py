from django.conf.urls import url,include
from submission import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('judgestatus', views.JudgeStatusView)
routers.register('getcode', views.GetCodeView)
routers.register('casestatus', views.CaseStatusView)
routers.register('quicktest', views.QuickTestView)
routers.register('rankboard', views.RankBoardView)

urlpatterns =[
    url('', include(routers.urls)),
    url(r'submitcode', views.SubmitCodeView.as_view(), name='submitcode'),
    url(r'submittestcode', views.QuickTestSubmitCodeView.as_view(), name='submittestcode'),
    url(r'^rejudge', views.RejudgeView.as_view(), name='rejudge'),
]