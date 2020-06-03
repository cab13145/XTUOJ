from django.db import models
from django.contrib.postgres.fields import JSONField

class UserType(object):
    REGULAR_USER = "Regular User"
    ADMIN = "Admin"
    SUPER_ADMIN = "Super Admin"

class ContestType(object):
    ACM = "ACM"
    OI = "OI"

class ProblemLevel(object):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "hard"

class ProblemAuth(object):
    PUBLIC = "Public"
    PRIVATE = "Private"
    IN_THE_CONTEST = "In The Contest"

class ContestAuth(object):
    PUBLIC = "Public"
    PRIVATE = "Private"
    PROTECT = "Protect"

class JudgeStatus(object):
    WAITING = -6
    PRESENTATION_ERROR = -5
    COMPILE_ERROR = -4
    WRONG_ANSWER = -3
    JUDGINNG = -2
    PENDING = -1
    ACCEPTED = 0
    CPU_TIME_LIMIT_EXCEEDED = 1
    REAL_TIME_LIMIT_EXCEEDED = 2
    MEMORY_LIMIT_EXCEEDED = 3
    RUNTIME_ERROR = 4
    SYSTEM_ERROR = 5

class SettingBoard(models.Model):
    openlanguage = models.CharField(max_length=500 ,default="C++|C|Python|Java")
    openoi = models.BooleanField(default=True)
    openstatus = models.BooleanField(default=True)
    openvisitor = models.BooleanField(default=True)
    openregister = models.BooleanField(default=True)
    openselfstatus = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = "setting_board"
