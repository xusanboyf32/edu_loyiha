from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('courses/', views.courses, name='courses'),
    path('students/', views.students, name='students'),
    path('quests/', views.quests, name='quests'),
    path('video-lessons/', views.video_lessons, name='video_lessons'),
    path('video/edit/<int:pk>/', views.video_edit, name='video_edit'),
    path('video/delete/<int:pk>/', views.video_delete, name='video_delete'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]