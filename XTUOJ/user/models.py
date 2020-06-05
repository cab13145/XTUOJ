from django.db import models
from utils.models import UserType
from problem.models import Problem


class User(models.Model):
    username = models.CharField(max_length=64, primary_key=True, null=False)
    password = models.CharField(max_length=64, null=False)
    name = models.CharField(max_length=64, null=False)
    regtime = models.DateTimeField(auto_now_add=True)
    logintime = models.DateTimeField(auto_now=True)
    classes = models.CharField(max_length=64, null=False, default="")
    number = models.CharField(max_length=64, null=False, default="")
    qq = models.CharField(max_length=20, null=True,default="")
    email = models.CharField(max_length=64, null=True,default="")
    type = models.CharField(max_length=64 ,default=UserType.REGULAR_USER)
    ac_number = models.IntegerField(null=False, default=0)
    submit_number = models.IntegerField(null=False, default=0)
    rating = models.IntegerField(default=1500)

    objects = models.Manager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"

class UserLoginData(models.Model):
    username = models.CharField(max_length=64, null=False)
    ip = models.CharField(max_length=150, null=True, default="unknown")
    logintime = models.DateTimeField(auto_now=True)
    msg = models.TextField(null=True)

    objects = models.Manager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user_login_data"
        ordering = ("-logintime",)

class UserACProblem(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, null=False, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.user

    class Meta:
        db_table = "user_ac_problem"