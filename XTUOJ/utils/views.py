from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
import datetime
import json

class SystemTime(APIView):
    def get(self,request):
        return Response(datetime.datetime.now(), status=HTTP_200_OK)