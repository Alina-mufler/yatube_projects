import tempfile

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from posts.forms import PostForm
from posts.models import Post, Group
from django.conf import settings
from django.urls import reverse
from django import forms

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class PostsViewsTest(TestCase):

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

    def setUp(self) -> None:
        self.user_1 = User.objects.create_user(username='TestName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_1)

    def test_uses_correct_template(self):

        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_posts', kwargs={'slug': PostsViewsTest.group.slug}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user_1.username}): 'posts/profile.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }

        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_uses_correct_template_with_kwargs(self):

        templates_pages_names = {
            reverse('posts:post_detail', kwargs={'post_id': PostsViewsTest.post.id}): 'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': PostsViewsTest.post.id}): 'posts/create_post.html',
        }

        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = PostsViewsTest.client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def context_correct(self, context):
        for value, expected in context.items():
            with self.subTest(value=value):
                self.assertEqual(value, expected)

    def test_index_page_show_correct_context(self):

        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]

        context = {
            first_object.author: PostsViewsTest.post.author,
            first_object.text: PostsViewsTest.post.text,
            first_object.group: PostsViewsTest.post.group,
        }

        self.context_correct(context)

    def test_group_post_show_correct_context(self):

        response = self.authorized_client.get(reverse('posts:group_posts', kwargs={'slug': PostsViewsTest.group.slug}))
        group = response.context['group']
        first_object = response.context['page_obj'][0]

        context = {
            group: PostsViewsTest.group,
            first_object.author: PostsViewsTest.post.author,
            first_object.text: PostsViewsTest.post.text,
            first_object.group: PostsViewsTest.post.group,
        }

        self.context_correct(context)

    def test_profile_show_correct_context(self):
        username = PostsViewsTest.user.username
        response = self.authorized_client.get(reverse('posts:profile', kwargs={'username': username}))
        username_context = response.context['username']
        first_object = response.context['page_obj'][0]

        context = {
            username_context: username,
            first_object.author: PostsViewsTest.post.author,
            first_object.text: PostsViewsTest.post.text,
            first_object.group: PostsViewsTest.post.group,
        }

        self.context_correct(context)

    def test_post_detail_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:post_detail', kwargs={'post_id': PostsViewsTest.post.id}))
        post = response.context['post']
        count_post = response.context['author_count_posts']

        author = PostsViewsTest.post.author
        author_count_posts = Post.objects.filter(author=author).count()

        context = {
            post.author: PostsViewsTest.post.author,
            post.text: PostsViewsTest.post.text,
            post.group: PostsViewsTest.post.group,
            count_post: author_count_posts,
        }

        self.context_correct(context)

    def test_create_post_show_correct_context(self):
        response = PostsViewsTest.client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)

    def test_edit_post_show_correct_contex(self):
        response = PostsViewsTest.client.get(reverse('posts:post_edit', kwargs={'post_id': PostsViewsTest.post.id}))
        form = response.context['form']
        is_edit = response.context['is_edit']
        post_id = response.context['post_id']

        context = {
            form.initial['text']: PostsViewsTest.post.text,
            form.initial['group']: PostsViewsTest.post.group,
            is_edit: True,
            post_id: PostsViewsTest.post.id,
        }

        self.context_correct(context)

    def test_create_post_with_group(self):
        self.authorized_client.post(reverse('posts:post_create'), {'text': 'Test post', 'group': PostsViewsTest.group.id})

        urls = {
            reverse('posts:index'),
            reverse('posts:group_posts', kwargs={'slug': PostsViewsTest.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user_1.username}),
        }

        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertContains(response, 'Test post')


class PaginatorViewsTest(TestCase):

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

        for i in range(14):
            cls.post_i = Post.objects.create(
                author=cls.user,
                text=f'Тестовый пост {i}',
                group=cls.group,
            )

        cls.urls = [
            reverse('posts:index'),
            reverse('posts:group_posts', kwargs={'slug': PaginatorViewsTest.group.slug}),
            reverse('posts:profile', kwargs={'username': PaginatorViewsTest.user.username}),
        ]

    def test_first_page_contains_ten_records(self):

        for url in PaginatorViewsTest.urls:
            with self.subTest(url=url):
                response = PaginatorViewsTest.client.get(url)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_four_records(self):

        for url in PaginatorViewsTest.urls:
            with self.subTest(url=url):
                response = self.client.get(url + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 4)
