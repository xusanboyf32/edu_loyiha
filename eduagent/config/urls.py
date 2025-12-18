from django.contrib import admin
from authentication.views import telegram_login, telegram_callback, login_view
from django.urls import path, include, re_path
from django.conf import settings as django_settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from eduagent import views
from eduagent.views import (
    home, courses, students, video_lessons, 
    profile, settings_view, quests, quest_create,
    student_detail, student_edit, student_delete,
    course_detail, course_edit, course_delete
)

<<<<<<< HEAD
# Swagger/OpenAPI configuration
=======
from .course.views import home_page

# ---------------- Swagger sozlamalari ----------------
>>>>>>> 13227d2d9d78bdc73efe4d2e90c24386fc663e72
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
<<<<<<< HEAD
    
    # Authentication
    path('login/', login_view, name='login'),
    
    # Main pages
    path('', home, name='index'),
    path('dashboard/', home, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('courses/', courses, name='courses'),
    path('students/', students, name='students'),
    path('video-lessons/', video_lessons, name='video_lessons'),
    path('settings/', settings_view, name='settings'),
    
    # Quests
    path('quests/', quests, name='quests'),
    path('quests/create/', quest_create, name='quest_create'),
    
    # API
    path('api/auth/', include('authentication.urls')),
    path('api/auth/', include('rest_framework.urls')),
    
    # Course API
=======
    path('admin/', admin.site.urls),

    # DRF login/logout sahifasi
    path('api/auth/', include('rest_framework.urls')),

    # Authentication app (check-auth, logout va hokazo)
    path('api/account/', include('authentication.urls')),

    # COURSE app uchun API
>>>>>>> 13227d2d9d78bdc73efe4d2e90c24386fc663e72
    path('api/course/', include(('course.urls', 'course'), namespace='course')),
    
    # Course management
    path('courses/<int:course_id>/', course_detail, name='course_detail'),
    path('courses/<int:course_id>/edit/', course_edit, name='course_edit'),
    path('courses/<int:course_id>/delete/', course_delete, name='course_delete'),
    
    # Student Management
    path('students/<int:pk>/', student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', student_delete, name='student_delete'),
    
    # Student API
    path('api/student/', include(('student.urls', 'student'), namespace='student')),
<<<<<<< HEAD
    
    # API Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('auth/telegram/login/', telegram_login, name='telegram_login'),
    path('auth/telegram/callback/', telegram_callback, name='telegram_callback'),
=======

    # Frontend bitta template orqali
    path('', home_page, name='home'),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
>>>>>>> 13227d2d9d78bdc73efe4d2e90c24386fc663e72
]

# Media files in development
if django_settings.DEBUG:
    urlpatterns += static(django_settings.MEDIA_URL, document_root=django_settings.MEDIA_ROOT)
