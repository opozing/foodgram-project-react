from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Subscription(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор')
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='follower',
                                 verbose_name='Подписчик')

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

        constraints = [models.UniqueConstraint(fields=['author', 'follower'],
                                               name='unique_follow')]

    # def __str__(self):
    #     return str(self.id)
