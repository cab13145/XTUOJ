from rest_framework import permissions
from contest.models import Contest
from utils.models import SettingBoard,UserType
import datetime

def getVisitorPermission(request):
    setting = SettingBoard.objects.filter(id=1)
    if len(setting) != 0:
        if not setting[0].openvisitor:
            user_id = request.session.get('user_id', None)
            if user_id:
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
            if request.method == "PUT":
                id = request.data.get('contest_id', None)
                if id:
                    contest = Contest.objects.get(contest_id=id)
                    if (datetime.datetime.now()-contest.start_time).total_seconds() > (contest.end_time-contest.start_time).total_seconds():
                        return False
            return True


        return False

class UserAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        if not getVisitorPermission(request):
            return False

        user_type = request.session.get('user_type', UserType.REGULAR_USER)
        if user_type == UserType.SUPER_ADMIN or user_type == UserType.ADMIN:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        username = request.data.get('username')
        user_id = request.session.get('user_id', None)
        if username == user_id:
            return True

        return False

