from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Subscription(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='follower')

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

        # проверка на уже существующую подписку
        constraints = [models.UniqueConstraint(fields=['author', 'follower'],
                                               name='unique_follow')]

    # def __str__(self):
    #     return str(self.id)
