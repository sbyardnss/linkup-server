from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from linkupapi.models import Golfer, Message
from django.db.models import Q

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'message', 'date_time', 'read')

class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'message', 'date_time', 'read')
class MessageView(ViewSet):
    """handle requests for messages"""
    def list(self, request):
        """list only gets messages pertaining to active user"""
        active_golfer = Golfer.objects.get(user=request.auth.user)
        messages = Message.objects.filter(Q(sender=active_golfer.id) | Q(recipient=active_golfer.id))
        serialized = MessageSerializer(messages, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    def create(self, request):
        golfer = Golfer.objects.get(user=request.auth.user)
        message={
            'sender': golfer.id,
            'recipient': request.data['recipientId'],
            'message': request.data['message'],
            'read': False,
            'date_time': request.data['time']
        }
        message = CreateMessageSerializer(data=message)
        message.is_valid(raise_exception=True)
        message.save()
        return Response(message.data, status=status.HTTP_201_CREATED)
