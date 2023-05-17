from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from linkupapi.models import HoleScore, Golfer

class HoleScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoleScore
        fields = ('id', 'golfer_match', 'strokes', 'course_hole', 'notes')

class CreateHoleScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoleScore
        fields = ['id', 'golfer_match', 'strokes', 'course_hole', 'notes']

class HoleScoreView(ViewSet):
    def list(self, request):
        active_golfer = Golfer.objects.get(user = request.auth.user)
