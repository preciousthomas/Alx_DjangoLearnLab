# accounts/tests_follow.py
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status

User = get_user_model()

class FollowUnfollowTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='pass')
        self.u2 = User.objects.create_user(username='u2', password='pass')
        self.u3 = User.objects.create_user(username='u3', password='pass')
        token = Token.objects.create(user=self.u1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_follow_user(self):
        url = reverse('follow-user', kwargs={'user_id': self.u2.id})
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn(self.u2, self.u1.following.all())

    def test_cannot_follow_self(self):
        url = reverse('follow-user', kwargs={'user_id': self.u1.id})
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_user(self):
        self.u1.following.add(self.u2)
        url = reverse('unfollow-user', kwargs={'user_id': self.u2.id})
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.u2, self.u1.following.all())

    def test_follow_requires_auth(self):
        self.client.force_authenticate(user=None)
        url = reverse('follow-user', kwargs={'user_id': self.u2.id})
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)