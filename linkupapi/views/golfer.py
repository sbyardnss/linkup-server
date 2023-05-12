from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action

from linkupapi.models import Golfer, GolferMatch, Match

class GolferSerializer(serializers.ModelSerializer):
    """serializer for golfer requests"""
    class Meta:
        model = Golfer
        fields = ('id', 'full_name')


class GolferView(ViewSet):
    """linkup golfer view"""
    def retrieve(self, request, pk=None):
        """handle get request for individual golfer"""
        golfer = Golfer.objects.get(pk=pk)
        serialized = GolferSerializer(golfer)
        return Response(serialized.data)

    def list(self, request):
        """handle list request for golfers"""
        golfers = Golfer.objects.all()
        serialized = GolferSerializer(golfers, many=True)
        return Response(serialized.data)