# -*- coding: utf-8 -*-

from django.conf.urls import url

from account import login_views, login_render
from competition import game_views, set_views, rank_views
from business import biz_views
from django.urls import path,re_path

# account
urlpatterns = [
    path('login_normal', login_views.normal_login, name='normal_login'),
    path('login_redirect', login_views.login_redirect, name='index'),
    path('login_vcode', login_views.login_vcode, name='login_vcode'),
    path('signup_normal', login_views.signup, name='normal_signup'),
    path('sendmail', login_views.sendmail, name='sendmail'),
    path('changepasswd', login_views.change_password, name='changepasswd'),
    path('updateprofile', login_views.update_profile, name='updateprofile'),
]

# game
urlpatterns += [
    path('questions', game_views.get_questions, name='get_questions'),
    path('answer', game_views.submit_answer, name='submit_answer'),
    path('entry', game_views.userinfo_entry, name='userinfo_entry'),
    # re_path('games/s/(\w+)', game_views.games, name='query_games'),
    path('qa_history_data', game_views.qa_history_data, name='qa_history_data'),
]

# set
urlpatterns += [
    re_path('query_banks', set_views.banks, name='query_banks'),
    path('get_a_bank', set_views.get_a_bank, name='get_a_bank'),
    re_path('banks/detail/(?P<bank_id>\w+)', set_views.bank_detail, name='bank_detail'),
    path('banks/set', set_views.set_bank, name='set_bank'),
    path('game_list_data', set_views.game_list_data, name='game_list_data'),
    path('update_competition_kind_info', set_views.update_competition_kind_info, name='update_competition_kind_info'),
]

# rank
urlpatterns += [
    path('myrank', rank_views.get_my_rank, name='my_rank'),
]

# bussiness
urlpatterns += [
    path('regbiz', biz_views.registry_biz, name='registry biz'),
    path('checkbiz', biz_views.check_biz, name='check_biz'),
]