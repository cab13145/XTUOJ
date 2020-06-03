from django.db import models
from utils.models import ProblemAuth,ProblemLevel

class ProblemTag(models.Model):
    tag = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.tag

    class Meta:
        db_table = "problemtag"

class Problem(models.Model):
    problem_id = models.CharField(max_length=64, primary_key=True, null=False)
    title = models.CharField(max_length=200)
    level = models.CharField(max_length=64, default=ProblemLevel.MEDIUM)
    score = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now=True)
    auth = models.CharField(max_length=64, default=ProblemAuth.PUBLIC)
    tag = models.ManyToManyField(ProblemTag)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "problem"
        ordering = ("problem_id",)

class ProblemDetail(models.Model):
    problem = models.ForeignKey(Problem, null=False, unique=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=64, null=True)
    problemdes = models.TextField()
    input = models.TextField()
    output = models.TextField()
    sinput = models.TextField()
    soutput = models.TextField()
    source = models.TextField(null=True)
    time = models.IntegerField()
    memory = models.IntegerField()
    hint = models.TextField(null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "problem_detail"
        ordering = ("problem",)

