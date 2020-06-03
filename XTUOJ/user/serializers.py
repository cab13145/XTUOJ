from rest_framework import serializers
from user.models import User,UserLoginData,UserACProblem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserACProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserACProblem
        fields = '__all__'

class UserLoginDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLoginData
        fields = '__all__'

class UserNoPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']