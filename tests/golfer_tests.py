import json
from rest_framework import status
from rest_framework.test import APITestCase
from linkupapi.models import Golfer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class GolferTests(APITestCase):
    fixtures = ['users', 'tokens', 'golfers']

    def setUp(self):
        self.golfer = Golfer.objects.first()
        self.user = User.objects.create(username = "sbyard", first_name = "stephen", last_name = "byard", email = "notMine@email.com")
        self.user.set_password("notMyPassword")
        self.user2 = User.objects.create(username = "notsbyard", first_name = "not_stephen", last_name = "not_byard", email = "not_notMine@email.com")
        self.user2.set_password("alsoNotMyPassword")
        self.golfer.user = self.user
        self.golfer.save()
        self.golfer_2 = Golfer.objects.last()
        self.golfer_2.user = self.user2
        self.golfer_2.save()
        token = Token.objects.create(user=self.golfer.user)
        token2 = Token.objects.create(user=self.golfer_2.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_update_golfer(self):
        data = {
            "first_name": "test",
            "last_name": "test",
            "username": "working update",
            "email": "test@test.com",
            "data": "testing",
            "password": "testing"
        }
        golfer = self.golfer
        response = self.client.put(f'/golfers/{golfer.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'/golfers/{golfer.id}')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['first_name'], data['first_name'])
        self.assertEqual(json_response['last_name'], data['last_name'])
        self.assertEqual(json_response['username'], data['username'])
        self.assertEqual(json_response['email'], data['email'])
        # self.assertEqual(json_response['password'], password) 

    def test_add_friend(self):
        golfer1 = self.golfer
        golfer2 = self.golfer_2
        golfer1.friends.set([])
        response = self.client.post(f'/golfers/{golfer2.id}/add_friend')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_golfer(self):
        golfer1 = self.golfer
        response = self.client.get(f'/golfers/{golfer1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        self.assertEqual(golfer1.first_name, json_response["first_name"])
        self.assertEqual(golfer1.last_name, json_response["last_name"])
        self.assertEqual(golfer1.username, json_response["username"])
