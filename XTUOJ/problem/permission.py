from rest_framework import permissions
from utils.models import ProblemAuth,SettingBoard,UserType
from problem.models import Problem

def getVisitorPermission(request):
    setting = SettingBoard.objects.filter(id=1)

    if len(setting) !=0:
        if not setting[0].openvisitor :
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
            return True
        else:
            return False

class AuthOnly(permissions.BasePermission):
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

    def has_object_permission(self, request, view, problem):
        if not getVisitorPermission(request):
            return False

        user_type = request.session.get('user_type', UserType.REGULAR_USER)

        if user_type == UserType.ADMIN or user_type == UserType.SUPER_ADMIN:
            return True
        problem_info = Problem.objects.get(title=problem.title)
        if problem_info.auth == ProblemAuth.PUBLIC or problem_info.auth == ProblemAuth.IN_THE_CONTEST:
            return True
        else:
            return False
