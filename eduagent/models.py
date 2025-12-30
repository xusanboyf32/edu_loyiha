from django.db import models
from django.conf import settings

class Exercise(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный')
    ])
    category = models.CharField(max_length=50, choices=[
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('html', 'HTML/CSS'),
        ('django', 'Django'),
        ('algorithm', 'Алгоритмы'),
        ('math', 'Математика')
    ])
    starter_code = models.TextField(blank=True, help_text="Начальный код для задания")
    solution = models.TextField(help_text="Правильное решение")
    test_cases = models.JSONField(default=list, help_text="Тестовые случаи")
    points = models.IntegerField(default=10)
    image = models.ImageField(upload_to='exercises/', blank=True, null=True, help_text="Изображение для задания")
    building_type = models.CharField(max_length=50, choices=[
        ('school', 'Школа'),
        ('library', 'Библиотека'),
        ('lab', 'Лаборатория'),
        ('gym', 'Спортзал'),
        ('art', 'Арт-студия')
    ], default='school', help_text="Тип здания в стиле EduPlay")
    level = models.IntegerField(default=1, help_text="Уровень задания (1-5)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'eduagent'

    def __str__(self):
        return self.title

class UserExercise(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    user_code = models.TextField()
    is_completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'eduagent'

    def __str__(self):
        return f"{self.user.username} - {self.exercise.title}"

# Монеты и экономика
class UserCoins(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    total_earned = models.IntegerField(default=0)
    total_spent = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'eduagent'

    def __str__(self):
        return f"{self.user.username} - {self.coins} монет"

# Аватары
class Avatar(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='avatars/')
    price = models.IntegerField(default=0)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'eduagent'

    def __str__(self):
        return f"{self.name} - {self.price} монет"

# Покупки аватаров
class UserAvatar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'eduagent'

    def __str__(self):
        return f"{self.user.username} - {self.avatar.name}"

# Мини-игры
class MiniGame(models.Model):
    GAME_TYPES = [
        ('math_quiz', 'Математический квиз'),
        ('word_collect', 'Сбор слов'),
        ('catch_numbers', 'Лови числа'),
        ('memory_cards', 'Память'),
        ('puzzle', 'Пазлы')
    ]
    
    name = models.CharField(max_length=100)
    game_type = models.CharField(max_length=20, choices=GAME_TYPES)
    description = models.TextField()
    reward_coins = models.IntegerField(default=5)
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный')
    ])
    building_type = models.CharField(max_length=50, choices=[
        ('school', 'Школа'),
        ('library', 'Библиотека'),
        ('lab', 'Лаборатория'),
        ('gym', 'Спортзал'),
        ('art', 'Арт-студия')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'eduagent'

    def __str__(self):
        return f"{self.name} ({self.get_game_type_display})"

# Результаты игр
class GameResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(MiniGame, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    coins_earned = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    time_spent = models.IntegerField(default=0)  # в секундах
    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'eduagent'

    def __str__(self):
        return f"{self.user.username} - {self.game.name} - {self.score} очков"

# Достижения
class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🏆')
    reward_coins = models.IntegerField(default=10)
    condition = models.JSONField(help_text="Условие для получения достижения")

    class Meta:
        app_label = 'eduagent'

    def __str__(self):
        return self.name

# Полученные достижения
class UserAchievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'eduagent'

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"
