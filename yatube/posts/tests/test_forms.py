import shutil

import tempfile

from ..forms import PostForm

from ..models import Group, Post

from django.conf import settings

from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import Client, TestCase, override_settings

from django.urls import reverse


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Post.objects.create(
            title='Тестовый заголовок',
            text='Тестовый текст',
            slug='first'
        )
        cls.form = PostCreateForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()

    def test_create_post(self):
        """Валидная форма создает новый пост."""
        post_count = Post.objects.count()  
        small_gif = (            
             b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'title': 'Тестовый заголовок',
            'text': 'Тестовый текст',
            'image': uploaded,
        }
        response = self.guest_client.post(
            reverse('post:create_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:profile'))
        self.assertEqual(Post.objects.count(), post_count+1)
        self.assertTrue(
            Post.objects.filter(
                slug='testovyij-zagolovok',
                text='Тестовый текст',
                image='tasks/small.gif'
            ).exists()
        )

    def test_cant_create_existing_slug(self):
        post_count = Post.objects.count()
        form_data = {
            'title': 'Заголовок из формы',
            'text': 'Текст из формы',
            'slug': 'first',
        }
        response = self.guest_client.post(
            reverse('posts:create_post'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), post_count)
        self.assertFormError(
            response, 
            'form',
            'slug',
            'Адрес "first" уже существует, придумайте уникальное значение'
        )
        self.assertEqual(response.status_code, 200)

    def test_post_edit(self):
        """Валидная форма редактирует пост."""
        post_count = Post.objects.count()  
        small_gif = (            
             b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'title': 'Тестовый заголовок два',
            'text': 'Тестовый текст второй',
            'image': uploaded,
        }
        response = self.guest_client.post(
            reverse('post:post_edit', args=('post_id')),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:post_detail'))
        self.assertEqual(Post.objects.count(), post_count+1)
        self.assertTrue(
            Post.objects.filter(
                slug='testovyij-zagolovok-dva',
                text='Тестовый текст второй',
                image='tasks/small.gif'
            ).exists()
        )

    