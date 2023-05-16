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

class MessageView(ViewSet):
    """handle requests for messages"""
    def list(self, request):
        active_golfer = Golfer.objects.get(user=request.auth.user)
        messages = Message.objects.filter(Q(sender=active_golfer.id) | Q(recipient=active_golfer.id))
        serialized = MessageSerializer(messages, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
