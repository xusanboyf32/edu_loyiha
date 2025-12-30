from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
import os
from django.conf import settings
from random_examples_generator import RandomExamplesGenerator

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required
def random_examples_api(request):
    """REST API для случайных примеров"""
    
    if request.method == 'GET':
        # Получить примеры из файла
        return get_examples_from_file()
    
    elif request.method == 'POST':
        # Перегенерировать примеры
        return regenerate_examples()

def get_examples_from_file():
    """Загружает примеры из файла"""
    try:
        examples_file = os.path.join(settings.BASE_DIR, 'random_examples.json')
        
        if not os.path.exists(examples_file):
            # Если файла нет, создаем его
            generator = RandomExamplesGenerator()
            examples = generator.save_to_file(examples_file)
        else:
            # Загружаем из файла
            with open(examples_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                examples = data.get('examples', [])
        
        # Перемешиваем для разнообразия
        import random
        random.shuffle(examples)
        
        return JsonResponse({
            'success': True,
            'examples': examples[:20],
            'total_count': len(examples),
            'source': 'file',
            'categories': list(set(ex['category'] for ex in examples))
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Не удалось загрузить примеры из файла'
        }, status=500)

def regenerate_examples():
    """Перегенерирует примеры"""
    try:
        examples_file = os.path.join(settings.BASE_DIR, 'random_examples.json')
        
        # Генерируем новые примеры
        generator = RandomExamplesGenerator()
        examples = generator.save_to_file(examples_file)
        
        # Перемешиваем
        import random
        random.shuffle(examples)
        
        return JsonResponse({
            'success': True,
            'examples': examples[:20],
            'total_count': len(examples),
            'source': 'regenerated',
            'message': 'Примеры успешно перегенерированы',
            'categories': list(set(ex['category'] for ex in examples))
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Не удалось перегенерировать примеры'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
@login_required
def examples_stats(request):
    """Статистика по примерам"""
    try:
        examples_file = os.path.join(settings.BASE_DIR, 'random_examples.json')
        
        if not os.path.exists(examples_file):
            return JsonResponse({
                'success': False,
                'message': 'Файл с примерами не найден'
            }, status=404)
        
        with open(examples_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            examples = data.get('examples', [])
        
        # Собираем статистику
        stats = {
            'total_count': len(examples),
            'categories': {},
            'difficulties': {},
            'coins_range': {'min': float('inf'), 'max': 0}
        }
        
        for example in examples:
            # По категориям
            category = example['category']
            if category not in stats['categories']:
                stats['categories'][category] = 0
            stats['categories'][category] += 1
            
            # По сложности
            difficulty = example['difficulty']
            if difficulty not in stats['difficulties']:
                stats['difficulties'][difficulty] = 0
            stats['difficulties'][difficulty] += 1
            
            # По монетам
            coins = example['coins']
            stats['coins_range']['min'] = min(stats['coins_range']['min'], coins)
            stats['coins_range']['max'] = max(stats['coins_range']['max'], coins)
        
        if stats['coins_range']['min'] == float('inf'):
            stats['coins_range']['min'] = 0
        
        return JsonResponse({
            'success': True,
            'stats': stats,
            'generated_at': data.get('generated_at'),
            'file_size': os.path.getsize(examples_file)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Не удалось получить статистику'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def add_custom_example(request):
    """Добавить кастомный пример"""
    try:
        data = json.loads(request.body)
        
        # Валидация данных
        required_fields = ['question', 'answer', 'category', 'difficulty', 'coins']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }, status=400)
        
        examples_file = os.path.join(settings.BASE_DIR, 'random_examples.json')
        
        # Загружаем существующие примеры
        if os.path.exists(examples_file):
            with open(examples_file, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
                examples = file_data.get('examples', [])
        else:
            examples = []
        
        # Создаем новый пример
        new_example = {
            'id': f"custom_{len(examples)}",
            'question': data['question'],
            'answer': data['answer'],
            'category': data['category'],
            'difficulty': data['difficulty'],
            'coins': data['coins'],
            'hint': data.get('hint', ''),
            'custom': True
        }
        
        # Добавляем пример
        examples.append(new_example)
        
        # Сохраняем файл
        file_data = {
            'success': True,
            'count': len(examples),
            'examples': examples,
            'categories': list(set(ex['category'] for ex in examples)),
            'generated_at': str(int(time.time()))
        }
        
        with open(examples_file, 'w', encoding='utf-8') as f:
            json.dump(file_data, f, ensure_ascii=False, indent=2)
        
        return JsonResponse({
            'success': True,
            'message': 'Пример успешно добавлен',
            'example': new_example,
            'total_count': len(examples)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Не удалось добавить пример'
        }, status=500)

import time
