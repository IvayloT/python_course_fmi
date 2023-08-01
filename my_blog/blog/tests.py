from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase, Client
from .models import Post, Category, Comment, Profile
from django.urls import reverse

from .views import Home


class TestHomeView(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        self.category = Category.objects.create(name='Test category')
        self.post = Post.objects.create(title='Test post', author=self.user, body = 'Test body', category=self.category)

    def test_login(self):
        client = Client()
        logged_in = client.login(username='testuser', password='secret')
        self.assertTrue(bool(logged_in), True)

    def test_home_response(self):
        client = Client()
        client.login(username='testuser', password='secret')
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 1)

class TestPostCreateView(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        self.category = Category.objects.create(name='Test category')

    def test_creation_of_post(self):
        client = Client()
        client.login(username='testuser', password='secret')
        title = 'TitlePost'

        response = client.post('/add_post/', {'title': title, 'body': 'BodyPost', 'category': Category.objects.last().id })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, title)

class TestEditPostView(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        self.category = Category.objects.create(name='Test category')
        Profile.objects.create(bio='Bio of user profile', user=self.user)

    def test_edit_post(self):
        body = 'Test body'
        new_title = 'NewPostTitle'
        post = Post.objects.create(title='Test post', author=self.user, body = body, category=self.category)
        client = Client()
        client.login(**self.credentials)

        response = client.post(reverse('edit_post', kwargs={'pk': post.id}),
                               {'title': new_title, 'body': 'BodyPost', 'category': self.category.id })

        post.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(post.title, new_title) # expects to be updated with the new_title.
