# posts/tests_feed.py
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from posts.models import Post

User = get_user_model()

class FeedTests(APITestCase):
    def setUp(self):
        # users
        self.viewer = User.objects.create_user(username='viewer', password='pass')
        self.a = User.objects.create_user(username='author_a', password='pass')
        self.b = User.objects.create_user(username='author_b', password='pass')

        # posts (created in this order)
        self.p_a1 = Post.objects.create(author=self.a, title='a1', content='a1-content')
        self.p_b1 = Post.objects.create(author=self.b, title='b1', content='b1-content')
        self.p_a2 = Post.objects.create(author=self.a, title='a2', content='a2-content')

        # auth token for viewer
        Token.objects.create(user=self.viewer)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.viewer).key)

        # only follow author_a
        self.viewer.following.add(self.a)

    def _get_feed_items(self, resp_json):
        if isinstance(resp_json, dict) and 'results' in resp_json:
            return resp_json['results']
        return resp_json

    def test_feed_contains_only_followed_users_posts(self):
        url = reverse('user-feed')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = self._get_feed_items(resp.json())
        ids = [item['id'] for item in items]
        # posts by author_a should be present
        self.assertIn(self.p_a1.id, ids)
        self.assertIn(self.p_a2.id, ids)
        # posts by author_b should not be present
        self.assertNotIn(self.p_b1.id, ids)

    def test_feed_ordering_newest_first(self):
        url = reverse('user-feed')
        resp = self.client.get(url)
        items = self._get_feed_items(resp.json())
        # expect created_at fields sorted descending
        created_at_list = [it['created_at'] for it in items]
        self.assertEqual(sorted(created_at_list, reverse=True), created_at_list)

    def test_feed_requires_auth(self):
        self.client.force_authenticate(user=None)
        url = reverse('user-feed')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)