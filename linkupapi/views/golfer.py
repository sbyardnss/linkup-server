from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from datetime import datetime
from linkupapi.models import Golfer, GolferMatch, Match

class GolferSerializer(serializers.ModelSerializer):
    """serializer for golfer requests"""
    class Meta:
        model = Golfer
        fields = ('id', 'full_name', 'matches', 'my_friends')

# class CreateFriendshipSerializer(serializers.ModelSerializer):
#     """serializer for creating friendships"""
#     model = Fr
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
    
    @action(methods=['post'], detail=True)
    def add_friend(self, request, pk):
        golfer = Golfer.objects.get(pk=pk)
        active_golfer = Golfer.objects.get(user=request.auth.user)
        friend_data = {
            'golfer': active_golfer.id,
            'friend': golfer.id,
            'created_on': datetime.now()
        }
        # friendship = 