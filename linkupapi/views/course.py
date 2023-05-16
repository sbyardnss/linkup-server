from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
# from rest_framework.decorators import action
from linkupapi.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model= Course
        fields= ('id', 'name', 'address', 'phone_number', 'url')

class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model= Course
        fields= ['id', 'name', 'address', 'phone_number', 'url']

class CourseView(ViewSet):
    """handle requests for course info"""
    def list(self, request):
        courses = Course.objects.all()
        serialized = CourseSerializer(courses, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    def retrieve(self, request, pk=None):
        course = Course.objects.get(pk=pk)
        serialized = CourseSerializer(course, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)
    def create(self, request):
        serializer = CreateCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk=None):
        course = Course.objects.get(pk=pk)
        course.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    