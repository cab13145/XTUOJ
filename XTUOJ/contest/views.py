from django.shortcuts import render
from rest_framework import viewsets,mixins,filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_403_FORBIDDEN
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from contest.models import Contest,ContestComment,ContestProblem,ContestAnnouncement,ACMContestRank,OIContestRank,ContestParticipant
from contest.permission import AdminOnly,UserAuth
from contest.serializers import ContestSerializer,ContestAnnouncementSerializer,ContestCommentSerializer,ContestProblemSerializer,ACMContestRankSerializer,OIContestRankSerializer,ContestParticipantSerializer
from utils.models import UserType,ContestAuth
from user.models import User
import datetime

class ContestView(viewsets.ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    permission_classes = (AdminOnly,)
    pagination_class = LimitOffsetPagination
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('title', 'start_time', 'creator', 'type')
    search_fields = ('title', 'contest_id')

class ContestAnnouncementView(viewsets.ModelViewSet):
    queryset = ContestAnnouncement.objects.all()
    serializer_class = ContestAnnouncementSerializer
    permission_classes = (AdminOnly,)
    parser_classes = LimitOffsetPagination
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('contest', )

class ContestCommentView(viewsets.ModelViewSet):
    queryset = ContestComment.objects.all()
    serializer_class = ContestCommentSerializer
    permission_classes = (UserAuth,)
    pagination_class = LimitOffsetPagination
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('contest', 'problem')

class ContestProblemView(viewsets.ModelViewSet):
    queryset = ContestProblem.objects.all()
    serializer_class =  ContestProblemSerializer
    permission_classes = (AdminOnly,)
    pagination_class = LimitOffsetPagination
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('contest', 'problem')

class ACMContestBoardView(viewsets.ModelViewSet):
    queryset = ACMContestRank.objects.all().order_by("-ac_number","total_time")
    serializer_class = ACMContestRankSerializer
    permission_classes = (AdminOnly,)
    pagination_class = LimitOffsetPagination
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'contest')

class OIContestBoardView(viewsets.ModelViewSet):
    queryset = OIContestRank.objects.all().order_by("-total_score")
    serializer_class = OIContestRankSerializer
    permission_classes = (AdminOnly,)
    pagination_class = LimitOffsetPagination
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = "post"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'contest')

class ContestParticipantView(viewsets.ModelViewSet):
    queryset = ContestParticipant.objects.all()
    serializer_class = ContestParticipantSerializer
    permission_classes = (UserAuth,)
    pagination_class = LimitOffsetPagination
    throttle_classes = [ScopedRateThrottle,]
    throttle_scopr = "post"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('contest', 'user')