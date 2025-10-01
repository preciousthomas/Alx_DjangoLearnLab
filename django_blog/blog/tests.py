# blog/tests.py (append)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass')
        self.other = User.objects.create_user(username='bob', password='pass')
        self.post = Post.objects.create(title='Test', content='Body', author=self.user)

    def test_create_comment_requires_login(self):
        url = reverse('blog:comment_create', kwargs={'post_pk': self.post.pk})
        resp = self.client.post(url, {'content': 'Nice post!'})
        self.assertEqual(resp.status_code, 302)  # redirect to login

    def test_authenticated_user_can_create_comment(self):
        self.client.login(username='alice', password='pass')
        url = reverse('blog:comment_create', kwargs={'post_pk': self.post.pk})
        resp = self.client.post(url, {'content': 'Nice post!'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(self.post.comments.filter(content='Nice post!').exists())

    def test_comment_edit_and_delete_permissions(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='Original')
        self.client.login(username='bob', password='pass')
        edit_url = reverse('blog:comment_update', kwargs={'pk': comment.pk})
        resp = self.client.get(edit_url)
        self.assertIn(resp.status_code, (302, 403))
        self.client.login(username='alice', password='pass')
        resp2 = self.client.post(edit_url, {'content': 'Updated'}, follow=True)
        self.assertEqual(resp2.status_code, 200)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated')