import json
import math

from django import http
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import RegisterUserForm, LoginUserForm
from .models import OperatingAccuracy, UsersInfo
from .utils import *


@login_required
def monotony_game_page(request):
    return render(request, 'game/monotony_game.html')


@login_required
def choose_page(request):
    return render(request, 'game/choose.html')


@login_required
def choose_train_page(request):
    return render(request, 'game/choose_train.html')


@login_required
def choose_game_page(request):
    return render(request, 'game/choose_game.html')


@login_required
def monotony_train_page(request):
    return render(request, 'game/monotony_train.html')


@login_required
def stress_train_page(request):
    return render(request, 'game/stress_train.html')


@login_required
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


@login_required
def save_data(request):
    # 校验登录
    if not request.user.is_authenticated:
        return http.JsonResponse({'code': 403, 'errmsg': 'Пользователь не авторизован, авторизуйтесь, пожалуйста~~'})
    # 接收参数
    json_dict = json.loads(request.body.decode())
    leftAccuracy = json_dict.get('leftAccuracy')
    middleAccuracy = json_dict.get('middleAccuracy')
    rightAccuracy = json_dict.get('rightAccuracy')
    OperatingTime = json_dict.get('OperatingTime')
    stress = json_dict.get('stress')
    # print(leftAccuracy, middleAccuracy, rightAccuracy, OperatingTime)

    # 校验参数
    if not all([leftAccuracy, middleAccuracy, rightAccuracy, OperatingTime]):
        return http.JsonResponse({'code': 400, 'errmsg': 'Отсутствует обязательный параметр'})

    if (eval(leftAccuracy) > 0 and eval(middleAccuracy) > 0) \
            or (eval(rightAccuracy) > 0 and eval(middleAccuracy) > 0) \
            or (eval(rightAccuracy) > 0 and eval(leftAccuracy) > 0):
        advantage = '+'
    else:
        advantage = '-'

    # 计算平均值
    mean = (math.fabs(eval(leftAccuracy)) + math.fabs(eval(middleAccuracy)) + math.fabs(eval(rightAccuracy))) / 3

    try:  # 成功写入

        minutes = OperatingTime.split(':')[0]
        s = OperatingTime.split(':')[1]
        total_time = eval(minutes) * 60 + eval(s)
        good = False
        if stress:
            if (abs(eval(leftAccuracy)) < 0.75 or abs(eval(middleAccuracy)) < 0.75 or abs(eval(rightAccuracy)) < 0.75) and (total_time>120):
                good = True
            if good==False:
                return http.JsonResponse({'code': 200, 'errmsg': 'Вы можете сыграть ещё раз!'})
        ope = OperatingAccuracy.objects.create(
            user=request.user,
            left_accuracy=leftAccuracy,
            middle_accuracy=middleAccuracy,
            right_accuracy=rightAccuracy,
            advantage=advantage,
            mean=mean
        )
        # stress有值则为stress_game

        if stress:
            total_time = eval(minutes) * 60 + eval(s)
            level = int(total_time / 120)
            ope.level = str(level)
            ope.save()
            ope.operatingtime_set.create(
                user=request.user,
                time=f'{minutes}минут{s}секунд',

            )

        else:
            if minutes != '0':
                ope.operatingtime_set.create(
                    user=request.user,
                    time=f'{minutes}минут{s}секунд'
                )

        return http.JsonResponse({'code': 200, 'errmsg': 'Вы можете сыграть ещё раз!'})

    except:  # 数据库写入异常
        return http.JsonResponse({'code': 400, 'errmsg': 'Ошибка сети, попробуйте еще раз~~'})


@login_required
def info_game(request):
    user = UsersInfo.objects.get(username=request.user.username)
    operatings = OperatingAccuracy.objects.filter(user=request.user)

    return render(request, 'game/info_game.html', locals())


@login_required
def ranking(request):
    # 校验登录
    if not request.user.is_authenticated:
        return http.JsonResponse({'code': 403, 'errmsg': 'Пользователь не авторизован, авторизуйтесь, пожалуйста~~'})

    # 接收参数
    json_dict = json.loads(request.body.decode())
    meanAccuracy = json_dict.get('mean')
    if len(meanAccuracy) > 3:
        meanAccuracy = meanAccuracy[-3:]

    # 计算平均值
    mean = 0
    for item in meanAccuracy:
        mean += math.fabs(item * 100)
    mean = mean / 3

    # 查询所有数据

    p = []
    # 查询当前用户性别
    sex = request.user.sex
    ope = OperatingAccuracy.objects.filter(user__sex=sex)
    for i in ope:
        p.append(i.mean)
    p.append(mean)

    # 冒泡排序计算排名
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] < p[j]:
                p[i], p[j] = p[j], p[i]

    # print(p)  # 性别的排名结果
    p_mean = p.index(mean) + 1

    # 同性别计算level排名
    L = set()
    level = int(json_dict.get('seconds') / 120)
    ope = ope.filter(user__operatingaccuracy__level=level)
    for i in ope:
        L.add(i.mean)
    L.add(mean)

    L = list(L)
    # 冒泡排序计算排名
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            if L[i] < L[j]:
                L[i], L[j] = L[j], L[i]

    # print(L)  # 性别的排名结果
    p_mean_level = L.index(mean) + 1

    a = []
    # 查询当前用户年龄
    age = request.user.age
    ope1 = OperatingAccuracy.objects.filter(user__age=age)
    for i in ope1:
        a.append(i.mean)
    a.append(mean)

    # 冒泡排序计算排名
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] < a[j]:
                a[i], a[j] = a[j], a[i]

    # print(a)  # 年龄的排名结果
    a_mean = a.index(mean) + 1

    # 同年龄计算level排名
    A = set()
    level = str(int(json_dict.get('seconds') / 120))
    ope1 = ope1.filter(user__operatingaccuracy__level=level)
    for i in ope1:
        A.add(i.mean)
    A.add(mean)

    A = list(A)
    # 冒泡排序计算排名
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            if A[i] < A[j]:
                A[i], A[j] = A[j], A[i]

    # print(A)  # 年龄的排名结果
    a_mean_level = A.index(mean) + 1

    data = {
        'sex': sex,
        'p_mean': p_mean,
        'p_mean_level': p_mean_level,
        'a_mean': a_mean,
        'a_mean_level': a_mean_level
    }

    # print(p)  # 排序排名
    return http.JsonResponse({'code': 200, 'errmsg': 'ok', 'data': data})


def logout_user(request):
    logout(request)
    return redirect('login')
