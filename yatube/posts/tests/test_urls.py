from django.contrib.auth import get_user_model

from django.test import TestCase, Client

from .models import Post, Group

User = get_user_model()



class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Post.objects.create(
            title='Тестовый заголовок',
            text='Тестовый текст',
            slug='test-slug'
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
        response = self.guest_client.get('/group/<slug>/')
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        response = self.guest_client.get('/profile/<str:username>/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail(self):
        response = self.guest_client.get('/posts/<int:post_id>/')
        self.assertEqual(response.status_code, 200)

    def test_unexisting_page(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_create(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit(self):
        response = self.authorized_client.get('/posts/<post_id>/edit/')
        self.assertEqual(response.status_code, 200)


    def test_create_url_redirect_anonymous(self):
        response = self.guest_client.get('/create/')
        self.assertEqual(response.status_code, 302)
            
    def test_post_edit_url_redirect_anonymous(self):
        response = self.client.get('/posts/<post_id>/edit/')
        self.assertEqual(response.status_code, 302)



    def test_create_url_redirect_anonymous_on_admin_login(self):
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/admin/login/?next=/create/'
        )

    def test_post_edit_url_redirect_anonymous_on_admin_login(self):
        response = self.client.get('/posts/<post_id>/edit/', follow=True)
        self.assertRedirects(
            response, ('/admin/login/?next=/posts/<post_id>/edit/')) 



    def test_urls_uses_correct_template(self):
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/<slug>/',
            'posts/profile.html': '/profile/<str:username>/',
            'posts/post_detail.html': '/posts/<int:post_id>/',
            'posts/create_post.html': '/posts/<post_id>/edit/',
            'posts/create_post.html': '/create/',
            '': '/unexisting_page/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)



    