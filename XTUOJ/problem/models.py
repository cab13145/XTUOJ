from django.db import models
from contest.models import Contest

class ProblemTag(models.Model):
    tag = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.tag

    class Meta:
        db_table = "problem_tag"

class Problem(models.Model):
    problem_id = models.CharField(max_length=64, primary_key=True)
    contest = models.ForeignKey(Contest, null=True, on_delete=models.CASCADE)
    author = models.CharField(max_length=64, default="eric_xie")
    title = models.CharField(max_length=200)
    addtime = models.DateTimeField(auto_now=True)
    problemdes = models.TextField()
    input = models.TextField()
    output = models.TextField()
    sinput = models.TextField()
    soutput = models.TextField()
    source = models.TextField(null=True)
    time = models.IntegerField()
    memory = models.IntegerField()
    hint = models.TextField(null=True)
    auth = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "problem"
        ordering = ("addtime",)

class ProblemData(models.Model):
    problem_id = models.CharField(max_length=64)
    contest = models.ForeignKey(Contest, null=True, on_delete=models.CASCADE)
    level = models.IntegerField()
    title = models.CharField(max_length=200)
    submission = models.IntegerField()
    acnum = models.IntegerField()
    wanum = models.IntegerField()
    mlenum = models.IntegerField()
    renum = models.IntegerField()
    cenum = models.IntegerField()
    penum = models.IntegerField()
    senum = models.IntegerField()
    tag = models.ManyToManyField(ProblemTag)
    auth = models.IntegerField()
    score = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "problem_data"

