from django.test import TestCase
from .models import Post
from django.core.exceptions import ValidationError


class PostModelTest(TestCase):

    def test_title_cannot_be_blank(self):
        post = Post(body='This is a test', slug='test-slug')
        post.title = ''
        with self.assertRaises(ValidationError):
            post.save()

    def test_slug_generation(self):
        post = Post(title='Some Title', body='This is a test body')
        post.save()
        self.assertEqual(post.slug, 'some-title')  # Jeśli chodzi o Twoją logikę

    def test_created_field_auto_now_add(self):
        post = Post(title='Test', body='Test body', slug='test')
        post.save()
        self.assertIsNotNone(post.created)

    def test_ordering(self):
        post1 = Post.objects.create(title='First', body='Body1', slug='first')
        post2 = Post.objects.create(title='Second', body='Body2', slug='second')
        self.assertEqual(list(Post.objects.all()), [post2, post1])