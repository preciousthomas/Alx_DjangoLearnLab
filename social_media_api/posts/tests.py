from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Comment
from rest_framework.authtoken.models import Token

User = get_user_model()

class PostCommentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass123')
        self.user2 = User.objects.create_user(username='u2', password='pass123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.post = Post.objects.create(author=self.user, title='T', content='C')

    def test_create_post(self):
        url = reverse('post-list')
        data = {'title': 'new', 'content': 'body'}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_post_update_by_non_owner_forbidden(self):
        # switch to user2
        token2 = Token.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token2.key)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        resp = self.client.patch(url, {'title':'hack'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_create(self):
        url = reverse('comment-list')
        resp = self.client.post(url, {'post': self.post.id, 'content': 'ok'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)