from django.test import TestCase
from myapp.models import Post


class PostModelTestCase(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title='Test post', body='This is a test post.')

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test post')
        self.assertEqual(self.post.body, 'This is a test post.')
