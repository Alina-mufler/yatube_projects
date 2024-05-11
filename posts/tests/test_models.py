from django.test import TestCase, Client
from posts.models import Group, Post
from django.contrib.auth import get_user_model

User = get_user_model()


class ModelsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Сообщество программистов',
            description='Привет, добавляйся, если ты любишь писать код',
            slug='programmers'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост'
        )

    def test_models_have_correct_object_names(self):
        post = ModelsTest.post
        group = ModelsTest.group
        models = [post, group]
        expected_object_names = [post.text[:15], group.title]
        for mod, exp_obj_name in zip(models, expected_object_names):
            with self.subTest(field=exp_obj_name):
                self.assertEqual(exp_obj_name, str(mod))

    def test_help_text_post(self):
        post = ModelsTest.post
        field_help_text = {
            'text': 'Напишите текст, который хотите опубликовать',
            'group': 'Выберите группу'
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(post._meta.get_field(field).help_text, expected_value)

    def test_verbose_name_post(self):
        post = ModelsTest.post
        field_verboses = {
            'text' : 'Текст поста',
            'pub_date': 'Дата публикации',
            'group': 'Группа',
            'author': 'Автор'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(post._meta.get_field(field).verbose_name, expected_value)