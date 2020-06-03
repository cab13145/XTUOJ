from rest_framework import serializers
from submission.models import Status,CaseStatus,SubmitCode,QuickTest,QuickTestCode
from problem.models import Problem

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['problem_id', 'title']

#class JudgeNoCodeStatusSerializer(serializers.ModelSerializer):
 #   problem = ProblemSerializer()
  #  class Meta:
   #     model = Status
    #    exclude = ['message']

class JudgeStatusSerializer(serializers.ModelSerializer):
    #problem = ProblemSerializer()
    class Meta:
        model = Status
        fields = '__all__'
        depth = 2

class SubmitCodeSerializer(serializers.ModelSerializer):
    #judge = StatusSerializer()
    class Meta:
        model = SubmitCode
        fields = '__all__'

class CaseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStatus
        fields = '__all__'

class QuickTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickTest
        fields = '__all__'

class QuickTestCodeSerializer(serializers.ModelSerializer):
    #test = QuickTestSerializer()
    class Meta:
        model = QuickTestCode
        fields = '__all__'