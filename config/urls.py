from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings as django_settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import views as auth_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Local views
from eduagent.views import (
    home, courses, students, video_lessons, video_edit, video_delete,
    profile, settings_view, quests, quest_create, quest_edit, quest_delete,
    student_detail, student_edit, student_delete,
    course_detail, course_edit, course_delete, analytics,
    exercises, exercise_detail, eduplay_exercises,
    mini_games, shop, achievements, play_game, buy_avatar, random_examples_page, random_examples
)
from eduagent.api_views import examples_stats
from authentication.views import telegram_login, telegram_callback, login_view, logout_view

# Swagger/OpenAPI configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Education Platform API",
        default_version="v1",
        description="Professional API documentation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Authentication - Redirect old /accounts/ URLs to new ones
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=True)),
    path('accounts/logout/', RedirectView.as_view(url='/logout/', permanent=True)),
    
    # Authentication - Custom views
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Social auth
    path('auth/telegram/login/', telegram_login, name='telegram_login'),
    path('auth/telegram/callback/', telegram_callback, name='telegram_callback'),
    
    # New Telegram Auth with code
    path('auth/', include('authentication.urls')),
    
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/password_reset/done/'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Main pages
    path('', home, name='home'),
    path('dashboard/', home, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('courses/', courses, name='courses'),
    path('students/', students, name='students'),
    path('video-lessons/', video_lessons, name='video_lessons'),
    path('video-lessons/<int:video_id>/edit/', video_edit, name='video_edit'),
    path('video-lessons/<int:video_id>/delete/', video_delete, name='video_delete'),
    path('eduplay/', eduplay_exercises, name='eduplay_exercises'),
    path('mini-games/', mini_games, name='mini_games'),
    path('shop/', shop, name='shop'),
    path('achievements/', achievements, name='achievements'),
    path('random-examples/', random_examples, name='random_examples'),
    path('random-examples-page/', random_examples_page, name='random_examples_page'),
    path('examples-stats/', examples_stats, name='examples_stats'),
    path('games/play/<int:game_id>/', play_game, name='play_game'),
    path('shop/buy/<int:avatar_id>/', buy_avatar, name='buy_avatar'),
    path('exercises/', exercises, name='exercises'),
    path('exercises/<int:exercise_id>/', exercise_detail, name='exercise_detail'),
    path('settings/', settings_view, name='settings'),
    path('analytics/', analytics, name='analytics'),

    # Quests
    path('quests/', quests, name='quests'),
    path('quests/create/', quest_create, name='quest_create'),
    path('quests/<int:quest_id>/edit/', quest_edit, name='quest_edit'),
    path('quests/<int:quest_id>/delete/', quest_delete, name='quest_delete'),

    # API
    path('api/auth/', include('rest_framework.urls')),  # DRF login/logout
    path('api/account/', include('authentication.urls')),  # Authentication API
    path('api/course/', include(('course.urls', 'course'), namespace='course')),
    path('api/student/', include(('student.urls', 'student'), namespace='student')),

    # Course management
    path('courses/<int:course_id>/', course_detail, name='course_detail'),
    path('courses/<int:course_id>/edit/', course_edit, name='course_edit'),
    path('courses/<int:course_id>/delete/', course_delete, name='course_delete'),

    # Student Management
    path('students/<int:pk>/', student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', student_delete, name='student_delete'),

    # API Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Media files in development
if django_settings.DEBUG:
    urlpatterns += static(django_settings.MEDIA_URL, document_root=django_settings.MEDIA_ROOT)
    urlpatterns += static(django_settings.STATIC_URL, document_root=django_settings.STATIC_ROOT)

# Optional AI URL
urlpatterns += [
    path('ai/', include('chatai.urls')),
]
