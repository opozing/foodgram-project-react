from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from users.models import Subscription


class UrlsViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create(username="sergey",
                                       password='test')
        cls.url_users = ('/api/users/')
        cls.url_users2 = ('/api/users/2/')
        cls.url_users1_subscribe = ('/api/users/1/subscribe/')
        cls.url_users2_subscribe = ('/api/users/2/subscribe/')

        cls.user2_create_data = {
            'email': 'test@email.ru',
            'username': 'test_username',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password': 'test_password',
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = APIClient()
        # self.authorized_client.force_login(self.user)
        self.authorized_client.force_authenticate(self.user)

    def test_create_user_unauthorized_user(self):
        """
        Проверка регистрации нового юзера Неавторизованным юзером.
        """
        self.assertEqual(User.objects.count(), 1)
        response = self.guest_client.post(self.url_users,
                                          data=self.user2_create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_create_user_unauthorized_user_double(self):
        """
        Проверка регистрации дубликата уже имеющегося юзера
        Неавторизованным юзером.
        """
        self.assertEqual(User.objects.count(), 1)
        response = self.guest_client.post(self.url_users,
                                          data=self.user2_create_data)
        self.assertEqual(User.objects.count(), 2)
        response = self.guest_client.post(self.url_users,
                                          data=self.user2_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)

    def test_delete_outsider_user_by_unauthorized_user(self):
        """
        Проверка удаления стороннего юзера Неавторизованным юзером.
        """
        response = self.guest_client.post(self.url_users,
                                          data=self.user2_create_data)
        self.assertEqual(User.objects.count(), 2)
        response = self.guest_client.delete(self.url_users2)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_outsider_user_by_self_user(self):
        """
        Проверка удаления стороннего юзера авторизованным юзером.
        """
        response = self.guest_client.post(self.url_users,
                                          data=self.user2_create_data)
        self.assertEqual(User.objects.count(), 2)
        response = self.authorized_client.delete(self.url_users2)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_subscription_unauthorized_user(self):
        """
        Проверка создания подписки Неавторизованным юзером.
        """
        response = self.guest_client.post(self.url_users,
                                          data=self.user2_create_data)
        self.assertEqual(Subscription.objects.count(), 0)
        response = self.guest_client.get(self.url_users2_subscribe)
        self.assertEqual(Subscription.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_subscription_unauthorized_user(self):
        """
        Проверка удаления чужой подписки Неавторизованным юзером.
        """
        response = self.guest_client.post(self.url_users,
                                          data=self.user2_create_data)
        response = self.authorized_client.get(self.url_users2_subscribe)
        self.assertEqual(Subscription.objects.count(), 1)
        response = self.guest_client.delete(self.url_users2_subscribe)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_subscription_authorized_user(self):
        """
        Проверка создания подписки авторизованным юзером.
        """
        response = self.guest_client.post(self.url_users,
                                          data=self.user2_create_data)
        self.assertEqual(User.objects.count(), 2)
        response = self.authorized_client.get(self.url_users2_subscribe)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.get().author.username,
                         'test_username')

    def test_delete_subscription_authorized_user(self):
        """
        Проверка удаления подписки авторизованным юзером.
        """
        response = self.guest_client.post(self.url_users,
                                          data=self.user2_create_data)
        response = self.authorized_client.get(self.url_users2_subscribe)
        self.assertEqual(Subscription.objects.count(), 1)
        response = self.authorized_client.delete(self.url_users2_subscribe)
        self.assertEqual(Subscription.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_outside_subscription_authorized_user(self):
        """
        Проверка удаления не существующей подписки авторизованным юзером.
        """
        response = self.guest_client.post(self.url_users,
                                          data=self.user2_create_data)
        self.assertEqual(Subscription.objects.count(), 0)
        response = self.authorized_client.delete(self.url_users2_subscribe)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_self_subscription_authorized_user(self):
        """
        Проверка создания подписки на себя самого авторизованным юзером.
        """
        self.assertEqual(Subscription.objects.count(), 0)
        response = self.authorized_client.get(self.url_users1_subscribe)
        self.assertEqual(Subscription.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
