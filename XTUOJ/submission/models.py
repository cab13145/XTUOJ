from django.db import models
from utils.shortcuts import rand_str
from problem.models import Problem
from contest.models import Contest
from user.models import User
from utils.models import JudgeStatus

class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, null=False, on_delete=models.CASCADE)
    #具体数字代表信息查阅判题机文档
    result = models.IntegerField(default=JudgeStatus.PENDING)
    time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)
    length = models.IntegerField()
    language = models.CharField(max_length=64)
    subtime = models.DateTimeField(auto_now_add=True)
    judger = models.CharField(max_length=64,default="judger")
    contest = models.ForeignKey(Contest, null=True, on_delete=models.CASCADE)
    message = models.TextField(default="null")
    ip = models.CharField(max_length=150, null=True, default="unknown")
    score = models.IntegerField(default=0)

    objects = models.Manager()


    class Meta:
        db_table = "judge_status"
        ordering = ("-subtime",)

class SubmitCode(models.Model):
    status = models.ForeignKey(Status, null=False, unique=True, on_delete=models.CASCADE)
    code = models.TextField(max_length=65536)

    objects = models.Manager()

    class Meta:
        db_table = "submit_code"

class CaseStatus(models.Model):
    status = models.ForeignKey(Status, null=False, on_delete=models.CASCADE)
    username = models.CharField(max_length=64)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    # 具体数字代表信息查阅判题机文档
    result = models.IntegerField()
    time = models.IntegerField()
    memory = models.IntegerField()
    testcase = models.CharField(max_length=200, default="unknown")
    inputdata = models.CharField(max_length=200, default="")
    outputdata = models.CharField(max_length=200, default="")
    useroutput = models.CharField(max_length=200, default="")

    objects = models.Manager()


    class Meta:
        db_table = "case_status"

class QuickTest(models.Model):
    username = models.CharField(max_length=64)
    problem = models.ForeignKey(Problem, null=False, on_delete=models.CASCADE)
    testin = models.TextField()
    testout = models.TextField()
    result = models.IntegerField(default=JudgeStatus.PENDING)
    time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)
    language = models.CharField(max_length=64)
    message = models.TextField(default="null")

    objects = models.Manager()

    class Meta:
        db_table = "quick_test"

class QuickTestCode(models.Model):
    test = models.ForeignKey(QuickTest, null=False, unique=True, on_delete=models.CASCADE)
    code = models.TextField(max_length=15000)

    objects = models.Manager()

    class Meta:
        db_table = "quick_test_code"