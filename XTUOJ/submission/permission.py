from rest_framework import permissions
from contest.models import Contest
from utils.models import SettingBoard,UserType
import datetime

def getVisitorPermission(request):
    setting = SettingBoard.objects.filter(id=1)
    if len(setting) != 0:
        if not setting[0].openvisitor:
            user_id = request.session.get('user_id', None)
            if user_id != None:
                return True
            else:
                return False
        else:
            return True
    else:
        return True

class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not getVisitorPermission(request):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        user_type = request.session.get('user_type', UserType.REGULAR_USER)
        if user_type == UserType.ADMIN or user_type == UserType.SUPER_ADMIN:
            return True
        else:
            return False

class UserPutOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not getVisitorPermission(request):
            return False
        username = request.data.get('username')
        user_id = request.session.get('user_id', None)
        user_type = request.session.get('user_type', UserType.REGULAR_USER)
        if user_id == username or user_type != UserType.REGULAR_USER:
            return True
        else:
            return False

    def has_object_permission(self, request, view, judge):
        if not getVisitorPermission(request):
            return False
        username = request.data.get('username')
        user_id = request.session.get('user_id', None)
        user_type = request.session.get('user_type', UserType.REGULAR_USER)
        if user_id == username or user_type != UserType.REGULAR_USER:
            return True
        else:
            return False

class AfterContestOnly(permissions.BasePermission):
    #取代码仅调用Retrieve，只需判断具体对象权限，因此只要定义具体对象权限函数
    def has_object_permission(self, request, view, judge):
        if not getVisitorPermission(request):
            return False

        user_type = request.session.get('user_type', UserType.REGULAR_USER)
        if user_type == UserType.ADMIN or user_type == UserType.SUPER_ADMIN:
            return True

        setting = SettingBoard.objects.get(id=1)
        user_id = request.session.get('user_id', None)
        #要取的代码是登录用户的代码
        if user_id == judge.username:
            #判断oj是否开启了查看自己代码的权限
            if not setting.openselfstatus:
                return False
            else:
                return True
        #查看oj是否开启了查看代码的权限
        if not setting.openstatus:
            return False

        contest = Contest.objects.get(id=judge.contest)
        #在比赛过程当中不能查看他人代码
        if (datetime.datetime.now()-contest.start_time).total_seconds()<(contest.end_time-contest.start_time).total_seconds():
            return False

        return True