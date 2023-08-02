from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase, Client
from .models import Post, Category, Comment, Profile
from django.urls import reverse

from .views import Home


class TestHomeView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        cls.user = User.objects.create_user(**cls.credentials)
        cls.category = Category.objects.create(name='Test category')
        cls.post = Post.objects.create(title='Test post',
                                       author=cls.user,
                                       body='Test body',
                                       category=cls.category)

    def setUp(self):
        self.logged_in = self.client.login(**self.credentials)

    def test_login(self):
        self.assertTrue(bool(self.logged_in), True)

    def test_home_response(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 1)


class TestPostCreateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        cls.user = User.objects.create_user(**cls.credentials)
        cls.category = Category.objects.create(name='Test category')

    def setUp(self):
        self.client.login(**self.credentials)

    def test_creation_of_post(self):
        title = 'TitlePost'
        category_id = self.category.id

        response = self.client.post('/add_post/', {'title': title,
                                                   'body': 'BodyPost',
                                                   'category': category_id})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, title)


class TestEditPostView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.bio = 'Bio of user profile'
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        cls.user = User.objects.create_user(**cls.credentials)
        cls.category = Category.objects.create(name='Test category')
        cls.post = Post.objects.create(title='Test post',
                                       author=cls.user,
                                       body='Test body',
                                       category=cls.category)
        cls.profile = Profile.objects.create(bio=cls.bio, user=cls.user)

    def setUp(self):
        self.client.login(**self.credentials)

    def test_edit_post(self):
        new_title = 'NewPostTitle'

        response = self.client.post(reverse('edit_post',
                                            kwargs={'pk': self.post.id}),
                                    {'title': new_title,
                                     'body': self.post.body,
                                     'category': self.category.id})

        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        # expects to be updated with the new_title.
        self.assertEqual(self.post.title, new_title)


class TestDeletePostView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.bio = 'Bio of user profile'
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        cls.user = User.objects.create_user(**cls.credentials)
        cls.category = Category.objects.create(name='Test category')
        cls.post = Post.objects.create(title='Test post',
                                       author=cls.user,
                                       body='Test body',
                                       category=cls.category)

    def setUp(self):
        self.client.login(**self.credentials)

    def test_delete_post(self):
        response = self.client.delete(reverse('delete_post',
                                              kwargs={'pk': self.post.id}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.exists(), False)


class TestImportPostView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        cls.user = User.objects.create_user(**cls.credentials)
        cls.category = Category.objects.create(name='Test category')

    def setUp(self):
        self.client.login(**self.credentials)

    def test_import_post_from_md_file(self):
        file = open("blog/fixtures/Test.md", 'r')
        response = self.client.post('/import_post/',
                                    {'title': 'Test Title',
                                     'import_post': file,
                                     'category': self.category.id})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().body, '<h4>Hello World</h4>')

    def test_import_post_from_txt_file(self):
        file = open("blog/fixtures/Test.txt", 'r')
        response = self.client.post('/import_post/',
                                    {'title': 'Test Title',
                                     'import_post': file,
                                     'category': self.category.id})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().body, 'Test text txt file.')
