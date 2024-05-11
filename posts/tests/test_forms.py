from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from posts.forms import PostForm
from posts.models import Post, Group
from django.urls import reverse

User = get_user_model()


class PostsFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.client = Client()
        cls.client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='Test title group',
            description='Привет, добавляйся, если ты любишь писать код',
            slug='test_slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
        )

        cls.form = PostForm()

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='TestName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_valid_form_create_post(self):
        posts_count = Post.objects.count()

        form_data = {
            'text': 'Тестовый пост для формы',
            'group': PostsFormTest.group.id
        }

        response = self.authorized_client.post(reverse('posts:post_create'), data=form_data, follow=True)
        self.assertRedirects(response, reverse('posts:profile', kwargs={'username': self.user.username}))
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_post_edit_bd_correct(self):
        form_data = {
            'text': 'Измененный тестовый пост для формы',
            'group': PostsFormTest.group.id
        }
        self.post = Post.objects.create(
            author=self.user,
            text='Тестовый пост для формы',
            group=PostsFormTest.group
        )
        posts_count = Post.objects.count()
        response = self.authorized_client.post(reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
                                               data=form_data, follow=True)

        self.assertEqual(Post.objects.count(), posts_count)
        self.assertRedirects(response, reverse('posts:profile', kwargs={'username': self.user.username}))
        post = get_object_or_404(Post, id=self.post.id)
        self.assertEqual(post.text, 'Измененный тестовый пост для формы')
