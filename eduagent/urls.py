from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('students/', views.students, name='students'),
    path('quests/', views.quests, name='quests'),
    path('video-lessons/', views.video_lessons, name='video_lessons'),
    path('video/edit/<int:pk>/', views.video_edit, name='video_edit'),
    path('video/delete/<int:pk>/', views.video_delete, name='video_delete'),
    path('eduplay/', views.eduplay_exercises, name='eduplay_exercises'),
    path('mini-games/', views.mini_games, name='mini_games'),
    path('shop/', views.shop, name='shop'),
    path('achievements/', views.achievements, name='achievements'),
    path('random-examples/', views.random_examples, name='random_examples'),
    path('random-examples-page/', views.random_examples_page, name='random_examples_page'),
    path('games/play/<int:game_id>/', views.play_game, name='play_game'),
    path('shop/buy/<int:avatar_id>/', views.buy_avatar, name='buy_avatar'),
    path('exercises/', views.exercises, name='exercises'),
    path('exercises/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('settings/', views.settings_view, name='settings'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # REST API endpoints
    path('api/random-examples/', api_views.random_examples_api, name='api_random_examples'),
    path('api/examples-stats/', api_views.examples_stats, name='api_examples_stats'),
    path('api/add-example/', api_views.add_custom_example, name='api_add_example'),
]