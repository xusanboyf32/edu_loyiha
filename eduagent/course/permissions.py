
from rest_framework import permissions
from .models import Group

class IsSifatchi(permissions.BasePermission):
    """Faqat sifatchilar uchun"""
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return hasattr(request.user, 'sifatchi_profile')


class IsAssistantTeacher(permissions.BasePermission):
    """Faqat yordamchi ustozlar uchun"""

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return hasattr(request.user, 'assistant_teacher_profile')


class IsHighTeacher(permissions.BasePermission):
    """Faqat katta ustozlar uchun"""

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return hasattr(request.user, 'high_teacher_profile')


class CanUploadVideo(permissions.BasePermission):
    """Video yuklash huquqi - faqat sifatchi"""

    def has_permission(self, request, view):
        if view.action == 'create':
            return hasattr(request.user, 'sifatchi_profile')
        return True


class CanReviewTask(permissions.BasePermission):
    """Vazifani tekshirish huquqi - faqat yordamchi ustoz"""

    def has_permission(self, request, view):
        if view.action in ['review', 'partial_update', 'update']:
            return hasattr(request.user, 'assistant_teacher_profile')
        return True


class IsTaskOwner(permissions.BasePermission):
    """Vazifa egasimi?"""

    def has_object_permission(self, request, view, obj):
        # Talaba faqat o'z vazifasini ko'ra oladi
        if hasattr(request.user, 'student_profile'):
            return obj.student == request.user.student_profile
        return False


class IsGroupMember(permissions.BasePermission):
    """Guruh a'zosimi?"""

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Talaba o'z guruhidagi videolarni ko'ra oladi
        if hasattr(user, 'student_profile'):
            student = user.student_profile
            if student.group:
                return obj.group.filter(id=student.group.id).exists()

        # Yordamchi ustoz o'z guruhlaridagi videolarni ko'ra oladi
        if hasattr(user, 'assistant_teacher_profile'):
            assistant = user.assistant_teacher_profile
            groups = Group.objects.filter(assistant_teacher=assistant)
            return obj.group.filter(id__in=groups).exists()

        # Katta ustoz o'z guruhlaridagi videolarni ko'ra oladi
        if hasattr(user, 'high_teacher_profile'):
            high_teacher = user.high_teacher_profile
            groups = Group.objects.filter(main_teacher=high_teacher)
            return obj.group.filter(id__in=groups).exists()

        return False


# course boyicha permisison
class CourseAdd(permissions.BasePermission):
    """
       Foydalanuvchi:
       - Superuser bo'lsa, hamma CRUD mumkin
       - Sifatchi bo'lsa, hamma CRUD mumkin
       - Boshqalar faqat o'qishi mumkin (GET, HEAD, OPTIONS)
       """

    def has_permission(self, request, view):
        # Superuser bo'lsa hamma narsa mumkin
        if request.user.is_superuser:
            return True

        # Boshqalar faqat safe methods (GET, HEAD, OPTIONS)
        from rest_framework.permissions import SAFE_METHODS
        if request.method in SAFE_METHODS:
            return True

        # Qolganlar hech narsa qila olmaydi (POST, PUT, DELETE)
        return False



# NOTION UCHUN PERMISSION

from rest_framework import permissions

class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Faqat High va Assistant Teacher create/edit/delete qilishi mumkin.
    Talabalar faqat read-only.
    """

    def has_permission(self, request, view):
        user = request.user
        # Teacher bo'lsa hamma metodga ruxsat
        if hasattr(user, 'high_teacher_profile') or hasattr(user, 'assistant_teacher_profile'):
            return True
        # Talaba faqat read
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        # Talabalar faqat read-only
        if request.method in permissions.SAFE_METHODS:
            return True
        # Teacher faqat o'z Notionlarini tahrirlashi mumkin
        user = request.user
        if hasattr(user, 'high_teacher_profile') and obj.main_teacher and obj.main_teacher.user == user:
            return True
        if hasattr(user, 'assistant_teacher_profile') and user.assistant_teacher_profile in obj.assistant_teacher.all():
            return True
        return False



# TEACHER COMMENT YOZISH UCHUN

from rest_framework import permissions

class IsAssistantTeacherOrAdmin(permissions.BasePermission):
    """
    Assistant teacher va admin comment yaratishi, tahrirlashi va o'chirishi mumkin
    """
    def has_permission(self, request, view):
        # create, update, delete uchun
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return hasattr(request.user, 'assistant_teacher_profile') or request.user.is_superuser
        return True

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Comment faqat yozgan assistant teacher yoki admin tahrirlashi mumkin
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Admin har doim CRUD qilishi mumkin
        if request.user.is_superuser:
            return True
        # Assistant teacher faqat o'z yozgan commentiga ruxsat
        return obj.assistant_teacher.user == request.user




#  KINESCOPE UCHUN VIDEO YUKLASH


from rest_framework import permissions, viewsets

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Adminlar CRUD qilishi mumkin,
    boshqalar faqat Read-only.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS (read-only)
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
