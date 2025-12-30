import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from eduagent.models import Exercise

# EduPlay задания с картинками и зданиями
eduplay_exercises = [
    # Школа - уровень 1
    {
        'title': 'Сложение в школе',
        'description': 'Реши пример: 12 + 8 = ?',
        'difficulty': 'easy',
        'category': 'math',
        'building_type': 'school',
        'level': 1,
        'starter_code': '',
        'solution': '20',
        'test_cases': [{'input': '', 'output': '20'}],
        'points': 10,
        'image': 'media/images/logo_falak.png'
    },
    # Школа - уровень 2
    {
        'title': 'Python приветствие',
        'description': 'Напиши функцию, которая возвращает "Привет, мир!"',
        'difficulty': 'easy',
        'category': 'python',
        'building_type': 'school',
        'level': 2,
        'starter_code': 'def hello():\n    # Напиши код здесь\n    pass',
        'solution': 'def hello():\n    return "Привет, мир!"',
        'test_cases': [{'input': '', 'output': 'Привет, мир!'}],
        'points': 15,
        'image': 'media/images/logo_falak.png'
    },
    # Библиотека - уровень 1
    {
        'title': 'Чтение текста',
        'description': 'Посчитай количество слов в предложении: "Быстрый коричневый лис прыгает через ленивую собаку"',
        'difficulty': 'easy',
        'category': 'algorithm',
        'building_type': 'library',
        'level': 1,
        'starter_code': '# Напиши ответ числом\nword_count = ',
        'solution': '8',
        'test_cases': [{'input': '', 'output': '8'}],
        'points': 10,
        'image': 'media/images/logo_falak.png'
    },
    # Библиотека - уровень 2
    {
        'title': 'Обратная строка',
        'description': 'Напиши функцию, которая переворачивает строку задом наперед',
        'difficulty': 'medium',
        'category': 'python',
        'building_type': 'library',
        'level': 2,
        'starter_code': 'def reverse_string(s):\n    # Напиши код здесь\n    pass',
        'solution': 'def reverse_string(s):\n    return s[::-1]',
        'test_cases': [{'input': 'hello', 'output': 'olleh'}],
        'points': 20,
        'image': 'media/images/logo_falak.png'
    },
    # Лаборатория - уровень 1
    {
        'title': 'Химическая формула',
        'description': 'Сколько атомов водорода в H₂O?',
        'difficulty': 'easy',
        'category': 'math',
        'building_type': 'lab',
        'level': 1,
        'starter_code': '# Напиши ответ числом\nhydrogen_atoms = ',
        'solution': '2',
        'test_cases': [{'input': '', 'output': '2'}],
        'points': 10,
        'image': 'media/images/logo_falak.png'
    },
    # Лаборатория - уровень 2
    {
        'title': 'Физика: скорость',
        'description': 'Машина проехала 100 км за 2 часа. Какая средняя скорость?',
        'difficulty': 'medium',
        'category': 'math',
        'building_type': 'lab',
        'level': 2,
        'starter_code': '# Напиши ответ числом (км/ч)\nspeed = ',
        'solution': '50',
        'test_cases': [{'input': '', 'output': '50'}],
        'points': 15,
        'image': 'media/images/logo_falak.png'
    },
    # Спортзал - уровень 1
    {
        'title': 'Баскетбольный счет',
        'description': 'Команда забила 3 трехочковых и 4 двухочковых броска. Сколько очков всего?',
        'difficulty': 'easy',
        'category': 'math',
        'building_type': 'gym',
        'level': 1,
        'starter_code': '# Напиши ответ числом\ntotal_points = ',
        'solution': '17',
        'test_cases': [{'input': '', 'output': '17'}],
        'points': 10,
        'image': 'media/images/logo_falak.png'
    },
    # Спортзал - уровень 2
    {
        'title': 'Футбольный турнир',
        'description': 'В турнире 6 команд. Каждая играет с каждой по 2 раза. Сколько всего матчей?',
        'difficulty': 'medium',
        'category': 'math',
        'building_type': 'gym',
        'level': 2,
        'starter_code': '# Напиши ответ числом\ntotal_matches = ',
        'solution': '30',
        'test_cases': [{'input': '', 'output': '30'}],
        'points': 20,
        'image': 'media/images/logo_falak.png'
    },
    # Арт-студия - уровень 1
    {
        'title': 'Цвета радуги',
        'description': 'Сколько цветов в радуге?',
        'difficulty': 'easy',
        'category': 'math',
        'building_type': 'art',
        'level': 1,
        'starter_code': '# Напиши ответ числом\nrainbow_colors = ',
        'solution': '7',
        'test_cases': [{'input': '', 'output': '7'}],
        'points': 10,
        'image': 'media/images/logo_falak.png'
    },
    # Арт-студия - уровень 2
    {
        'title': 'Геометрический узор',
        'description': 'Сколько сторон у правильного шестиугольника?',
        'difficulty': 'easy',
        'category': 'math',
        'building_type': 'art',
        'level': 2,
        'starter_code': '# Напиши ответ числом\nsides = ',
        'solution': '6',
        'test_cases': [{'input': '', 'output': '6'}],
        'points': 10,
        'image': 'media/images/logo_falak.png'
    }
]

for exercise_data in eduplay_exercises:
    exercise, created = Exercise.objects.get_or_create(
        title=exercise_data['title'],
        defaults=exercise_data
    )
    if created:
        print(f"Создано EduPlay задание: {exercise.title} ({exercise.building_type} - уровень {exercise.level})")
    else:
        print(f"Задание уже существует: {exercise.title}")

print("EduPlay задания успешно созданы!")
print("\nДоступные здания:")
print("🏫 Школа - основные предметы")
print("📚 Библиотека - чтение и теория") 
print("🔬 Лаборатория - наука и эксперименты")
print("⚽ Спортзал - физическая активность")
print("🎨 Арт-студия - творчество")
