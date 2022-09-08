from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )


    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        expected_object_name = post.title
        self.assertEqual(expected_object_name, str(post)) 


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='З'*200,
            text='Тестовый текст',
            slug='Тестовый слаг'
        )

    def test_text_convert_to_slug(self):
        """Содержимое поля title преобразуется в slug."""
        task = GroupModelTest.group
        slug = group.slug
        self.assertEqual(slug, 'z'*200)

    def test_text_slug_max_length_not_exceed(self):
        """Длинный slug обрезается и не превышает max_length поля slug в модели."""
        task = GroupModelTest.group
        max_length_slug = group._meta.get_field('slug').max_length
        length_slug = len(group.slug)
        self.assertEqual(max_length_slug, length_slug)

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        group = GroupModelTest.group
        field_verboses = {
            'title': 'Название группы',
            'slug': 'slug',
            'description': 'Описание группы',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(group._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        group = GroupModelTest.group
        field_help_text = {
            'title': 'Дайте короткое название группе',
            'description': 'Дайте короткое описание группе',
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(group._meta.get_field(field).help_text, expected_value)



    def test_object_name_is_title_fild(self):
        """__str__  task - это строчка с содержимым task.title."""
        group = GroupModelTest.group  # Обратите внимание на синтаксис
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group)) 