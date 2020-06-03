from django.conf.urls import url,include
from problem import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('problem', views.ProblemView)
routers.register('problemdetail', views.ProblemDetailView)
routers.register('problemtag', views.ProblemTagView)


urlpatterns = [
    url('', include(routers.urls)),
    url(r'^uploadfile/', views.UploadFileView.as_view(), name='upload_file'),
    url(r'^downloadfile/',views.DownloadFileView.as_view(), name='download_file'),
    url(r'^showpicture/', views.ShowPictureView.as_view(), name='show_picture'),
]