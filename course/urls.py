from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    HighTeacherViewSet,
    AssistantTeacherViewSet,
    GroupViewSet,
    VideoLessonViewSet,
    TaskViewSet,
    StudentVideoListView,
    SubmitTaskView, NotionURLViewSet, TeacherCommentViewSet,
    KnescopeVideoUrlViewSet,
    home_page
)

# ------------------ Router yaratish ------------------
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'high-teachers', HighTeacherViewSet, basename='highteacher')
router.register(r'assistant-teachers', AssistantTeacherViewSet, basename='assistantteacher')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'video-lessons', VideoLessonViewSet, basename='videolesson')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'notion', NotionURLViewSet,basename='notionurl')
router.register(r'comment',TeacherCommentViewSet, basename='comment')
router.register(r'kinescope', KnescopeVideoUrlViewSet, basename='kinescopeurl')

# ------------------ URL patterns ------------------
urlpatterns = [
    # Asosiy sahifa
    path('', home_page, name='home'),
    
    # Router orqali avtomatik CRUD URL-lar
    path('api/', include(router.urls)),

    # Talaba uchun video ro'yxati
    path('api/student/videos/', StudentVideoListView.as_view(), name='student-video-list'),

    # Talaba vazifa yuklash (SubmitTaskView)
    path('api/student/videos/<int:video_lesson_id>/submit-task/', SubmitTaskView.as_view(), name='submit-task')
]

