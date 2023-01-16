from django.contrib.auth.models import AbstractUser
from django.db import models


class UsersInfo(AbstractUser):

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['last_name']


class OperatingAccuracy(models.Model):
    user = models.ForeignKey(UsersInfo, on_delete=models.CASCADE)
    left_accuracy = models.FloatField()
    middle_accuracy = models.FloatField()
    right_accuracy = models.FloatField()


class State(models.Model):
    user = models.ForeignKey(UsersInfo, on_delete=models.CASCADE)
    previous_stressIndex = models.FloatField()
    after_stressIndex = models.FloatField()
    start_lf_hf = models.FloatField()
    end_lf_hf = models.FloatField()


class Result(models.Model):
    user = models.ForeignKey(UsersInfo, on_delete=models.CASCADE)
    monotony = models.BooleanField()

