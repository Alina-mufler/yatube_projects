from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model
from posts.models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):

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

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверка urls для авторизованного пользователя
    def test_urls_uses_auth_correct_template(self):
        templates_urls_names = {
            '/create/': 'posts/create_post.html',
            '/group/test_slug/': 'posts/group_list.html',
            '': 'posts/index.html',
            f'/posts/{PostURLTests.post.id}/': 'posts/post_detail.html',
            f'/profile/auth/': 'posts/profile.html',
        }
        for address, template in templates_urls_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template, f'Mistake in {address}')

    # проверка urls для неавторизованного пользователя
    def test_urls_uses_correct_template(self):
        templates_urls_names = {
            '/group/test_slug/': 'posts/group_list.html',
            '': 'posts/index.html',
            f'/posts/{PostURLTests.post.id}/': 'posts/post_detail.html',
            f'/profile/auth/': 'posts/profile.html',
        }
        for address, template in templates_urls_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template, f'Mistake in {address}')

    def test_urls_status_code_auth(self):
        urls_status_codes = {
            '': HTTPStatus.OK,
            f'/profile/auth/': HTTPStatus.OK,
            '/create/': HTTPStatus.OK,
            '/group/test_slug/': HTTPStatus.OK,
            f'/posts/{PostURLTests.post.id}/': HTTPStatus.OK,
            f'/posts/{PostURLTests.post.id}/edit/': HTTPStatus.FOUND,
            f'/unexisting_page/': HTTPStatus.NOT_FOUND

        }

        for address, status_code in urls_status_codes.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, status_code)

    def test_urls_status_codes(self):
        urls_status_codes = {
            '/group/test_slug/': HTTPStatus.OK,
            '': HTTPStatus.OK,
            f'/posts/{PostURLTests.post.id}/': HTTPStatus.OK,
            f'/profile/auth/': HTTPStatus.OK,
            f'/posts/{PostURLTests.post.id}/edit/': HTTPStatus.FOUND,
            f'/unexisting_page/': HTTPStatus.NOT_FOUND

        }
        for address, status_code in urls_status_codes.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status_code)

    def test_urls_available_author(self):
        author = PostURLTests.client
        response = author.get(f'/posts/{PostURLTests.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_redirect_anonymous_on_login(self):
        urls_names = [
            '/create/',
            f'/posts/{PostURLTests.post.id}/edit/',
        ]
        for address in urls_names:
            with self.subTest(address=address):
                response = self.guest_client.get(address, follow=True)
                self.assertRedirects(response, (f'/auth/login/?next={address}'))

    def test_url_redirect(self):
        address = f'/posts/{PostURLTests.post.id}/edit/'
        response = self.authorized_client.get(address, follow=True)
        self.assertRedirects(response, f'/posts/{PostURLTests.post.id}/')


