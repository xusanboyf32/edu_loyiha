import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from eduagent.models import Exercise

# Создаем тестовые задания
exercises_data = [
    {
        'title': 'Hello World на Python',
        'description': 'Напиши функцию solve(), которая возвращает строку "Hello, World!"',
        'difficulty': 'easy',
        'category': 'python',
        'starter_code': 'def solve():\n    # Напиши свой код здесь\n    pass',
        'solution': 'def solve():\n    return "Hello, World!"',
        'test_cases': [
            {'input': '', 'output': 'Hello, World!'}
        ],
        'points': 10
    },
    {
        'title': 'Сумма двух чисел',
        'description': 'Напиши функцию solve(a, b), которая возвращает сумму двух чисел',
        'difficulty': 'easy',
        'category': 'python',
        'starter_code': 'def solve(a, b):\n    # Напиши свой код здесь\n    pass',
        'solution': 'def solve(a, b):\n    return a + b',
        'test_cases': [
            {'input': '2, 3', 'output': '5'},
            {'input': '10, 5', 'output': '15'}
        ],
        'points': 15
    },
    {
        'title': 'Факториал числа',
        'description': 'Напиши функцию solve(n), которая возвращает факториал числа n',
        'difficulty': 'medium',
        'category': 'algorithm',
        'starter_code': 'def solve(n):\n    # Напиши свой код здесь\n    pass',
        'solution': 'def solve(n):\n    if n <= 1:\n        return 1\n    return n * solve(n-1)',
        'test_cases': [
            {'input': '5', 'output': '120'},
            {'input': '3', 'output': '6'}
        ],
        'points': 25
    },
    {
        'title': 'Проверка палиндрома',
        'description': 'Напиши функцию solve(s), которая проверяет является ли строка палиндромом',
        'difficulty': 'medium',
        'category': 'algorithm',
        'starter_code': 'def solve(s):\n    # Напиши свой код здесь\n    pass',
        'solution': 'def solve(s):\n    return s == s[::-1]',
        'test_cases': [
            {'input': 'racecar', 'output': 'True'},
            {'input': 'hello', 'output': 'False'}
        ],
        'points': 20
    },
    {
        'title': 'HTML заголовок',
        'description': 'Создай HTML код для заголовка первого уровня',
        'difficulty': 'easy',
        'category': 'html',
        'starter_code': '<!-- Напиши HTML код здесь -->',
        'solution': '<h1>Мой заголовок</h1>',
        'test_cases': [
            {'input': '', 'output': '<h1>Мой заголовок</h1>'}
        ],
        'points': 10
    }
]

for exercise_data in exercises_data:
    exercise, created = Exercise.objects.get_or_create(
        title=exercise_data['title'],
        defaults=exercise_data
    )
    if created:
        print(f"Создано задание: {exercise.title}")
    else:
        print(f"Задание уже существует: {exercise.title}")

print("Задания успешно созданы!")
