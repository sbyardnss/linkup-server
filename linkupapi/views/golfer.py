from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from datetime import datetime
from linkupapi.models import Golfer, GolferMatch, Match, Friendship

class GolferSerializer(serializers.ModelSerializer):
    """serializer for golfer requests"""
    class Meta:
        model = Golfer
        fields = ('id', 'user', 'full_name', 'matches', 'my_friends')

class CreateFriendshipSerializer(serializers.ModelSerializer):
    """serializer for creating friendships"""
    class Meta:
        model = Friendship
        fields = ['id', 'golfer', 'friend', 'created_on']

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
        print(request)
        if "friends" in request.query_params:
            golfers = golfers.filter(friendships = request.query_params['friends'])
        if "email" in request.query_params:
            golfers = golfers.filter(user__email__exact=request.query_params['email'])
        serialized = GolferSerializer(golfers, many=True)
        return Response(serialized.data)
    
    @action(methods=['post'], detail=True)
    def add_friend(self, request, pk):
        golfer = Golfer.objects.get(pk=pk)
        active_golfer = Golfer.objects.get(user=request.auth.user)
        friendship = {
            'golfer': active_golfer.id,
            'friend': golfer.id,
            'created_on': datetime.now()
        }
        print(friendship)
        friendship = CreateFriendshipSerializer(data=friendship)
        friendship.is_valid(raise_exception=True)
        friendship.save()
        return Response({'message': 'friend added'}, status=status.HTTP_201_CREATED)
    @action(methods=['delete'], detail=True)
    def remove_friend(self, request, pk):
        golfer = Golfer.objects.get(user=request.auth.user)
        friendship = Friendship.objects.get(golfer=golfer.id, friend=pk)
        friendship.delete()
        return Response({'message': 'friend removed'})