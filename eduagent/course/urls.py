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
    SubmitTaskView, NotionURLViewSet, TeacherCommentViewSet
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


from .authentication.views import telegram_callback

# ------------------ URL patterns ------------------
urlpatterns = [
    # Router orqali avtomatik CRUD URL-lar
    path('', include(router.urls)),

    # Talaba uchun video ro'yxati
    path('student/videos/', StudentVideoListView.as_view(), name='student-video-list'),

    # Talaba vazifa yuklash (SubmitTaskView)
    path('student/videos/<int:video_lesson_id>/submit-task/', SubmitTaskView.as_view(), name='submit-task'),

    path('auth/telegram/callback/', telegram_callback, name='telegram_callback')

]

