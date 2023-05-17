from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from linkupapi.models import Match, Golfer, Course, GolferMatch


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'creator', 'course', 'date_time', 'message', 'players')
        depth = 1

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
        try:
            matches = Match.objects.all()
            if "my_matches" in request.query_params:
                matches = matches.filter(players=request.query_params['my_matches'])
            serialized = MatchSerializer(matches, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Match.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    def retrieve(self, request, pk=None):
        match = Match.objects.get(pk=pk)
        serialized = MatchSerializer(match, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        golfer = Golfer.objects.get(user=request.auth.user)
        course = Course.objects.get(pk=request.data['courseId'])
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

    @action(methods=['post'], detail=True)
    def join_tee_time(self, request, pk):
        """post request for user to join other's tee time"""
        golfer = Golfer.objects.get(user=request.auth.user)
        match = Match.objects.get(pk=pk)
        golfer_match = {
            'golfer': golfer.id,
            'match': match.id,
            'is_initiator': 0
        }
        golfer_match = CreateGolferMatchSerializer(data=golfer_match)
        golfer_match.is_valid(raise_exception=True)
        golfer_match.save()
        return Response({'message': 'tee time joined'}, status=status.HTTP_201_CREATED)
    @action(methods=['delete'], detail=True)
    def leave_tee_time(self, request, pk):
        """delete request to leave other's tee time"""
        golfer= Golfer.objects.get(user=request.auth.user)
        golfer_match = GolferMatch.objects.get(golfer=golfer, match=pk)
        golfer_match.delete()
        return Response({'message': 'tee time bailed'})