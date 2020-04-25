from django.db import models

class UserData(models.Model):
    username = models.CharField(max_length=64, primary_key=True, null=False)
    ac_number = models.IntegerField(null=False, default=0)
    submit_number = models.IntegerField(null=False, default=0)
    rating = models.IntegerField(default=1500)
    ac_problem = models.TextField(null=True,default="")

    objects = models.Manager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user_data"
        ordering = ("-rating",)

class User(models.Model):
    username = models.CharField(max_length=64, primary_key=True, null=False)
    password = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=64, null=False)
    regtime = models.DateTimeField(auto_now_add=True)
    logintime = models.DateTimeField(auto_now=True)
    classes = models.CharField(max_length=64, null=False, default="")
    number = models.CharField(max_length=64, null=False, default="")
    qq = models.CharField(max_length=20, null=True,default="")
    email = models.CharField(max_length=64, null=True,default="")
    type = models.IntegerField(null=False, default=1)

    objects = models.Manager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"

