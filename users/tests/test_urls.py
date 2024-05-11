from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model

User = get_user_model()


class UsersUrlsTest(TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     pass

    def setUp(self):
        self.gues_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        urls_template_names = {
            '/auth/login/': 'users/login.html',
            '/auth/signup/': 'users/signup.html',
            '/auth/logout/': 'users/logged_out.html',
            # '/auth/password_change/': 'users/password_change_form.html',
            # '/auth/password_change/done/': 'users/password_change_done.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            # '/reset/<uidb64>/<token>/': 'users/password_reset_confirm.html',
            # 'reset/done/': 'users/password_reset_complete.html',
        }

        for address, template in urls_template_names.items():
            with self.subTest(address=address):
                response = self.gues_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_uses_auth_correct_template(self):
        urls_template_names = {
            '/auth/login/': 'users/login.html',
            '/auth/signup/': 'users/signup.html',
            '/auth/logout/': 'users/logged_out.html',
            '/auth/password_change/': 'users/password_change_form.html',
            '/auth/password_change/done/': 'users/password_change_done.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            # '/reset/<uidb64>/<token>/': 'users/password_reset_confirm.html',
            # 'reset/done/': 'users/password_reset_complete.html',
        }

        for address, template in urls_template_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_status_codes(self):
        pass
