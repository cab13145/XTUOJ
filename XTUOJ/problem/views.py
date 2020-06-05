from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework import viewsets,mixins,filters
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN
from django_filters.rest_framework import DjangoFilterBackend
from .models import Problem,ProblemAuth,ProblemTag,ProblemDetail
from .serializers import ProblemSerializer,ProblemDetailSerializer,ProblemTagSerializer
from .permission import AdminOnly,AuthOnly
from django.http import FileResponse
from utils.models import UserType,ContestAuth,ContestType

import os
import base64
import zipfile
import shutil

class ProblemDetailView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    # 获取所有problem表数据，但是get请求走Retrieve所以是通过request中的problem_id取单条数据
    queryset = ProblemDetail.objects.all()
    lookup_field = 'problem'
    serializer_class = ProblemDetailSerializer
    permission_classes = (AuthOnly,)
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('problem',)

class ProblemView(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOnly,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle,]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('auth', 'title')
    search_fields = ('problem_id', 'tag__tag', 'title')

class ProblemTagView(viewsets.ModelViewSet):
    queryset = ProblemTag.objects.all()
    serializer_class = ProblemTagSerializer
    permission_classes = (AdminOnly,)
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"

class UploadFileView(APIView):
    def post(self, request, format=None):
        user_type = request.session.get('user_type', UserType.REGULAR_USER)
        #如果用户不是管理员则无权限上传文件
        if user_type == UserType.REGULAR_USER:
            return Response("Only administrators have authority",  status=HTTP_403_FORBIDDEN)
        uploadFile = request.FILES.get('file', None)
        #如果request没有携带文件则请求出错
        if not uploadFile:
            return Response("The file doesn't exist", status=HTTP_400_BAD_REQUEST)
        #以二进制方式打开ProblemData文件夹，权限为可读可写
        des = open("./ProblemData/" + uploadFile.name, 'wb+')
        #将上传的文件分块读入ProblemData文件夹中，上传文件需是zip压缩格式
        for chunk in uploadFile.chunks():
            des.write(chunk)
        des.close()
        return Response("File uploaded successfully", HTTP_200_OK)

class DownloadFileView(APIView):
    def get(self, request):
        user_type = request.session.get('user_type', UserType.REGULAR_USER)
        #如果用户不是管理员则无权限下载文件
        if  user_type == UserType.REGULAR_USER:
            return Response("Only administrators have authority", status=HTTP_403_FORBIDDEN)
        filename = request.GET.get('filename', '')
        #如果get请求没有携带filename参数，返回400
        if not filename:
            return Response("No file name specified", status=HTTP_400_BAD_REQUEST)
        #以只读权限打开对应zip压缩文件
        file = open('./ProblemData' + filename + '.zip', 'rb')
        response = FileResponse(file)
        #指定文件类型为word文档
        response['Content-Type'] = 'application/msword'
        #指定下载后保存文件的名字
        content_dis = 'attachment;filename=' + filename + '.zip'
        response['Content-Disposition'] = content_dis
        return response

class ShowPictureView(APIView):
    def get(self,request):
        picname = request.GET.get('problem_id', '')
        #如果get请求没有携带problem_id参数，返回400
        if not picname:
            return Response("No picture name specified", status=HTTP_400_BAD_REQUEST)
        #以只读权限，打开指定图片文件
        file = open('./ProblemData/' + picname + '.jpg', 'rb')
        result = file.read()
        result = base64.b64encode(result)
        return HttpResponse(result, content_type='image/jpg')