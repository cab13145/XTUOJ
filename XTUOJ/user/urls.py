from django.conf.urls import url,include
from user import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('user', views.UserView)
routers.register('useracproblem', views.UserACProblemView)
routers.register('userlogindata', views.UserLoginDataView)

urlpatterns = [
    url('', include(routers.urls)),
    url(r'^register', views.UserRegisterView.as_view(), name='register'),
    url(r'^login', views.UserLoginView.as_view(), name='login'),
    url(r'^logout', views.UserLogoutView.as_view(), name='logout'),
    url(r'^updaterating', views.UserRatingUpdateView.as_view(), name='update_rating'),
    url(r'^updatelogindata', views.UserLoginDataUpdateView.as_view(), name='update_logindata'),
    url(r'^userupdate', views.UserUpdateView.as_view(), name='user_update'),
    url(r'^adminupdate',views.AdminAuthUpdateView.as_view(), name='admin_update'),
]