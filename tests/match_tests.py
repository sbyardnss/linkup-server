import json
from rest_framework import status
from rest_framework.test import APITestCase
from linkupapi.models import Golfer, Match, Course
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class MatchTests(APITestCase):
    fixtures = ['users', 'tokens', 'golfers']

    def setUp(self):
        self.golfer = Golfer.objects.first()
        self.user = User.objects.create(
            username="sbyard", first_name="stephen", last_name="byard", email="notMine@email.com")
        self.user.set_password("notMyPassword")
        self.golfer.user = self.user
        self.golfer.save()

        self.golfer_2 = Golfer.objects.last()
        self.user2 = User.objects.create(
            username="notsbyard", first_name="not_stephen", last_name="not_byard", email="not_notMine@email.com")
        self.user2.set_password("alsoNotMyPassword")
        self.golfer_2.user = self.user2
        self.golfer_2.save()

        self.course = Course.objects.create(name = "Two Rivers Golf Course", address = "2235 Two Rivers Pkwy, Nashville, TN 37214", phone_number = "(615) 889-2675")
        self.match = Match.objects.create(course = self.course, date="2023-05-17", time="16:00:00", message="no message", creator=self.golfer_2)

        token = Token.objects.create(user=self.golfer.user)
        token2 = Token.objects.create(user=self.golfer_2.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_create_match(self):
        data = {
            "creator": 1,
            "courseId": 1,
            "date": "2023-05-17",
            "time": "16:00:00",
            "message": "this is a test tee time",
        }
        creator = Golfer.objects.get(pk=data['creator'])
        course = Course.objects.get(pk=data['courseId'])
        response = self.client.post(f'/matches', data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_match = Match.objects.get(pk=json_response['id'])
        self.assertEqual(created_match.creator, creator)
        self.assertEqual(created_match.course, course)
        self.assertEqual(json_response['date'], data['date'])
        self.assertEqual(json_response['time'], data['time'])
        self.assertEqual(json_response['message'], data['message'])

    def test_join_match(self):
        match = self.match
        match.golfers.set([self.golfer_2])
        golfer = self.golfer
        response = self.client.post(f'/matches/{match.id}/join_tee_time')
        json_response=json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(f'/matches/{match.id}')
        json_response=json.loads(response.content)
        self.assertEqual(json_response['golfers'], [{"full_name": self.golfer_2.full_name, "id": self.golfer_2.id}, {"full_name": golfer.full_name, "id": golfer.id}])
