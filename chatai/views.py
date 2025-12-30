# chatai/views.py
import json
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone
from dotenv import load_dotenv
from .models import ChatSession, ChatMessage

# Load environment variables
load_dotenv()

# Get API keys from environment
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
AI_MODEL = os.getenv('AI_MODEL', 'llama-3.1-8b-instant')

@login_required
def chat_page(request):
    """Главная страница ИИ-чата"""
    return render(request, 'chatai/chat.html')

@login_required
def math_chat_page(request):
    """Страница математического ИИ-чата"""
    return render(request, 'chatai/math_chat.html')

@csrf_exempt
@require_POST
def math_chat_api(request):
    """API для математического чата без программирования"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        message = data.get('message', '').strip()
        session_id = data.get('session_id', 'math_session')
        
        print(f"DEBUG: Math chat received: {message}, session: {session_id}")

        if not message:
            return JsonResponse({'success': False, 'error': 'Сообщение пустое'}, status=400)

        # Используем Groq API для математических задач
        try:
            import requests
            
            groq_api_key = GROQ_API_KEY
            ai_model = AI_MODEL or "llama-3.1-8b-instant"
            GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }
            
            # Специальный промпт для математики
            system_prompt = """Ты - математический помощник. Отвечай на математические вопросы без программирования.
            
Правила:
1. Решай математические задачи шаг за шагом
2. Дай только числовой ответ для простых примеров
3. Для сложных задач покажи решение
4. Не используй программный код
5. Отвечай кратко и по делу на русском языке
6. Если задача не математическая, вежливо откажись"""

            payload = {
                "model": ai_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Реши математическую задачу: {message}"}
                ],
                "max_tokens": 300,
                "temperature": 0.1
            }
            
            response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                print(f"DEBUG: Math response: {ai_response[:100]}...")
            else:
                print(f"DEBUG: Math API error: {response.status_code}")
                ai_response = generate_math_response(message)
                
        except Exception as e:
            print(f"DEBUG: Math connection error: {str(e)}")
            ai_response = generate_math_response(message)

        # Save to database
        with transaction.atomic():
            session, created = ChatSession.objects.get_or_create(
                session_id=session_id,
                defaults={'created_at': timezone.now()}
            )
            
            ChatMessage.objects.create(
                session=session,
                user_message=message,
                ai_response=ai_response
            )
        
        return JsonResponse({
            'success': True,
            'response': ai_response
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Неверный формат JSON'
        }, status=400)
    except Exception as e:
        error_msg = f'Math Chat Error: {str(e)}'
        print(f"DEBUG: {error_msg}")
        return JsonResponse({
            'success': False,
            'error': f'Ошибка: {str(e)[:200]}'
        }, status=500)

def generate_math_response(message):
    """Генерирует математические ответы без ИИ"""
    message_lower = message.lower()
    
    # Простые арифметические операции
    if '+' in message and all(c.isdigit() or c in '+-*/.() ' for c in message):
        try:
            result = eval(message)
            return f"Ответ: {result}"
        except:
            pass
    
    # Распознавание типов задач
    if any(word in message_lower for word in ['сложи', 'плюс', '+']):
        numbers = [int(s) for s in message.split() if s.isdigit()]
        if len(numbers) >= 2:
            return f"Ответ: {sum(numbers)}"
    
    if any(word in message_lower for word in ['умножь', 'умножить', '×', '*']):
        numbers = [int(s) for s in message.split() if s.isdigit()]
        if len(numbers) >= 2:
            result = 1
            for num in numbers:
                result *= num
            return f"Ответ: {result}"
    
    if any(word in message_lower for word in ['вычти', 'минус', '-']):
        numbers = [int(s) for s in message.split() if s.isdigit()]
        if len(numbers) >= 2:
            return f"Ответ: {numbers[0] - numbers[1]}"
    
    # Геометрия
    if 'площадь' in message_lower and 'треугольника' in message_lower:
        return "Для площади треугольника нужна формула: S = 0.5 × основание × высота. Укажи размеры."
    
    if 'круг' in message_lower and 'площадь' in message_lower:
        return "Площадь круга: S = π × r². Укажи радиус."
    
    # По умолчанию
    return "Я могу решать арифметические примеры (сложение, вычитание, умножение, деление). Напиши пример числами."

@csrf_exempt
@require_POST
def chat_api(request):
    """API для обработки сообщений ИИ-чата"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default_session')
        
        print(f"DEBUG: Received message: {message}, session: {session_id}")

        if not message:
            return JsonResponse({'success': False, 'error': 'Xabar bo\'sh'}, status=400)

        # Используем бесплатный Groq API (быстрый и надежный)
        try:
            import requests
            
            # Groq API - используем переменные из .env
            groq_api_key = GROQ_API_KEY
            ai_model = AI_MODEL or "llama-3.1-8b-instant"
            GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": ai_model,  # используем модель из .env
                "messages": [
                    {"role": "system", "content": "Отвечай кратко и по делу на русском языке."},
                    {"role": "user", "content": message}
                ],
                "max_tokens": 300,
                "temperature": 0.5
            }
            
            response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                print(f"DEBUG: Groq response: {ai_response[:100]}...")
            else:
                print(f"DEBUG: Groq error: {response.status_code}")
                ai_response = generate_smart_response(message)
                
        except Exception as e:
            print(f"DEBUG: Groq connection error: {str(e)}")
            ai_response = generate_smart_response(message)

        # Save to database
        with transaction.atomic():
            session, created = ChatSession.objects.get_or_create(
                session_id=session_id,
                defaults={'created_at': timezone.now()}
            )
            
            # Save user message and AI response
            ChatMessage.objects.create(
                session=session,
                user_message=message,
                ai_response=ai_response
            )
        
        return JsonResponse({
            'success': True,
            'response': ai_response
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Noto\'g\'ri JSON formati'
        }, status=400)
    except Exception as e:
        error_msg = f'Chat API Error: {str(e)}'
        print(f"DEBUG: {error_msg}")
        return JsonResponse({
            'success': False,
            'error': f'Ошибка: {str(e)[:200]}'
        }, status=500)

def generate_smart_response(message):
    """Генерирует умные ответы на основе контекста"""
    message_lower = message.lower()
    
    # Обучение/образование
    if any(word in message_lower for word in ['учить', 'изучать', 'learn', 'study']):
        return f'Отлично, что хочешь изучить! Для "{message}" рекомендую начать с основ и практиковаться каждый день.'
    
    # Программирование
    if any(word in message_lower for word in ['код', 'python', 'javascript', 'программа']):
        return f'Программирование - это круто! Для "{message}" советую начать с простых проектов и постепенно усложнять.'
    
    # Приветствия
    if any(word in message_lower for word in ['привет', 'ку', 'hello', 'hi']):
        greetings = ['Привет! Чем могу помочь?', 'Ку! Что интересует?', 'Здравствуй! Рад тебя видеть!']
        import random
        return random.choice(greetings)
    
    # Вопросы
    if '?' in message:
        if 'как' in message_lower:
            return f'Отличный вопрос! Для "{message}" нужно разбить задачу на шаги: 1) Анализ 2) Планирование 3) Действие'
        elif 'что' in message_lower:
            return f'Хороший вопрос! "{message}" - это важная тема. Давай разберемся вместе.'
        elif 'почему' in message_lower:
            return f'Интересный вопрос! Причина "{message}" кроется в нескольких факторах. Давай изучим их.'
    
    # Математика
    if any(char.isdigit() for char in message):
        return f'Математические задачи требуют точности. Для "{message}" проверь формулы и careful calculations.'
    
    # По умолчанию
    responses = [
        f'Интересная мысль: "{message}". Расскажи подробнее!',
        f'Понял тебя: "{message}". Это достойно обсуждения.',
        f'Спасибо, что поделился: "{message}". Мое мнение...',
        f'Заметил: "{message}". Это действительно важно.'
    ]
    import random
    return random.choice(responses)

def get_history(request, session_id):
    """Получить историю чата"""
    try:
        session = ChatSession.objects.get(session_id=session_id)
        messages = ChatMessage.objects.filter(
            session=session
        ).order_by('created_at')
        
        history = []
        for msg in messages:
            # Add both user and AI messages
            if msg.user_message:
                history.append({
                    'message': msg.user_message,
                    'is_user': True,
                    'timestamp': msg.created_at.isoformat()
                })
            if msg.ai_response:
                history.append({
                    'message': msg.ai_response,
                    'is_user': False,
                    'timestamp': msg.created_at.isoformat()
                })
        
        return JsonResponse({'success': True, 'history': history})
    except ChatSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def clear_history(request, session_id):
    """Очистить историю чата"""
    try:
        session = ChatSession.objects.get(session_id=session_id)
        count = ChatMessage.objects.filter(session=session).count()
        ChatMessage.objects.filter(session=session).delete()
        session.delete()

        return JsonResponse({
            'success': True,
            'message': f'{count} сообщений удалено',
            'session_id': session_id
        })
    except ChatSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def chat_widget(request):
    """Chat widget для отдельной страницы"""
    return JsonResponse({
        'widget': True,
        'endpoints': {
            'chat': '/ai/api/',
            'history': '/ai/history/{session_id}/',
            'clear': '/ai/clear/{session_id}/'
        }
    })