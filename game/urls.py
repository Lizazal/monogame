from django.urls import path
from .views import *

urlpatterns = [
    path('', LoginUser.as_view(), name='login'),
    path('login/', LoginUser.as_view(), name='login'),  # http://127.0.0.1:8000/login
    path('register/', RegisterUser.as_view(), name='register'),  # http://127.0.0.1:8000/register
    path('monotony_game/', monotony_game_page, name='monotony_game'),  # http://127.0.0.1:8000/monotony_game
    path('choose/', choose_page, name='choose'),
    path('choose_train/', choose_train_page, name='choose_train'),
    path('choose_game/', choose_game_page, name='choose_game'),
    path('monotony_train/', monotony_train_page, name='monotony_train'),
    path('stress_train/', stress_train_page, name='stress_train'),
    path('stress_game/', stress_game_page, name='stress_game'),
    path('logout/', logout_user, name='logout'),

    path('save_data/', save_data, name='save_data'),   # 保存玩家游戏精准度接口
    path('info_game/', info_game, name='info_game'),   # 显示玩家信息接口
    path('ranking/', ranking, name='ranking'),   # 显示玩家排名接口

]
