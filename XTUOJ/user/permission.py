from rest_framework import permissions
from utils.models import SettingBoard,UserType

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

def getRegisterPermission(request):
    setting = SettingBoard.objects.filter(id=1)
    if len(setting) != 0:
        if not setting[0].openregister:
            return False
        else:
            return True
    else:
        return True

class AdminReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user_type = request.session.get('user_type', UserType.REGULAR_USER)
        if user_type == UserType.ADMIN or user_type == UserType.SUPER_ADMIN:
            #if request.method in permissions.SAFE_METHODS or request.method == "POST" or request.method == "DELETE":
            #    return True
            #else:
            #    return False
            return True
        else:
            return False

class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not getVisitorPermission(request):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST":
            return True

        user_type = request.session.get('user_type', UserType.REGULAR_USER)
        if user_type == UserType.REGULAR_USER:
            return False
        else:
            return True

class UserSafe(permissions.BasePermission):
    def has_permission(self, request, view):
        if not getVisitorPermission(request):
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.session.get('user_type',UserType.REGULAR_USER) == UserType.SUPER_ADMIN:
            return True

        rating = request.data.get('rating', -1)
        ac = request.data.get('ac_number', -1)
        submision = request.data.get('submit_number', -1)
        score = request.data.get('score', -1)
        type = request.data.get('type', -1)
        username = request.data.get('username')

        if request.method == "POST":
            if type != -1:
                return False
            if rating != "" or ac != "" or submision != "" or score != "":
                if rating == -1:
                    return True
                return False
            else:
                return True

        if rating != -1 or ac != -1 or submision != -1 or score != -1:
            return False

        user_id = request.session.get('user_id', None)
        if user_id == username:
            return True
        else:
            return False

class UserPutOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not getVisitorPermission(request):
            return False

        if request.method != "PUT" and request.method != "PATCH":
            return False

        username = request.data.get('username')
        user_id = request.session.get('user_id', None)

        if username == user_id or request.session.get('user_type', UserType.REGULAR_USER) == UserType.SUPER_ADMIN:
            return True
        else:
            return False

    def has_object_permission(self, request, view, user):
        if not getVisitorPermission(request):
            return False

        if request.method != "PUT" and request.method != "PATCH":
            return False

        username = request.data.get('username')
        user_id = request.session.get('user_id', None)

        if username == user_id or request.session.get('user_type', UserType.REGULAR_USER) == UserType.SUPER_ADMIN:
            return True
        else:
            return False

class AdminPutOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not getVisitorPermission(request):
            return False

        if request.method != "PUT" and request.method != "PATCH":
            return False

        if request.session.get('user_type', UserType.REGULAR_USER) == UserType.SUPER_ADMIN:
            return True
        else:
            return False

    def has_object_permission(self, request, view, user):
        if not getVisitorPermission(request):
            return False

        if request.method != "PUT" and request.method != "PATCH":
            return False

        if request.session.get('user_type', UserType.REGULAR_USER) == UserType.SUPER_ADMIN:
            return True
        else:
            return False

