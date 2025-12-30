# Telegram Auth с кодом - Инструкция по использованию

## Обзор
Система аутентификации через Telegram с использованием 4-значного кода подтверждения.

## Как это работает

### 1. Пользователь нажимает "Войти через Telegram"
- Frontend отправляет запрос на `/auth/telegram/start/`
- Backend создает session token (10 минут действия)
- Возвращает session token и имя бота

### 2. Пользователь переходит в Telegram
- Открывается бот: `https://t.me/eduagent_bot?start=login_{session_token}`
- Бот запрашивает номер телефона
- Пользователь отправляет контакт

### 3. Бот генерирует код
- Создает 4-значный код
- Отправляет код пользователю
- Код действует 2 минуты

### 4. Пользователь вводит код на сайте
- Frontend отправляет код на `/auth/telegram/verify/`
- Backend проверяет код и session token
- При успехе - пользователь авторизуется

## Файлы системы

### Backend
- `authentication/models.py` - модель TelegramAuth
- `authentication/views.py` - views для auth
- `authentication/urls.py` - URL маршруты
- `config/settings.py` - настройки Telegram
- `bot.py` - Telegram бот

### Frontend
- `templates/login.html` - страница входа с модальным окном

## API Endpoints

### POST `/auth/telegram/start/`
Создание сессии
```json
{
  "success": true,
  "session_token": "abc123def",
  "bot_username": "eduagent_bot",
  "expires_in": 600
}
```

### POST `/auth/telegram/verify/`
Проверка кода
```json
{
  "session_token": "abc123def",
  "code": "1234"
}
```

Ответ:
```json
{
  "success": true,
  "message": "Мувваффакиятли киритилди!",
  "redirect_url": "/",
  "user": {
    "id": 1,
    "phone_number": "+998901234567",
    "first_name": "Telegram",
    "last_name": "User",
    "role": "student"
  }
}
```

## Настройки в .env
```env
TELEGRAM_BOT_ID=8266841349
TELEGRAM_BOT_TOKEN=8266841349:AAHAKCzXriwBdmMCjmxHkIfLB1wRMeT2ZfM
TELEGRAM_BOT_USERNAME=eduagent_bot
SITE_URL=http://127.0.0.1:8000
```

## Запуск бота
```bash
python bot.py
```

## Безопасность
- Session token - 10 минут
- Код подтверждения - 2 минуты  
- Ограничение на повторную отправку кода - 3 раза за 5 минут
- Код используется только один раз

## Возможные проблемы

### 1. Бот не отвечает
- Проверьте токен в .env
- Убедитесь что бот запущен

### 2. Код не принимается
- Проверьте что session token не истек
- Убедитесь что код правильный и не использован

### 3. Пользователь не создается
- Проверьте модель CustomUser
- Убедитесь что телефонный номер правильный

## Тестирование
1. Запустите Django сервер: `python manage.py runserver`
2. Запустите бота: `python bot.py`
3. Откройте `http://127.0.0.1:8000/login/`
4. Нажмите "Telegram с кодом"
5. Следуйте инструкциям
