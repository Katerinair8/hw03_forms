from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_list(self):
        slug = PostURLTests.group.slug
        response = self.guest_client.get(f'/group/{slug}/')
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        user = PostURLTests.user
        response = self.guest_client.get(f'/profile/{user}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail(self):
        post_id = PostURLTests.post.id
        response = self.guest_client.get(f'/posts/{post_id}/')
        self.assertEqual(response.status_code, 200)

    def test_unexisting_page(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test__post_create(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit(self):
        post_id = PostURLTests.post.id
        response = self.authorized_client.get(f'/posts/{post_id}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_create_url_redirect_anonymous(self):
        response = self.guest_client.get('/create/')
        self.assertEqual(response.status_code, 302)

    def test_post_edit_url_redirect_anonymous(self):
        post_id = PostURLTests.post.id
        response = self.client.get(f'/posts/{post_id}/edit/')
        self.assertEqual(response.status_code, 302)

    def test_create_url_redirect_anonymous_on_admin_login(self):
        login_url = reverse('users:login')
        post_create_url = reverse('posts:post_create')
        target_url = f'{login_url}?next={post_create_url}'
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, target_url
        )

    def test_post_edit_url_redirect_anonymous_on_admin_login(self):
        post_id = PostURLTests.post.id
        response = self.client.get(f'/posts/{post_id}/edit/', follow=True)
        self.assertRedirects(
            response, (f'/auth/login/?next=/posts/{post_id}/edit/'))

    def test_urls_uses_correct_template(self):
        slug = PostURLTests.group.slug
        post_id = PostURLTests.post.id
        user = PostURLTests.user
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{slug}/': 'posts/group_list.html',
            f'/profile/{user}/': 'posts/profile.html',
            f'/posts/{post_id}/': 'posts/post_detail.html',
            f'/posts/{post_id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(address=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
