
from django.contrib import admin
from .models import Course, Group, VideoLesson, Task, Assistant_Teacher, High_Teacher
from student.models import Student

# ================== Student Inline ==================
class StudentInline(admin.TabularInline):
    model = Student
    fk_name = 'assigned_group'  # qaysi field bilan Group bog‘langan
    extra = 0
    readonly_fields = ['full_name', 'phone_number', 'email']
    show_change_link = True  # talaba profiliga tez kirish

# ================== Group Admin ==================
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'main_teacher', 'is_active']
    search_fields = ['name', 'course__name', 'main_teacher__full_name']
    list_filter = ['course', 'is_active']
    filter_horizontal = ['assistant_teacher']  # yordamchi ustozlar qulay tanlanadi
    inlines = [StudentInline]  # guruhdagi talabalar inline ko‘rinadi

# ================== Group Inline for Course ==================
class GroupInline(admin.TabularInline):
    model = Group
    fk_name = 'course'  # group qaysi kursga tegishli
    extra = 0
    readonly_fields = ['name', 'main_teacher', 'is_active']
    show_change_link = True  # guruh paneliga tez kirish

# ================== Course Admin ==================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['is_active']
    inlines = [GroupInline]  # kursga biriktirilgan guruhlar inline ko‘rinadi

# ================== High Teacher Admin ==================
@admin.register(High_Teacher)
class HighTeacherAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'email', 'job', 'experience_year']
    search_fields = ['full_name', 'phone_number', 'email']

# ================== Assistant Teacher Admin ==================
@admin.register(Assistant_Teacher)
class AssistantTeacherAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'email', 'job', 'experience_year']
    search_fields = ['full_name', 'phone_number', 'email']

# ================== Video Lesson Admin ==================
@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_by', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['course', 'group']  # qaysi kurs va guruhga tegishli

# ================== Task Admin ==================
# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ['id', 'video_lesson', 'student', 'assistant_teacher', 'score', 'created_at']
#     search_fields = ['student__full_name', 'video_lesson__title']
#     list_filter = ['assistant_teacher', 'score']


# admin.py
from django.contrib import admin
from .models import NotionURL

@admin.register(NotionURL)
class NotionURLAdmin(admin.ModelAdmin):
    list_display = ('title', 'main_teacher', 'created_at')  # ustunlar
    list_filter = ('main_teacher', 'created_at')  # filterlar
    search_fields = ('title', 'main_teacher__full_name')  # qidiruv



# coment uchun

from django.contrib import admin
from django import forms
from .models import Task

# Admin panelda placeholder ko'rsatish uchun formfield_overrides ishlatamiz
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('student', 'video_lesson', 'title', 'score', 'created_at')
    search_fields = ('student__full_name', 'video_lesson__title', 'title')
    list_filter = ('created_at', 'score')

    # CharField uchun placeholder berish
    formfield_overrides = {
        forms.CharField: {'widget': forms.TextInput(attrs={'placeholder': '1-dars vazifam'})},
    }

# admin.site.register(Task, TaskAdmin)





# course/admin.py
from django.contrib import admin
from .models import Teachercomment

from django.contrib import admin
from .models import Teachercomment

@admin.register(Teachercomment)
class TeacherCommentAdmin(admin.ModelAdmin):
    list_display = ('get_task_id', 'get_video_lesson', 'get_student', 'get_assistant_teacher', 'created_at')
    search_fields = ('task__video_lesson__title', 'task__student__full_name', 'assistant_teacher__full_name')
    list_filter = ('created_at',)

    # Task ID ko'rsatish
    def get_task_id(self, obj):
        return obj.task.id
    get_task_id.short_description = 'Task ID'

    # VideoLesson nomi ko'rsatish
    def get_video_lesson(self, obj):
        return obj.task.video_lesson.title
    get_video_lesson.short_description = 'Vazifa'

    # Student nomi ko'rsatish
    def get_student(self, obj):
        return obj.task.student.full_name
    get_student.short_description = 'Student'

    # Assistant teacher nomi ko'rsatish
    def get_assistant_teacher(self, obj):
        return obj.assistant_teacher.full_name if obj.assistant_teacher else "-"
    get_assistant_teacher.short_description = 'Yozgan Ustoz'
