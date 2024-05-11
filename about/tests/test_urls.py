from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model

User = get_user_model()


class AboutUrlsTest(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.clients = [self.guest_client, self.authorized_client]

    def test_urls_uses_correct_templates(self):
        templates_urls_names = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html'
        }

        for address, template in templates_urls_names.items():
            with self.subTest(address=address):
                for client in self.clients:
                    response = client.get(address)
                    self.assertTemplateUsed(response, template)

    def test_urls_status_codes(self):
        urls_status_codes = {
            '/about/author/': HTTPStatus.OK,
            '/about/tech/': HTTPStatus.OK
        }

        for address, status_code in urls_status_codes.items():
            with self.subTest(address=address):
                for client in self.clients:
                    response = client.get(address).status_code
                    self.assertEqual(response, status_code)
