from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from linkupapi.models import HoleScore, Golfer, Match, GolferMatch

class HoleScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoleScore
        fields = ('id', 'golfer', 'match', 'strokes', 'course_hole', 'notes')

class CreateHoleScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoleScore
        fields = ['id', 'golfer', 'match', 'strokes', 'course_hole', 'notes']

class HoleScoreView(ViewSet):
    def list(self, request):
        # golfer = Golfer.objects.get(pk=request.data['golfer'])
        hole_scores = HoleScore.objects.all()
        if "match" in request.query_params:
            match = Match.objects.get(pk=request.query_params['match'])
            hole_scores = hole_scores.filter(match=match)
        hole_scores = HoleScore.objects.filter(match=match)
        serialized = HoleScoreSerializer(hole_scores, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    def create(self, request):
        scored_golfer = Golfer.objects.get(pk=request.data['golfer'])
        scored_match = Match.objects.get(pk=request.data['match'])
        serialized = CreateHoleScoreSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save(golfer=scored_golfer, match=scored_match)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    def update(self, request, pk):
        hole_score_to_change = HoleScore.objects.get(pk=pk)
        hole_score_to_change.strokes = request.data['strokes']
        hole_score_to_change.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)