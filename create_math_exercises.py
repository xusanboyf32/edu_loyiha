import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from eduagent.models import Exercise

# Математические задания
math_exercises = [
    {
        'title': 'Сложение чисел',
        'description': 'Реши пример: 15 + 27 = ?',
        'difficulty': 'easy',
        'category': 'math',
        'starter_code': '# Напиши ответ числом\nresult = ',
        'solution': '42',
        'test_cases': [
            {'input': '', 'output': '42'}
        ],
        'points': 10
    },
    {
        'title': 'Умножение',
        'description': 'Реши пример: 8 × 7 = ?',
        'difficulty': 'easy',
        'category': 'math',
        'starter_code': '# Напиши ответ числом\nresult = ',
        'solution': '56',
        'test_cases': [
            {'input': '', 'output': '56'}
        ],
        'points': 10
    },
    {
        'title': 'Квадратное уравнение',
        'description': 'Реши уравнение: x² - 5x + 6 = 0. Найди корни (через запятую)',
        'difficulty': 'medium',
        'category': 'math',
        'starter_code': '# Напиши корни через запятую\nroots = ',
        'solution': '2, 3',
        'test_cases': [
            {'input': '', 'output': '2, 3'}
        ],
        'points': 20
    },
    {
        'title': 'Площадь треугольника',
        'description': 'Найди площадь треугольника с основанием 10 и высотой 6. Формула: S = 0.5 × основание × высота',
        'difficulty': 'medium',
        'category': 'math',
        'starter_code': '# Напиши площадь числом\narea = ',
        'solution': '30',
        'test_cases': [
            {'input': '', 'output': '30'}
        ],
        'points': 15
    },
    {
        'title': 'Проценты',
        'description': 'Найди 25% от числа 200',
        'difficulty': 'easy',
        'category': 'math',
        'starter_code': '# Напиши ответ числом\nresult = ',
        'solution': '50',
        'test_cases': [
            {'input': '', 'output': '50'}
        ],
        'points': 10
    },
    {
        'title': 'Степень числа',
        'description': 'Вычисли: 3⁴ = ?',
        'difficulty': 'easy',
        'category': 'math',
        'starter_code': '# Напиши ответ числом\nresult = ',
        'solution': '81',
        'test_cases': [
            {'input': '', 'output': '81'}
        ],
        'points': 10
    },
    {
        'title': 'Теорема Пифагора',
        'description': 'В прямоугольном треугольнике катеты равны 3 и 4. Найди гипотенузу (c² = a² + b²)',
        'difficulty': 'medium',
        'category': 'math',
        'starter_code': '# Напиши длину гипотенузы\nc = ',
        'solution': '5',
        'test_cases': [
            {'input': '', 'output': '5'}
        ],
        'points': 20
    },
    {
        'title': 'Системы уравнений',
        'description': 'Реши систему: x + y = 10, x - y = 2. Найди x и y (через запятую)',
        'difficulty': 'hard',
        'category': 'math',
        'starter_code': '# Напиши x и y через запятую\nsolution = ',
        'solution': '6, 4',
        'test_cases': [
            {'input': '', 'output': '6, 4'}
        ],
        'points': 30
    }
]

for exercise_data in math_exercises:
    exercise, created = Exercise.objects.get_or_create(
        title=exercise_data['title'],
        defaults=exercise_data
    )
    if created:
        print(f"Создано задание: {exercise.title}")
    else:
        print(f"Задание уже существует: {exercise.title}")

print("Математические задания успешно созданы!")
