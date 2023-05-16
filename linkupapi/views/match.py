from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from linkupapi.models import Match, Golfer, Course, GolferMatch

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'creator', 'golfers', 'course', 'date_time', 'message')

class CreateMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'date_time', 'message']
class CreateGolferMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = GolferMatch
        fields = ['id', 'golfer', 'match', 'is_initiator']
class MatchView(ViewSet):
    def list(self, request):
        matches = Match.objects.all()
        serialized = MatchSerializer(matches, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    def retrieve(self, request, pk=None):
        match = Match.objects.get(pk=pk)
        serialized = MatchSerializer(match, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)
    def create(self, request):
        golfer = Golfer.objects.get(user=request.auth.user)
        course = Course.objects.get(pk=request.data['courseId'])
        # match = Match()
        # match.creator = golfer
        # match.course = course
        # match.message = request.data['message']
        serialized = CreateMatchSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save(creator=golfer, course=course)
        golf_match_data = {
            'golfer': golfer.id,
            'match': serialized.data['id'],
            'is_initiator': 1
        }
        golfer_match = CreateGolferMatchSerializer(data=golf_match_data)
        golfer_match.is_valid(raise_exception=True)
        golfer_match.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk=None):
        match = Match.objects.get(pk=pk)
        match.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)