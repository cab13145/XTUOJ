from django.shortcuts import render
from rest_framework import viewsets,filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.throttling import ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from user.models import User,UserLoginData,UserACProblem
from utils.models import UserType,ProblemAuth,SettingBoard,JudgeStatus
from user.serializers import UserSerializer,UserNoPassSerializer,UserACProblemSerializer,UserLoginDataSerializer
from user.permission import AdminOnly,UserSafe,UserPutOnly,AdminPutOnly,AdminReadOnly
from rest_framework.authentication import TokenAuthentication
from user.permission import getRegisterPermission

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserNoPassSerializer
    permission_classes = (UserSafe,)
    pagination_class = LimitOffsetPagination
    throttle_classes = [ScopedRateThrottle,]
    throttle_scpoe = "post"
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('type', 'username')
    search_fields = ('username', 'name', 'classes', 'number')

class UserACProblemView(viewsets.ModelViewSet):
    queryset = UserACProblem.objects.all()
    serializer_class = UserACProblemSerializer
    permission_classes = (UserSafe,)
    pagination_class = LimitOffsetPagination
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'problem')

class UserUpdateView(APIView):
    throttle_classes = [ScopedRateThrottle,]
    throttle_scpoe = "post"
    def put(self, request, format=None):
        username = request.session.get('user_id',None)
        password = request.data.get('password', None)
        name = request.data.get('name', None)
        classes = request.data.get('classes', None)
        number = request.data.get('number', None)
        qq = request.data.get('qq', None)
        email = request.data.get('email', None)
        #如果session中没有user_id，说明用户未登录
        if username == None:
            return Response("username error", status=HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.get(username=username)
            if password:
                user.password = password
            if name:
                user.name = name
            if classes:
                user.classes = classes
            if number:
                user.number = number
            if qq:
                user.qq = qq
            if email:
                user.email = email
            user.save()
            return Response("successful", status=HTTP_200_OK)

class AdminAuthUpdateView(APIView):
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    def put(self, request, format=None):
        user_type = request.session.get('user_type', UserType.REGULAR_USER)
        #查看登录用户权限类型，只有超级管理员才能修改用户信息
        if user_type != UserType.SUPER_ADMIN:
            return Response("Only super administrators have authority", status=HTTP_400_BAD_REQUEST)
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        name = request.data.get('name', None)
        number = request.data.get('number', None)
        classes = request.data.get('classes', None)
        qq = request.data.get('qq', None)
        email = request.data.get('email', None)
        type = request.data.get('type', None)
        if username == None:
            return Response("username error", status=HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.get(username=username)
            if password:
                user.password = password
            if name:
                user.name = name
            if number:
                user.number = name
            if classes:
                user.classes = classes
            if qq:
                user.qq = qq
            if email:
                user.email = email
            if type and user_type == UserType.SUPER_ADMIN:
                user.type = type
            user.save()
            return Response("successful", status=HTTP_200_OK)

class UserLoginDataView(viewsets.ModelViewSet):
    queryset = UserLoginData.objects.all()
    serializer_class = UserLoginDataSerializer
    permission_classes = (AdminReadOnly,)
    pagination_class = LimitOffsetPagination
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('username', 'ip')

class UserLoginDataUpdateView(APIView):
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    def post(self, request, format=None):
        ip = "User login IP failed to be retrieved"
        data = request.data.copy()
        #获取用户真实ip
        addr = request.META.get('HTTP_X_FORWARDED_FOR')
        if addr:
            ip = addr.split(',')[0]
        else:
            #获取用户代理ip
            ip = request.META.get('REMOTE_ADDR')
        data["ip"] = ip
        #获取客户端用户描述信息
        data["msg"] = request.META.get('HTTP_USER_AGENT', "The client’s user-agent string failed to be retrieved")
        serializer = UserLoginDataSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save() #如果新增失败查看是否是需要传入外键实例
        return Response("successful", status=HTTP_200_OK)

class UserLoginView(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.get(username=username)
        #比对request中的password与数据库中的是否一致
        if user.password != password:
            return Response("password error", status=HTTP_200_OK)
        else:
            serializer = UserSerializer(user)
            data = serializer.data
            #登录成功，填入session信息以供其他接口实现认证
            request.session['user_id'] = user.username
            request.session['user_type'] = user.type
            request.session['rating'] = user.rating
            return Response(data, status=HTTP_200_OK)

class UserLogoutView(APIView):
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    def get(self, request):
        user_id = request.session.get('user_id', None)
        user_type = request.session.get('user_type', None)
        rating = request.session.get('rating', None)
        if user_id:
            del request.session['user_id']
        if user_type:
            del request.session['user_type']
        if rating:
            del request.session['rating']
        return Response("Login out successful", status=HTTP_200_OK)


class UserRatingUpdateView(APIView):
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"

    def get(self, request):
        username = request.session.get('user_id', None)
        if username:
            userdata = User.objects.get(username=username)
            request.session['rating'] = userdata.rating
            return Response("Rating Update successfully", status=HTTP_200_OK)
        else:
            return Response("Rating Update failed", status=HTTP_200_OK)


class UserRegisterView(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"

    def post(self, request, format=None):
        #查看注册权限是否打开
        if not getRegisterPermission(request):
            return Response("Registration not open!", status=HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        username = data.get('username')
        #查看用户注册用户名是否重名
        if User.objects.filter(username=username):
            return Response("The username already exists!", status=HTTP_200_OK)
        data['type'] = UserType.REGULAR_USER
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)