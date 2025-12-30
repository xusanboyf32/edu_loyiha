# REST API документация - Случайные примеры EduPlay

## Обзор
REST API для управления случайными примерами в образовательной платформе EduPlay. Примеры генерируются с помощью файла рандомайзера и сохраняются в JSON файл.

## Базовый URL
```
http://127.0.0.1:8000/api/
```

## Эндпоинты

### 1. Получить случайные примеры
**GET** `/api/random-examples/`

Возвращает случайные примеры из файла `random_examples.json`.

**Ответ:**
```json
{
    "success": true,
    "examples": [
        {
            "id": "math_0",
            "question": "15 + 23 = ?",
            "answer": "38",
            "difficulty": "medium",
            "category": "math",
            "coins": 10,
            "hint": "Используй операцию +"
        }
    ],
    "total_count": 20,
    "source": "file",
    "categories": ["math", "english", "geometry", "logic"]
}
```

### 2. Перегенерировать примеры
**POST** `/api/random-examples/`

Генерирует новые случайные примеры с помощью `RandomExamplesGenerator`.

**Тело запроса:**
```json
{}
```

**Ответ:**
```json
{
    "success": true,
    "examples": [...],
    "total_count": 20,
    "source": "regenerated",
    "message": "Примеры успешно перегенерированы",
    "categories": ["math", "english", "geometry", "logic"]
}
```

### 3. Получить статистику примеров
**GET** `/api/examples-stats/`

Возвращает подробную статистику по примерам в файле.

**Ответ:**
```json
{
    "success": true,
    "stats": {
        "total_count": 20,
        "categories": {
            "math": 8,
            "english": 6,
            "geometry": 4,
            "logic": 2
        },
        "difficulties": {
            "easy": 10,
            "medium": 7,
            "hard": 3
        },
        "coins_range": {
            "min": 5,
            "max": 20
        }
    },
    "generated_at": "1640995200",
    "file_size": 2048
}
```

### 4. Добавить кастомный пример
**POST** `/api/add-example/`

Добавляет новый пример в файл.

**Тело запроса:**
```json
{
    "question": "Сколько будет 2 + 2?",
    "answer": "4",
    "category": "math",
    "difficulty": "easy",
    "coins": 5,
    "hint": "Простое сложение"
}
```

**Ответ:**
```json
{
    "success": true,
    "message": "Пример успешно добавлен",
    "example": {
        "id": "custom_20",
        "question": "Сколько будет 2 + 2?",
        "answer": "4",
        "category": "math",
        "difficulty": "easy",
        "coins": 5,
        "hint": "Простое сложение",
        "custom": true
    },
    "total_count": 21
}
```

## Категории примеров

### Math (Математика)
- Арифметические операции: сложение, вычитание, умножение, деление
- Сложность: easy (результат < 50), medium (50-100), hard (> 100)
- Монеты: 5-20 в зависимости от сложности

### English (Английский язык)
- Перевод слов с русского на английский
- Подсказки для контекста
- Сложность: easy
- Монеты: 8-15

### Geometry (Геометрия)
- Площадь и периметр фигур
- Прямоугольники, квадраты, круги
- Сложность: easy, medium, hard
- Монеты: 6-20

### Logic (Логика)
- Числовые последовательности
- Простые логические задачи
- Сложность: easy, medium, hard
- Монеты: 5-15

## Использование в JavaScript

### Загрузка примеров
```javascript
async function loadExamples() {
    const response = await fetch('/api/random-examples/');
    const data = await response.json();
    
    if (data.success) {
        examples = data.examples;
        displayExamples();
    }
}
```

### Перегенерация примеров
```javascript
async function regenerateExamples() {
    const response = await fetch('/api/random-examples/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    });
    const data = await response.json();
    
    if (data.success) {
        examples = data.examples;
        displayExamples();
    }
}
```

### Получение статистики
```javascript
async function getStats() {
    const response = await fetch('/api/examples-stats/');
    const data = await response.json();
    
    if (data.success) {
        console.log('Статистика:', data.stats);
    }
}
```

## Файловая структура

```
falak_reboot/
├── random_examples_generator.py  # Генератор примеров
├── random_examples.json          # Файл с примерами
├── eduagent/
│   ├── api_views.py             # REST API views
│   └── urls.py                  # URL маршруты
└── templates/
    └── eduagent/
        └── eduplay_exercises.html  # Фронтенд
```

## Генератор примеров

### RandomExamplesGenerator
Класс для генерации различных типов примеров:

- `generate_math_examples(count)` - математические примеры
- `generate_english_examples(count)` - английские слова
- `generate_geometry_examples(count)` - геометрические задачи
- `generate_logic_examples(count)` - логические задачи
- `generate_all_examples(total_count)` - все типы примеров
- `save_to_file(filename)` - сохранение в JSON файл

### Пример использования генератора
```python
from random_examples_generator import RandomExamplesGenerator

generator = RandomExamplesGenerator()
examples = generator.generate_all_examples(20)
generator.save_to_file('random_examples.json')
```

## Ошибки

### Коды ошибок
- `200` - Успешно
- `400` - Ошибка валидации данных
- `404` - Файл не найден
- `500` - Внутренняя ошибка сервера

### Формат ошибок
```json
{
    "success": false,
    "error": "Ошибка",
    "message": "Описание ошибки"
}
```

## Безопасность

- Все эндпоинты требуют аутентификации (`@login_required`)
- CSRF защита для POST запросов
- Валидация входных данных
- Обработка исключений

## Кэширование

- Примеры кэшируются в файле `random_examples.json`
- При отсутствии файла автоматически создается новый
- Поддержка перегенерации примеров по запросу

## Интеграция с фронтендом

JavaScript в шаблоне `eduplay_exercises.html` автоматически:
- Загружает примеры при загрузке страницы
- Поддерживает перегенерацию примеров
- Отображает примеры в pop-up окнах
- Проверяет ответы и начисляет монеты
- Показывает уведомления о результатах
