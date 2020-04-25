from django.db import models
from user.models import User
from django.contrib.postgres.fields import JSONField


class Contest(models.Model):
    contest_id = models.CharField(max_length=64,null=False)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=64, default="ACM")
    auth = models.IntegerField(default=2)

    objects = models.Manager()

    def __str__(self):
        return self.creator

    class Meta:
        db_table = "contest"
        ordering = ("-start_time",)

class ContestAnouncement(models.Model):
    contest_id = models.ForeignKey(Contest, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.contest_id

    class Meta:
        db_table = "contest_anouncement"
        ordering = ("-create_time",)

class ContestProblem(models.Model):
    contest_id = models.CharField(max_length=64)
    problem_id = models.CharField(max_length=64)
    problemtitle = models.CharField(max_length=200)
    rank = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return self.contest_id

    class Meta:
        db_table = "contest_problem"

class AbstractContestRank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    submission_number = models.IntegerField(default=0)

    class Meta:
        abstract = True

class ACMContestRank(AbstractContestRank):
    ac_number = models.IntegerField()
    total_time = models.IntegerField()
    #{“1001”:{“is_ac”:True,”ac_time”:666,”error_number”:2,”is_first_ac”:True}}
    #key是problem_id
    submission_info = JSONField(default=dict)

    objects = models.Manager()

    class Meta:
        db_table = "acm_contest_rank"
        unique_together = (("user", "contest"),)

class OIContestRank(AbstractContestRank):
    total_score = models.IntegerField(default=0)
    #{“1001”:666}
    # key为problem_id,值为现在的分数
    submission_info = JSONField(default=dict)

    objects = models.Manager()

    class Meta:
        db_table = "oi_contest_rank"
        unique_together = (("user", "contest"),)