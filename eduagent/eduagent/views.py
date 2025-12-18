from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def home(request):
    context = {
        'stats': {
            'total_students': 150,
            'active_courses': 12,
            'completed_quests': 89,
            'avg_progress': 75
        },
        'user_stats': {
            'courses_enrolled': 5,
            'courses_completed': 2,
            'total_points': 850,
            'rank': 'Advanced'
        }
    }
    return render(request, 'index.html', context)

@login_required
def courses(request):
    context = {
        'courses': [
            {
                'id': 1, 
                'name': 'Python Basics', 
                'students': 45, 
                'progress': 80, 
                'status': 'active',
                'description': 'Learn Python programming from scratch',
                'duration': '8 weeks',
                'level': 'Beginner'
            },
            {
                'id': 2, 
                'name': 'Django Framework', 
                'students': 38, 
                'progress': 65, 
                'status': 'active',
                'description': 'Build web applications with Django',
                'duration': '10 weeks',
                'level': 'Intermediate'
            },
            {
                'id': 3, 
                'name': 'JavaScript ES6+', 
                'students': 52, 
                'progress': 90, 
                'status': 'active',
                'description': 'Modern JavaScript development',
                'duration': '6 weeks',
                'level': 'Intermediate'
            },
        ]
    }
    return render(request, 'courses.html', context)

@login_required
def course_detail(request, course_id):
    # Mock course data - in a real app, this would come from the database
    courses_data = {
        1: {
            'id': 1,
            'name': 'Python Basics',
            'description': 'Learn Python programming from scratch',
            'instructor': 'John Doe',
            'duration': '8 weeks',
            'level': 'Beginner',
            'students': 45,
            'rating': 4.7,
            'status': 'active',
            'start_date': '2023-11-01',
            'end_date': '2023-12-20'
        },
        2: {
            'id': 2,
            'name': 'Django Framework',
            'description': 'Build web applications with Django',
            'instructor': 'Jane Smith',
            'duration': '10 weeks',
            'level': 'Intermediate',
            'students': 38,
            'rating': 4.8,
            'status': 'active',
            'start_date': '2023-11-15',
            'end_date': '2024-01-15'
        },
        3: {
            'id': 3,
            'name': 'JavaScript ES6+',
            'description': 'Modern JavaScript development',
            'instructor': 'Mike Johnson',
            'duration': '6 weeks',
            'level': 'Intermediate',
            'students': 52,
            'rating': 4.9,
            'status': 'active',
            'start_date': '2023-12-01',
            'end_date': '2024-01-12'
        }
    }
    
    course = courses_data.get(course_id)
    if not course:
        messages.error(request, 'Курс не найден')
        return redirect('courses')
        
    return render(request, 'course_detail.html', {'course': course})

@login_required
def course_edit(request, course_id):
    # In a real app, this would handle form submission to update a course
    messages.success(request, f'Курс {course_id} успешно обновлен')
    return redirect('courses')

@login_required
def course_delete(request, course_id):
    # In a real app, this would delete the course from the database
    messages.success(request, f'Курс {course_id} успешно удален')
    return redirect('courses')

@login_required
def students(request):
    context = {
        'students': [
            {'id': 1, 'user': {'username': 'johndoe', 'email': 'john@example.com'}, 'enrolled_courses': [1, 2, 3], 'avg_progress': 75, 'is_active': True},
            {'id': 2, 'user': {'username': 'janesmith', 'email': 'jane@example.com'}, 'enrolled_courses': [1, 2], 'avg_progress': 85, 'is_active': True},
        ],
        'courses': [
            {'id': 1, 'name': 'Python Basics'},
            {'id': 2, 'name': 'Django Framework'},
            {'id': 3, 'name': 'JavaScript ES6+'}
        ]
    }
    return render(request, 'students.html', context)

def student_detail(request, pk):
    # In a real application, this would fetch the student by ID
    student = {
        'id': pk,
        'user': {'username': 'johndoe', 'email': 'john@example.com'},
        'enrolled_courses': [1, 2, 3],
        'avg_progress': 75,
        'is_active': True,
        'courses': [
            {'id': 1, 'name': 'Python Basics', 'progress': 80},
            {'id': 2, 'name': 'Django Framework', 'progress': 60},
            {'id': 3, 'name': 'JavaScript ES6+', 'progress': 85}
        ]
    }
    return render(request, 'student_detail.html', {'student': student})

def student_edit(request, pk):
    # In a real application, this would handle the student edit form
    if request.method == 'POST':
        # Process form data and save
        messages.success(request, 'Данные студента успешно обновлены!')
        return redirect('student_detail', pk=pk)
    
    # For GET request, show the edit form
    student = {
        'id': pk,
        'user': {'username': 'johndoe', 'email': 'john@example.com'},
        'first_name': 'John',
        'last_name': 'Doe',
        'is_active': True
    }
    return render(request, 'student_form.html', {
        'student': student,
        'title': 'Редактировать студента'
    })

def student_delete(request, pk):
    # In a real application, this would delete the student
    if request.method == 'POST':
        messages.success(request, 'Студент успешно удален!')
        return redirect('students')
    
    # For GET request, show the confirmation page
    return render(request, 'student_confirm_delete.html', {
        'student': {'id': pk, 'user': {'username': 'johndoe'}}
    })

@login_required
def quests(request):
    context = {
        'quests': [
            {'id': 1, 'title': 'Complete Python Course', 'points': 100, 'difficulty': 'medium', 'status': 'active', 'deadline': '2023-12-31', 'course': {'name': 'Python Basics'}},
            {'id': 2, 'title': 'Submit 5 Assignments', 'points': 50, 'difficulty': 'easy', 'status': 'active', 'deadline': '2023-12-15', 'course': {'name': 'Django Framework'}},
        ]
    }
    return render(request, 'quests.html', context)

@login_required
def quest_create(request):
    if request.method == 'POST':
        # In a real application, this would save the new quest to the database
        # For now, we'll just redirect back to the quests list
        messages.success(request, 'Задание успешно создано!')
        return redirect('quests')
    
    # In a real application, you would pass a form and any other required context
    return render(request, 'quest_form.html', {
        'title': 'Создать новое задание',
        'courses': [
            {'id': 1, 'name': 'Python Basics'},
            {'id': 2, 'name': 'Django Framework'},
            {'id': 3, 'name': 'JavaScript ES6+'}
        ]
    })

@login_required
def video_lessons(request):
    context = {
        'videos': [
            {'id': 1, 'title': 'Introduction to Python', 'duration': '15:30', 'views': 120, 'course': {'name': 'Python Basics'}},
            {'id': 2, 'title': 'Django Models', 'duration': '22:45', 'views': 98, 'course': {'name': 'Django Framework'}},
        ]
    }
    return render(request, 'video_lessons.html', context)

@login_required
def video_edit(request, pk):
    # In a real application, this would fetch the video by ID and handle the form
    # For now, we'll just redirect back to the video list
    return redirect('video_lessons')

@login_required
def video_delete(request, pk):
    # In a real application, this would delete the video with the given ID
    # For now, we'll just redirect back to the video list
    return redirect('video_lessons')

@login_required
def profile(request):
    context = {
        'user': request.user,  # Explicitly pass the user object
        'user_stats': {
            'courses_enrolled': 5,
            'courses_completed': 2,
            'total_points': 850,
            'rank': 'Advanced'
        }
    }
    return render(request, 'profile.html', context)

def settings_view(request):
    if request.method == 'POST':
        user = request.user
        
        # Update basic user info
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        
        # Handle phone number (assuming you have a UserProfile model with a OneToOneField to User)
        if hasattr(user, 'profile'):
            user.profile.phone = request.POST.get('phone', user.profile.phone)
        
        # Handle password change if all password fields are filled
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if current_password and new_password and confirm_password:
            # Verify current password
            if not user.check_password(current_password):
                messages.error(request, 'Текущий пароль введен неверно')
                return render(request, 'settings.html', {'user': user})
            
            # Check if new passwords match
            if new_password != confirm_password:
                messages.error(request, 'Новые пароли не совпадают')
                return render(request, 'settings.html', {'user': user})
            
            # Check password strength (min 8 chars, etc.)
            if len(new_password) < 8:
                messages.error(request, 'Пароль должен содержать минимум 8 символов')
                return render(request, 'settings.html', {'user': user})
            
            # Set new password
            user.set_password(new_password)
            
        try:
            user.save()
            if hasattr(user, 'profile'):
                user.profile.save()
            
            # If password was changed, user needs to log in again
            if current_password and new_password and confirm_password:
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, user)  # Keep the user logged in
                messages.success(request, 'Настройки и пароль успешно обновлены!')
            else:
                messages.success(request, 'Настройки успешно обновлены!')
                
            return redirect('settings')
            
        except Exception as e:
            messages.error(request, f'Произошла ошибка при обновлении настроек: {str(e)}')
            return render(request, 'settings.html', {'user': user})
    
    # GET request - just show the form
    return render(request, 'settings.html', {'user': request.user})

def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
