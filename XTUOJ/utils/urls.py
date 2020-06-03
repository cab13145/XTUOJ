from django.conf.urls import url,include
from utils import views
from rest_framework import routers

urlpatterns =[
    url(r'^systemtime', views.SystemTime.as_view(), name='systemtime'),
]