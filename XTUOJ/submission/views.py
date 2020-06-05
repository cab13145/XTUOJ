from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_403_FORBIDDEN
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.pagination import  LimitOffsetPagination
from rest_framework import viewsets,mixins
from django_filters.rest_framework import DjangoFilterBackend
from submission.models import  Status,CaseStatus,SubmitCode,QuickTestCode,QuickTest
from submission.serializers import JudgeStatusSerializer,CaseStatusSerializer,SubmitCodeSerializer,QuickTestSerializer,QuickTestCodeSerializer
from submission.permission import AdminOnly,UserPutOnly,AfterContestOnly
from contest.models import Contest
from problem.models import Problem
from user.models import User
from utils.models import JudgeStatus
import datetime

class JudgeStatusView(viewsets.ModelViewSet):
    #id为自动生成的主键字段
    queryset = Status.objects.all()
    serializer_class = JudgeStatusSerializer
    permission_classes = (AdminOnly,)
    pagination_class = LimitOffsetPagination
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'result', 'contest', 'problem', 'language',)

class SubmitCodeView(APIView):
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "judge"
    def post(self, request):
        data = request.data.copy()
        contest_id = data.get('contest')
        problem_id = data.get('problem')
        print(problem_id)
        if contest_id:
            try:
                contest = Contest.objects.get(contest_id=contest_id)
                if (datetime.datetime.now()-contest.start_time).total_seconds()>(contest.end_time-contest.start_time).total_seconds():
                    return Response("The contest has ended!", status=HTTP_400_BAD_REQUEST)

            except Contest.DoesNotExist:
                return Response("Contest doesn't exist!", status=HTTP_200_OK)
        try:
            problem = Problem.objects.get(problem_id=problem_id)
        except Problem.DoesNotExist:
            return Response("Problem not exist!", status=HTTP_200_OK)

        username = data.get('user')
        user_id = request.session.get('user_id', None)
        user_ins = User.objects.get(username=username)
        problem_ins = Problem.objects.get(problem_id=problem_id)
        user_type = request.session.get('user_type', None)
        if not user_id:
            return Response("Please login first!", status=HTTP_400_BAD_REQUEST)
        if username == user_id:
            status =  Status.objects.create(user=user_ins, problem=problem_ins, length=data["length"], language=data["language"], contest=contest_id)
            status.save()
            code = SubmitCode.objects.create(status=status, code=data["code"])
            code.save()
            return Response("Submit successfully!", status=HTTP_200_OK)
        return Response("Submit unsuccessfully!", status=HTTP_200_OK)


class GetCodeView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = SubmitCode.objects.all()
    serializer_class = SubmitCodeSerializer
    permission_classes = (AfterContestOnly,)
    pagination_class = LimitOffsetPagination
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"


class CaseStatusView(viewsets.ModelViewSet):
    queryset = CaseStatus.objects.all()
    serializer_class = CaseStatusSerializer
    permission_classes = (AdminOnly,)
    pagination_class = LimitOffsetPagination
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('username', 'problem', 'status')

class QuickTestView(viewsets.ModelViewSet):
    queryset = QuickTest.objects.all()
    serializer_class = QuickTestSerializer
    permission_classes = (UserPutOnly,)
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('username', 'problem')

class QuickTestSubmitCodeView(APIView):
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "judge"
    def post(self, request):
        data = request.data.copy()
        problem_id = data.get('problem')
        try:
            problem = Problem.objects.get(problem_id=problem_id)
        except Problem.DoesNotExist:
            return Response("Problem not exist!", status=HTTP_200_OK)
        username = data.get('username')
        user_id = request.session.get('user_id', None)
        problem_ins = Problem.objects.get(problem_id=problem_id)
        if not user_id:
            return Response("Please login first!", status=HTTP_400_BAD_REQUEST)
        if username == user_id:
            test = QuickTest.objects.create(username=username, problem=problem_ins, testin=data["testin"], testout=data["testout"], language=data["language"])
            test.save()
            testcode = QuickTestCode.objects.create(test=test, code=data["code"])
            testcode.save()
            return Response("Test code submit successfully!", status=HTTP_200_OK)
        return Response("Test code submit unsuccessfully!", status=HTTP_200_OK)

class RankBoardView(viewsets.ModelViewSet):
    #取出七天之内ac的status
    queryset = Status.objects.filter(subtime__gte=datetime.datetime.now()-datetime.timedelta(days=7), result=0)
    serializer_class = JudgeStatusSerializer
    permission_classes = (AdminOnly,)
    pagination_class = LimitOffsetPagination
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('username', 'contest', 'problem', 'language')

class RejudgeView(APIView):
    permission_classes = (AdminOnly,)
    def post(self, request):
        contest_id = request.data.get('contest', None)
        problem_id = request.data.get('problem', None)
        status_id = request.data.get('status_id', None)
        judgestatus = request.data.get('judgestatus', None)

        if not contest_id and not problem_id:
            Status.objects.filter(contest=contest_id).filter(problem=problem_id).update(result=JudgeStatus.PENDING)
            return Response("Rejudge successfully!", status=HTTP_200_OK)

        if problem_id and not contest_id:
            Status.objects.filter(problem=problem_id).update(result=JudgeStatus.PENDING)
            return Response("Rejudge successfully!", status=HTTP_200_OK)

        if status_id:
            Status.objects.filter(status_id=status_id).update(result=JudgeStatus.PENDING)
            return Response("Rejudge successfully!", status=HTTP_200_OK)

        if judgestatus:
            Status.objects.filter(result=judgestatus).update(result=JudgeStatus.PENDING)
            return Response("Rejudge successfully!", status=HTTP_200_OK)

        return Response("Rejudge unsuccessfully!", status=HTTP_400_BAD_REQUEST)

