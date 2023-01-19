from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


class UsersInfo(AbstractUser):
    username = models.CharField(max_length=50, verbose_name='Логин', unique=True)
    email = models.CharField(max_length=50, verbose_name='Email', unique=True, default="")
    first_name = models.CharField(max_length=50, verbose_name='Имя', default="")
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', default="")
    password1 = models.CharField(max_length=50, verbose_name='Пароль', default="")
    password2 = models.CharField(max_length=50, verbose_name='Повтор пароля', default="")
    sex = models.CharField(max_length=1, choices=(('F', 'Женский'), ('M', 'Мужской ')), default='F', verbose_name='Пол')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', default=0)

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