from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Subscription
from users.serializers import (SubscriptionSerializer)


class UserSerializerTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create(username="sergey")
        cls.user2 = User.objects.create(username="test")

    def setUp(self):
        self.data = {
            'author': self.user.id,
            'follower': self.user2.id
        }

    def test_subscriprion_serializer_create_object(self):
        """
        Проверка создания подписки сериализатором.
        """
        self.assertEqual(Subscription.objects.count(), 0)
        serializer = SubscriptionSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(Subscription.objects.get(id=1).author.username,
                         self.user.username)

    def test_subscriprion_serializer_create_object_double(self):
        """
        Проверка создания повторной подписки сериализатором.
        """
        serializer = SubscriptionSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(Subscription.objects.count(), 1)
        serializer = SubscriptionSerializer(data=self.data)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(serializer.is_valid(), False)
