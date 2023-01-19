import json

from django import http
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import RegisterUserForm, LoginUserForm
from .models import OperatingAccuracy
from .utils import *


def monotony_game_page(request):
    return render(request, 'game/monotony_game.html')


def choose_page(request):
    return render(request, 'game/choose.html')


def choose_train_page(request):
    return render(request, 'game/choose_train.html')


def choose_game_page(request):
    return render(request, 'game/choose_game.html')


def monotony_train_page(request):
    return render(request, 'game/monotony_train.html')


def stress_train_page(request):
    return render(request, 'game/stress_train.html')


def stress_game_page(request):
    return render(request, 'game/stress_game.html')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'game/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('choose')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'game/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('choose')


def save_data(request):
    if not request.user.is_authenticated:
        return http.JsonResponse({'code': 403, 'errmsg': '用户未登录，前往登录~~'})
    # 接收参数
    json_dict = json.loads(request.body.decode())
    leftAccuracy = json_dict.get('leftAccuracy')
    middleAccuracy = json_dict.get('middleAccuracy')
    rightAccuracy = json_dict.get('rightAccuracy')
    # print(leftAccuracy, middleAccuracy, rightAccuracy)

    # 校验参数
    if not all([leftAccuracy, middleAccuracy, rightAccuracy]):
        return http.JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})

    try:  # 成功写入
        OperatingAccuracy.objects.create(
            user=request.user,
            left_accuracy=leftAccuracy,
            middle_accuracy=middleAccuracy,
            right_accuracy=rightAccuracy
        )
        return http.JsonResponse({'code': 200, 'errmsg': '再玩一盘！！'})

    except:  # 数据库写入异常
        return http.JsonResponse({'code': 400, 'errmsg': '网络错误，请重试~~'})