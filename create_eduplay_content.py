import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from eduagent.models import Avatar, MiniGame, Achievement, UserCoins

User = get_user_model()

# Создаем аватары (используем существующие картинки)
avatars_data = [
    {
        'name': 'Стандартный',
        'image': 'media/images/logo_falak.png',
        'price': 0,
        'is_premium': False
    },
    {
        'name': 'Спортсмен',
        'image': 'media/images/avatar_soccer.jpg',
        'price': 50,
        'is_premium': False
    },
    {
        'name': 'Землянин',
        'image': 'media/images/avater_earth.jpg',
        'price': 75,
        'is_premium': False
    },
    {
        'name': 'Бизнесмен',
        'image': 'media/images/avatar_b.jpg',
        'price': 100,
        'is_premium': False
    },
    {
        'name': 'Смайлик',
        'image': 'media/images/pic.jpeg',
        'price': 25,
        'is_premium': False
    }
]

print("Создание аватаров...")
for avatar_data in avatars_data:
    avatar, created = Avatar.objects.get_or_create(
        name=avatar_data['name'],
        defaults={
            'image': avatar_data['image'],
            'price': avatar_data['price'],
            'is_premium': avatar_data['is_premium']
        }
    )
    if created:
        print(f"✅ Создан аватар: {avatar.name} - {avatar.price} монет")
    else:
        print(f"📋 Аватар уже существует: {avatar.name}")

# Создаем мини-игры из EduPlay
minigames_data = [
    {
        'name': 'Математический квиз',
        'game_type': 'math_quiz',
        'description': 'Реши математические примеры и получи монеты!',
        'reward_coins': 12,
        'difficulty': 'easy',
        'building_type': 'school'
    },
    {
        'name': 'Сбор слов',
        'game_type': 'word_collect',
        'description': 'Собери английские слова из букв',
        'reward_coins': 10,
        'difficulty': 'medium',
        'building_type': 'library'
    },
    {
        'name': 'Лови числа',
        'game_type': 'catch_numbers',
        'description': 'Лови правильные ответы и избегай неправильные',
        'reward_coins': 15,
        'difficulty': 'medium',
        'building_type': 'gym'
    },
    {
        'name': 'Память',
        'game_type': 'memory_cards',
        'description': 'Найди парные карточки',
        'reward_coins': 8,
        'difficulty': 'easy',
        'building_type': 'art'
    },
    {
        'name': 'Пазлы',
        'game_type': 'puzzle',
        'description': 'Собери пазл из кусочков',
        'reward_coins': 20,
        'difficulty': 'hard',
        'building_type': 'lab'
    }
]

print("\nСоздание мини-игр...")
for game_data in minigames_data:
    game, created = MiniGame.objects.get_or_create(
        name=game_data['name'],
        defaults=game_data
    )
    if created:
        print(f"🎮 Создана игра: {game.name} - {game.reward_coins} монет")
    else:
        print(f"📋 Игра уже существует: {game.name}")

# Создаем достижения
achievements_data = [
    {
        'name': 'Первая победа',
        'description': 'Выполни первое задание',
        'icon': '🏆',
        'reward_coins': 10,
        'condition': {'type': 'first_exercise', 'completed': True}
    },
    {
        'name': 'Математический гений',
        'description': 'Выполни 10 математических заданий',
        'icon': '🧮',
        'reward_coins': 50,
        'condition': {'type': 'exercises_count', 'category': 'math', 'count': 10}
    },
    {
        'name': 'Коллекционер',
        'description': 'Собери 5 разных аватаров',
        'icon': '🖼️',
        'reward_coins': 30,
        'condition': {'type': 'avatars_count', 'count': 5}
    },
    {
        'name': 'Игроман',
        'description': 'Сыграй во все мини-игры',
        'icon': '🎮',
        'reward_coins': 40,
        'condition': {'type': 'games_played', 'count': 5}
    },
    {
        'name': 'Миллионер',
        'description': 'Накопи 100 монет',
        'icon': '💰',
        'reward_coins': 100,
        'condition': {'type': 'coins_earned', 'amount': 100}
    },
    {
        'name': 'Студент',
        'description': 'Выполни задание в каждом здании',
        'icon': '🎓',
        'reward_coins': 25,
        'condition': {'type': 'buildings_completed', 'count': 5}
    }
]

print("\nСоздание достижений...")
for achievement_data in achievements_data:
    achievement, created = Achievement.objects.get_or_create(
        name=achievement_data['name'],
        defaults=achievement_data
    )
    if created:
        print(f"🏅 Создано достижение: {achievement.name} - {achievement.reward_coins} монет")
    else:
        print(f"📋 Достижение уже существует: {achievement.name}")

# Создаем монеты для всех пользователей
print("\nСоздание монет для пользователей...")
for user in User.objects.all():
    user_coins, created = UserCoins.objects.get_or_create(
        user=user,
        defaults={'coins': 50}  # Начальные монеты
    )
    if created:
        print(f"💰 Созданы монеты для пользователя: {user.email} - 50 монет")
    else:
        print(f"📋 Монеты уже существуют для: {user.email} - {user_coins.coins} монет")

print("\n🎉 Контент EduPlay успешно создан!")
print("\n📊 Статистика:")
print(f"👥 Аватаров: {Avatar.objects.count()}")
print(f"🎮 Мини-игр: {MiniGame.objects.count()}")
print(f"🏅 Достижений: {Achievement.objects.count()}")
print(f"💰 Пользователей с монетами: {UserCoins.objects.count()}")

print("\n🎯 Доступные функции:")
print("• Покупка аватаров за монеты")
print("• Мини-игры с наградами")
print("• Система достижений")
print("• Монеты за выполнение заданий")
print("• Прогресс в зданиях")
