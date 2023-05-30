from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from datetime import datetime
from django.db.models import Count, Q
from django.contrib.auth.models import User
from linkupapi.models import Golfer, Match

class MyMatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'creator', 'course', 'date', 'time', 'message', 'golfers', 'players')
class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Golfer
        fields = ('id', 'full_name', 'my_matches')
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')
class GolferSerializer(serializers.ModelSerializer):
    """serializer for golfer requests"""
    my_matches = MyMatchesSerializer(many=True)
    friends = FriendSerializer(many=True)
    user = UserSerializer(many=True)
    class Meta:
        model = Golfer
        fields = ('id', 'user', 'full_name',
                  'my_matches', 'followers', 'friends', 'is_friend', 'first_name', 'last_name')
# class CreateFriendshipSerializer(serializers.ModelSerializer):
#     """serializer for creating friendships"""
#     class Meta:
#         model = Friendship
#         fields = ['id', 'golfer', 'friend', 'created_on']


class GolferView(ViewSet):
    """linkup golfer view"""

    def retrieve(self, request, pk=None):
        """handle get request for individual golfer"""
        golfer = Golfer.objects.get(pk=pk)
        serialized = GolferSerializer(golfer)
        return Response(serialized.data)

    def list(self, request):
        """handle list request for golfers"""
        active_golfer = Golfer.objects.get(user=request.auth.user)
        golfers = Golfer.objects.annotate(is_friend=Count('followers', filter=Q(followers=active_golfer)))
        # print(request)
        if "friends" in request.query_params:
            golfers = golfers.filter(friends=request.query_params['friends'])
        if "email" in request.query_params:
            golfers = golfers.filter(
                user__email__exact=request.query_params['email'])
        serialized = GolferSerializer(golfers, many=True)
        return Response(serialized.data)
    def update(self, request, pk):
        golfer = Golfer.objects.get(pk=pk)
        golfer.user.username = request.data['username']
        golfer.user.set_password(request.data['password'])
        golfer.user.email = request.data['email']
        golfer.user.first_name = request.data['first_name']
        golfer.user.last_name = request.data['last_name']
        golfer.user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def add_friend(self, request, pk):
        golfer = Golfer.objects.get(user=request.auth.user)
        friend = Golfer.objects.get(pk=pk)
        golfer.friends.add(friend)
        return Response({'message': 'friend added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def remove_friend(self, request, pk):
        golfer = Golfer.objects.get(user=request.auth.user)
        friend = Golfer.objects.get(pk=pk)
        golfer.friends.remove(friend)
        return Response({'message': 'friend removed'}, status=status.HTTP_204_NO_CONTENT)
