from rest_framework import serializers
from contest.models import Contest,ContestAnnouncement,ContestProblem,ACMContestRank,OIContestRank,ContestComment,ContestParticipant

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'

class ContestAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestAnnouncement
        fields = '__all__'

class ContestProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestProblem
        fields = '__all__'

class ContestCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestComment
        fields = '__all__'


class ACMContestRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = ACMContestRank
        fields = '__all__'

class OIContestRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = OIContestRank
        fields = '__all__'

class ContestParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestParticipant
        fields = '__all__'