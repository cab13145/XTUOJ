from django.db import models
from user.models import User
from problem.models import Problem
from django.contrib.postgres.fields import JSONField
from utils.models import ContestType,ContestAuth


class Contest(models.Model):
    contest_id = models.CharField(max_length=64,null=False, primary_key=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=64, default=ContestType.ACM)
    auth = models.CharField(default=ContestAuth.PRIVATE, max_length=64)

    objects = models.Manager()

    def __str__(self):
        return self.creator

    class Meta:
        db_table = "contest"
        ordering = ("-start_time",)

class ContestAnnouncement(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.contest_id

    class Meta:
        db_table = "contest_announcement"
        ordering = ("-create_time",)

class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, null=False, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, null=False, on_delete=models.CASCADE)
    problemtitle = models.CharField(max_length=200)
    rank = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return self.contest_id

    class Meta:
        db_table = "contest_problem"

class ContestComment(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    username = models.CharField(max_length=64)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    question = models.CharField(max_length=64, default="Question")
    content = models.TextField(max_length=500)
    reply = models.TextField(default="No Response")
    create_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = "contest_comment"
        ordering = ("-create_time",)

class ACMContestRank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    problem_rank = models.IntegerField()
    submission_number = models.IntegerField(default=0)
    ac_number = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)
    ac_time = models.IntegerField(default=0)
    is_ac = models.BooleanField(default=False)
    error_number = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        db_table = "acm_contest_rank"
        unique_together = (("user","contest","problem"),)

class OIContestRank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    problem_rank = models.IntegerField()
    submission_number = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    submit_time = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        db_table = "oi_contest_rank"
        unique_together = (("user","contest","problem"),)


class ContestParticipant(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        db_table = "contest_participant"
