from django.test import TestCase
from .models import *
# Create your tests here.


class PostTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(email="a@b.com", password="Abc")
        CustomUser.objects.create(email="c@d.com", password="BDC")
        Post.objects.create(content="Test case", user_id=1)

    def test_sample(self):
        post = Post.objects.get(content="Test case")
        user = CustomUser.objects.get(pk=1)
        self.assertEqual(post.content, "Test case")
        self.assertEqual(user.password, "abcccc")

