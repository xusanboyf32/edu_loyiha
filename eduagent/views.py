from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.db import models
from django.utils import timezone
from .models import Exercise, UserExercise, MiniGame, GameResult, Avatar, UserAvatar, UserCoins, Achievement, UserAchievement
import json

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
def quest_edit(request, quest_id):
    # In a real application, this would fetch the quest by ID and handle the form
    # For now, we'll just redirect back to the quests list
    messages.info(request, f'Редактирование задания #{quest_id}')
    return redirect('quests')

@login_required
def quest_delete(request, quest_id):
    # In a real application, this would delete the quest with the given ID
    # For now, we'll just redirect back to the quests list
    messages.warning(request, f'Задание #{quest_id} удалено')
    return redirect('quests')

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
def video_edit(request, video_id):
    # In a real application, this would fetch the video by ID and handle the form
    # For now, we'll just redirect back to the video list
    messages.info(request, f'Редактирование видео #{video_id}')
    return redirect('video_lessons')

@login_required
def video_delete(request, video_id):
    # In a real application, this would delete the video with the given ID
    # For now, we'll just redirect back to the video list
    messages.warning(request, f'Видео #{video_id} удалено')
    return redirect('video_lessons')

@login_required
def analytics(request):
    context = {
        'analytics_data': {
            'total_users': 1250,
            'active_users': 890,
            'new_users_this_month': 45,
            'user_growth': 12.5,
            'course_completion_rate': 78.3,
            'avg_session_duration': '25:30',
            'popular_courses': [
                {'name': 'Python Basics', 'enrollments': 234, 'completion': 85},
                {'name': 'Django Framework', 'enrollments': 189, 'completion': 72},
                {'name': 'JavaScript ES6+', 'enrollments': 156, 'completion': 68}
            ],
            'monthly_stats': [
                {'month': 'Янв', 'users': 980, 'revenue': 12500},
                {'month': 'Фев', 'users': 1020, 'revenue': 13200},
                {'month': 'Мар', 'users': 1150, 'revenue': 14800},
                {'month': 'Апр', 'users': 1200, 'revenue': 15600},
                {'month': 'Май', 'users': 1250, 'revenue': 16500},
                {'month': 'Июн', 'users': 1250, 'revenue': 16500}
            ]
        }
    }
    return render(request, 'analytics.html', context)

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

@login_required
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

@login_required
def mini_games(request):
    """Страница мини-игр"""
    games = MiniGame.objects.all()
    user_results = GameResult.objects.filter(user=request.user)
    
    # Группируем игры по типам зданий
    games_by_building = {}
    for game in games:
        if game.building_type not in games_by_building:
            games_by_building[game.building_type] = []
        games_by_building[game.building_type].append(game)
    
    # Вычисляем статистику
    completed_games = user_results.filter(is_completed=True).count()
    total_coins_earned = user_results.aggregate(total=models.Sum('coins_earned'))['total'] or 0
    average_score = user_results.aggregate(avg=models.Avg('score'))['avg'] or 0
    
    context = {
        'games_by_building': games_by_building,
        'user_results': user_results,
        'total_coins': UserCoins.objects.get_or_create(user=request.user)[0].coins,
        'completed_games': completed_games,
        'total_coins_earned': total_coins_earned,
        'average_score': round(average_score, 1)
    }
    return render(request, 'eduagent/mini_games.html', context)

@login_required
def shop(request):
    """Магазин аватаров"""
    avatars = Avatar.objects.all()
    user_coins, created = UserCoins.objects.get_or_create(user=request.user)
    user_avatars = UserAvatar.objects.filter(user=request.user, is_active=True)
    
    context = {
        'avatars': avatars,
        'user_coins': user_coins.coins,
        'user_avatars': user_avatars
    }
    return render(request, 'eduagent/shop.html', context)

@login_required
def buy_avatar(request, avatar_id):
    """Покупка аватара"""
    if request.method == 'POST':
        avatar = get_object_or_404(Avatar, id=avatar_id)
        user_coins, created = UserCoins.objects.get_or_create(user=request.user)
        
        if user_coins.coins >= avatar.price:
            # Списываем монеты
            user_coins.coins -= avatar.price
            user_coins.total_spent += avatar.price
            user_coins.save()
            
            # Добавляем аватар пользователю
            user_avatar, created = UserAvatar.objects.get_or_create(
                user=request.user,
                avatar=avatar,
                defaults={'is_active': True}
            )
            
            # Если аватар уже был, просто активируем
            if not created:
                # Деактивируем все остальные аватары
                UserAvatar.objects.filter(user=request.user).update(is_active=False)
                user_avatar.is_active = True
                user_avatar.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Аватар "{avatar.name}" успешно куплен!',
                'new_coins': user_coins.coins
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Недостаточно монет!'
            })
    
    return JsonResponse({'success': False, 'message': 'Неверный метод запроса'})

@login_required
def play_game(request, game_id):
    """Играть в мини-игру"""
    game = get_object_or_404(MiniGame, id=game_id)
    
    if request.method == 'GET':
        # Показать страницу игры
        context = {
            'game': game,
            'user_coins': UserCoins.objects.get_or_create(user=request.user)[0].coins
        }
        return render(request, f'eduagent/games/{game.game_type}.html', context)
    
    elif request.method == 'POST':
        # Обработать результат игры
        score = int(request.POST.get('score', 0))
        time_spent = int(request.POST.get('time_spent', 0))
        
        # Начисляем монеты
        coins_earned = game.reward_coins if score > 0 else 0
        
        # Обновляем монеты пользователя
        user_coins, created = UserCoins.objects.get_or_create(user=request.user)
        user_coins.coins += coins_earned
        user_coins.total_earned += coins_earned
        user_coins.save()
        
        # Сохраняем результат игры
        GameResult.objects.create(
            user=request.user,
            game=game,
            score=score,
            coins_earned=coins_earned,
            is_completed=score > 0,
            time_spent=time_spent
        )
        
        # Проверяем достижения
        check_achievements(request.user)
        
        return JsonResponse({
            'success': True,
            'coins_earned': coins_earned,
            'new_total': user_coins.coins,
            'message': f'Отлично! Ты заработал {coins_earned} монет!'
        })

def check_achievements(user):
    """Проверка и выдача достижений"""
    user_coins = UserCoins.objects.get_or_create(user=user)[0]
    user_exercises = UserExercise.objects.filter(user=user, is_completed=True)
    user_games = GameResult.objects.filter(user=user, is_completed=True)
    user_avatars = UserAvatar.objects.filter(user=user)
    
    # Проверяем различные достижения
    achievements = Achievement.objects.all()
    
    for achievement in achievements:
        # Проверяем, не получено ли уже достижение
        if UserAchievement.objects.filter(user=user, achievement=achievement).exists():
            continue
            
        condition = achievement.condition
        earned = False
        
        if condition['type'] == 'first_exercise' and user_exercises.exists():
            earned = True
        elif condition['type'] == 'exercises_count' and condition['category'] == 'math':
            math_exercises = user_exercises.filter(exercise__category='math').count()
            if math_exercises >= condition['count']:
                earned = True
        elif condition['type'] == 'avatars_count' and user_avatars.count() >= condition['count']:
            earned = True
        elif condition['type'] == 'games_played' and user_games.count() >= condition['count']:
            earned = True
        elif condition['type'] == 'coins_earned' and user_coins.total_earned >= condition['amount']:
            earned = True
        elif condition['type'] == 'buildings_completed':
            completed_buildings = set()
            for exercise in user_exercises:
                completed_buildings.add(exercise.exercise.building_type)
            if len(completed_buildings) >= condition['count']:
                earned = True
        
        if earned:
            # Выдаем достижение и награду
            UserAchievement.objects.create(user=user, achievement=achievement)
            user_coins.coins += achievement.reward_coins
            user_coins.total_earned += achievement.reward_coins
            user_coins.save()

@login_required
def random_examples_page(request):
    """Страница случайных примеров"""
    return render(request, 'eduagent/random_examples.html')

@login_required
def random_examples(request):
    """Генератор случайных примеров для EduPlay через REST API"""
    import json
    import os
    from django.conf import settings
    
    try:
        # Путь к файлу с примерами
        examples_file = os.path.join(settings.BASE_DIR, 'random_examples.json')
        
        # Если файла нет, генерируем его
        if not os.path.exists(examples_file):
            from random_examples_generator import RandomExamplesGenerator
            generator = RandomExamplesGenerator()
            examples = generator.save_to_file(examples_file)
        else:
            # Загружаем из файла
            with open(examples_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                examples = data.get('examples', [])
        
        # Перемешиваем примеры для разнообразия
        import random
        random.shuffle(examples)
        
        # Возвращаем JSON
        return JsonResponse({
            'success': True,
            'examples': examples[:20],  # Возвращаем первые 20 примеров
            'total_count': len(examples),
            'source': 'file'
        })
        
    except Exception as e:
        # Если что-то пошло не так, возвращаем базовые примеры
        import random
        
        # Базовые математические примеры
        math_examples = []
        for i in range(10):
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            operation = random.choice(['+', '-', '*', '/'])
            
            if operation == '+':
                result = a + b
                question = f"{a} + {b} = ?"
            elif operation == '-':
                result = a - b
                question = f"{a} - {b} = ?"
            elif operation == '*':
                result = a * b
                question = f"{a} × {b} = ?"
            else:  # деление
                b = random.randint(1, 10)
                a = b * random.randint(1, 10)
                result = a // b
                question = f"{a} ÷ {b} = ?"
            
            math_examples.append({
                'id': f"math_{i}",
                'question': question,
                'answer': str(result),
                'difficulty': 'easy' if result < 20 else 'medium' if result < 50 else 'hard',
                'category': 'math',
                'coins': random.choice([5, 8, 10, 12, 15])
            })
        
        return JsonResponse({
            'success': True,
            'examples': math_examples,
            'total_count': len(math_examples),
            'source': 'fallback',
            'error': str(e)
        })

@login_required
def achievements(request):
    """Страница достижений"""
    user_achievements = UserAchievement.objects.filter(user=request.user).select_related('achievement')
    all_achievements = Achievement.objects.all()
    
    # Разделяем на полученные и не полученные
    earned_ids = [ua.achievement.id for ua in user_achievements]
    available_achievements = all_achievements.exclude(id__in=earned_ids)
    
    context = {
        'user_achievements': user_achievements,
        'available_achievements': available_achievements,
        'total_coins': UserCoins.objects.get_or_create(user=request.user)[0].coins
    }
    return render(request, 'eduagent/achievements.html', context)

@login_required
def eduplay_exercises(request):
    """Задания в стиле EduPlay - Школьный городок"""
    exercises_list = Exercise.objects.all()
    user_exercises = UserExercise.objects.filter(user=request.user)
    completed_exercises = [ue.exercise.id for ue in user_exercises if ue.is_completed]
    
    # Группировка заданий по зданиям
    buildings = {}
    building_types = [
        ('school', '🏫 Школа', 'Основные предметы', '/media/images/logo_falak.png'),
        ('library', '📚 Библиотека', 'Чтение и теория', '/media/images/logo_falak.png'),
        ('lab', '🔬 Лаборатория', 'Наука и эксперименты', '/media/images/logo_falak.png'),
        ('gym', '⚽ Спортзал', 'Физическая активность', '/media/images/logo_falak.png'),
        ('art', '🎨 Арт-студия', 'Творчество', '/media/images/logo_falak.png')
    ]
    
    for building_type, name, description, image in building_types:
        building_exercises = exercises_list.filter(building_type=building_type)
        completed_count = user_exercises.filter(
            exercise__building_type=building_type, 
            is_completed=True
        ).count()
        
        # Подготовка данных для JavaScript
        exercises_data = []
        for exercise in building_exercises:
            exercises_data.append({
                'id': exercise.id,
                'title': exercise.title,
                'description': exercise.description,
                'difficulty': exercise.difficulty,
                'category': exercise.category,
                'points': exercise.points,
                'starter_code': exercise.starter_code or ''
            })
        
        buildings[building_type] = {
            'name': name,
            'description': description,
            'image': image,
            'icon': name.split(' ')[0],
            'exercises_count': building_exercises.count(),
            'completed_count': completed_count,
            'level': 1 if completed_count < 3 else 2 if completed_count < 6 else 3,
            'exercises': exercises_data
        }
    
    # Получаем монеты пользователя
    user_coins, created = UserCoins.objects.get_or_create(user=request.user)
    
    context = {
        'buildings': buildings,
        'total_exercises': exercises_list.count(),
        'completed_exercises': user_exercises.filter(is_completed=True).count(),
        'total_coins': user_coins.coins,
        'unlocked_buildings': len([b for b in buildings.values() if b['completed_count'] > 0]),
        'user_level': 1 if user_exercises.filter(is_completed=True).count() < 5 else 2 if user_exercises.filter(is_completed=True).count() < 15 else 3
    }
    return render(request, 'eduagent/eduplay_exercises.html', context)

@login_required
def exercises(request):
    """Список всех заданий"""
    exercises_list = Exercise.objects.all()
    user_exercises = UserExercise.objects.filter(user=request.user)
    completed_exercises = [ue.exercise.id for ue in user_exercises if ue.is_completed]
    
    context = {
        'exercises': exercises_list,
        'completed_exercises': completed_exercises,
    }
    return render(request, 'eduagent/exercises.html', context)

@login_required
def exercise_detail(request, exercise_id):
    """Страница конкретного задания"""
    exercise = get_object_or_404(Exercise, id=exercise_id)
    user_exercise, created = UserExercise.objects.get_or_create(
        user=request.user,
        exercise=exercise,
        defaults={'user_code': exercise.starter_code}
    )
    
    context = {
        'exercise': exercise,
        'user_exercise': user_exercise,
    }
    return render(request, 'eduagent/exercise_detail.html', context)

@login_required
def submit_exercise(request, exercise_id):
    """Проверка решения задания"""
    if request.method == 'POST':
        exercise = get_object_or_404(Exercise, id=exercise_id)
        user_code = request.POST.get('code', '')
        
        user_exercise, created = UserExercise.objects.get_or_create(
            user=request.user,
            exercise=exercise,
            defaults={'user_code': user_code}
        )
        
        user_exercise.user_code = user_code
        user_exercise.attempts += 1
        
        # Простая проверка кода
        is_correct = check_exercise_solution(exercise, user_code)
        
        if is_correct:
            user_exercise.is_completed = True
            user_exercise.score = exercise.points
            user_exercise.completed_at = timezone.now()
            result = {'success': True, 'message': 'Отлично! Задание выполнено!'}
        else:
            user_exercise.score = 0
            result = {'success': False, 'message': 'Попробуй еще раз!'}
        
        user_exercise.save()
        
        return JsonResponse(result)
    
    return JsonResponse({'success': False, 'message': 'Неверный метод запроса'})

def check_exercise_solution(exercise, user_code):
    """Простая проверка решения"""
    try:
        # Для Python заданий
        if exercise.category == 'python':
            exec_globals = {}
            exec(user_code, exec_globals)
            
            # Проверка тестовых случаев
            for test_case in exercise.test_cases:
                input_data = test_case.get('input', '')
                expected_output = test_case.get('output', '')
                
                if 'solve' in exec_globals:
                    result = exec_globals['solve'](input_data)
                    if str(result) != str(expected_output):
                        return False
                else:
                    return False
        
        return True
        
    except Exception as e:
        print(f"Error checking solution: {e}")
        return False

def analytics(request):
    """Аналитика"""
    return render(request, 'eduagent/analytics.html')

def profile(request):
    """Профиль"""
    return render(request, 'eduagent/profile.html')
