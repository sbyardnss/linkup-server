from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.db.models import Count, Q
from linkupapi.models import Match, Golfer, Course, GolferMatch

class GolferOnMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Golfer
        fields = ('id', 'full_name')

class MatchSerializer(serializers.ModelSerializer):
    golfers = GolferOnMatchSerializer(many=True)
    class Meta:
        model = Match
        fields = ('id', 'creator', 'course', 'date', 'time', 'message', 'golfers', 'joined')
        depth = 1

class CreateMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'date', 'time', 'message']


class CreateGolferMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = GolferMatch
        fields = ['id', 'golfer', 'match', 'is_initiator']


class MatchView(ViewSet):
    def list(self, request):
        active_golfer = Golfer.objects.get(user=request.auth.user)
        try:
            matches = Match.objects.annotate(joined=Count('golfers', filter=Q(golfers=active_golfer)))
            # if "my_matches" in request.query_params:
            #     matches = matches.filter(golfers__user__id=request.auth.user.id)
            # if "open_matches" in request.query_params:
            #     matches = matches.filter(joined=0)
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
        serialized.save(creator=golfer, course=course, golfers=[golfer])
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
        match.golfers.add(golfer)
        return Response({'message': 'tee time joined'}, status=status.HTTP_201_CREATED)
    @action(methods=['delete'], detail=True)
    def leave_tee_time(self, request, pk):
        """delete request to leave other's tee time"""
        golfer= Golfer.objects.get(user=request.auth.user)
        match = Match.objects.get(pk=pk)
        match.golfers.remove(golfer)
        return Response({'message': 'tee time bailed'}, status=status.HTTP_204_NO_CONTENT)
    @action(methods=['get'], detail=False)
    def open(self, request):
        active_golfer= Golfer.objects.get(user=request.auth.user)
        matches = Match.objects.annotate(joined=Count('golfers', filter=Q(golfers=active_golfer)))
        matches = matches.filter(joined=0)
        serialized=MatchSerializer(matches, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    @action(methods=['get'], detail=False)
    def joined(self, request):
        active_golfer= Golfer.objects.get(user=request.auth.user)
        matches = Match.objects.annotate(joined=Count('golfers', filter=Q(golfers=active_golfer)))
        matches = matches.filter(joined=1)
        serialized=MatchSerializer(matches, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

