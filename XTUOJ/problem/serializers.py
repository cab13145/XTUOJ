from rest_framework import serializers
from problem.models import Problem,ProblemDetail,ProblemTag

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'
        depth = 2

class ProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemDetail
        fields = '__all__'

class ProblemTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemTag
        fields = '__all__'
