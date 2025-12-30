import random
import json

class RandomExamplesGenerator:
    """Генератор случайных примеров для EduPlay"""
    
    def __init__(self):
        self.math_operations = ['+', '-', '*', '/']
        self.english_words = [
            {'word': 'cat', 'translation': 'кошка', 'hint': 'Домашнее животное'},
            {'word': 'dog', 'translation': 'собака', 'hint': 'Домашнее животное'},
            {'word': 'house', 'translation': 'дом', 'hint': 'Здание'},
            {'word': 'book', 'translation': 'книга', 'hint': 'Чтение'},
            {'word': 'sun', 'translation': 'солнце', 'hint': 'Небесное тело'},
            {'word': 'water', 'translation': 'вода', 'hint': 'Жидкость'},
            {'word': 'tree', 'translation': 'дерево', 'hint': 'Растение'},
            {'word': 'car', 'translation': 'машина', 'hint': 'Транспорт'},
            {'word': 'apple', 'translation': 'яблоко', 'hint': 'Фрукт'},
            {'word': 'computer', 'translation': 'компьютер', 'hint': 'Техника'},
            {'word': 'school', 'translation': 'школа', 'hint': 'Учебное заведение'},
            {'word': 'teacher', 'translation': 'учитель', 'hint': 'Профессия'},
            {'word': 'student', 'translation': 'студент', 'hint': 'Учится'},
            {'word': 'library', 'translation': 'библиотека', 'hint': 'Место с книгами'},
            {'word': 'pencil', 'translation': 'карандаш', 'hint': 'Письменная принадлежность'}
        ]
        
    def generate_math_examples(self, count=10):
        """Генерирует математические примеры"""
        examples = []
        for i in range(count):
            operation = random.choice(self.math_operations)
            
            if operation == '+':
                a = random.randint(1, 50)
                b = random.randint(1, 50)
                result = a + b
                question = f"{a} + {b} = ?"
                difficulty = 'easy' if result < 50 else 'medium' if result < 100 else 'hard'
                coins = random.choice([5, 8, 10, 12, 15])
                
            elif operation == '-':
                a = random.randint(10, 100)
                b = random.randint(1, min(a-1, 50))
                result = a - b
                question = f"{a} - {b} = ?"
                difficulty = 'easy' if result < 30 else 'medium' if result < 70 else 'hard'
                coins = random.choice([5, 8, 10, 12, 15])
                
            elif operation == '*':
                a = random.randint(2, 12)
                b = random.randint(2, 12)
                result = a * b
                question = f"{a} × {b} = ?"
                difficulty = 'easy' if result < 25 else 'medium' if result < 80 else 'hard'
                coins = random.choice([8, 10, 12, 15, 18])
                
            else:  # деление
                b = random.randint(2, 10)
                result = random.randint(2, 20)
                a = b * result
                question = f"{a} ÷ {b} = ?"
                difficulty = 'easy' if result < 10 else 'medium' if result < 15 else 'hard'
                coins = random.choice([10, 12, 15, 18, 20])
            
            examples.append({
                'id': f"math_{i}",
                'question': question,
                'answer': str(result),
                'difficulty': difficulty,
                'category': 'math',
                'coins': coins,
                'hint': f'Используй операцию {operation}'
            })
        
        return examples
    
    def generate_english_examples(self, count=8):
        """Генерирует примеры по английскому языку"""
        examples = []
        selected_words = random.sample(self.english_words, min(count, len(self.english_words)))
        
        for i, word_data in enumerate(selected_words):
            examples.append({
                'id': f"eng_{i}",
                'question': f"Translate '{word_data['word']}'",
                'answer': word_data['translation'],
                'hint': word_data['hint'],
                'difficulty': 'easy',
                'category': 'english',
                'coins': random.choice([8, 10, 12, 15])
            })
        
        return examples
    
    def generate_geometry_examples(self, count=5):
        """Генерирует геометрические задачи"""
        examples = []
        
        # Прямоугольники
        for i in range(2):
            a = random.randint(3, 15)
            b = random.randint(3, 15)
            area = a * b
            perimeter = 2 * (a + b)
            
            if random.choice([True, False]):
                examples.append({
                    'id': f"geo_area_{i}",
                    'question': f'Найди площадь прямоугольника со сторонами {a} и {b} см',
                    'answer': str(area),
                    'hint': 'S = a × b',
                    'difficulty': 'medium' if area > 50 else 'easy',
                    'category': 'geometry',
                    'coins': 12 if area > 50 else 8
                })
            else:
                examples.append({
                    'id': f"geo_perimeter_{i}",
                    'question': f'Найди периметр прямоугольника со сторонами {a} и {b} см',
                    'answer': str(perimeter),
                    'hint': 'P = 2 × (a + b)',
                    'difficulty': 'medium' if perimeter > 30 else 'easy',
                    'category': 'geometry',
                    'coins': 10 if perimeter > 30 else 6
                })
        
        # Квадраты
        for i in range(1, 3):
            side = random.randint(3, 12)
            area = side * side
            perimeter = 4 * side
            
            if random.choice([True, False]):
                examples.append({
                    'id': f"geo_square_area_{i}",
                    'question': f'Найди площадь квадрата со стороной {side} см',
                    'answer': str(area),
                    'hint': 'S = a²',
                    'difficulty': 'medium' if area > 50 else 'easy',
                    'category': 'geometry',
                    'coins': 10 if area > 50 else 7
                })
            else:
                examples.append({
                    'id': f"geo_square_perimeter_{i}",
                    'question': f'Найди периметр квадрата со стороной {side} см',
                    'answer': str(perimeter),
                    'hint': 'P = 4 × a',
                    'difficulty': 'easy',
                    'category': 'geometry',
                    'coins': 6
                })
        
        # Круги
        for i in range(1, 2):
            radius = random.randint(2, 8)
            area = round(3.14 * radius * radius, 2)
            
            examples.append({
                'id': f"geo_circle_{i}",
                'question': f'Найди площадь круга с радиусом {radius} см (π ≈ 3.14)',
                'answer': str(area),
                'hint': 'S = π × r²',
                'difficulty': 'hard',
                'category': 'geometry',
                'coins': 20
            })
        
        return examples[:count]
    
    def generate_logic_examples(self, count=5):
        """Генерирует логические задачи"""
        examples = []
        
        logic_tasks = [
            {
                'question': 'Число следующее за 7',
                'answer': '8',
                'hint': 'Считай по порядку',
                'difficulty': 'easy',
                'coins': 5
            },
            {
                'question': 'Сколько дней в неделе?',
                'answer': '7',
                'hint': 'Понедельник, вторник...',
                'difficulty': 'easy',
                'coins': 5
            },
            {
                'question': 'Сколько месяцев в году?',
                'answer': '12',
                'hint': 'Январь, февраль...',
                'difficulty': 'easy',
                'coins': 5
            },
            {
                'question': 'Продолжи последовательность: 2, 4, 6, 8, ?',
                'answer': '10',
                'hint': 'Каждое число увеличивается на 2',
                'difficulty': 'medium',
                'coins': 8
            },
            {
                'question': 'Продолжи последовательность: 1, 3, 5, 7, ?',
                'answer': '9',
                'hint': 'Нечетные числа по порядку',
                'difficulty': 'medium',
                'coins': 8
            },
            {
                'question': 'Продолжи последовательность: 5, 10, 15, 20, ?',
                'answer': '25',
                'hint': 'Каждое число увеличивается на 5',
                'difficulty': 'medium',
                'coins': 10
            },
            {
                'question': 'Сколько минут в часе?',
                'answer': '60',
                'hint': 'В часе 60 минут',
                'difficulty': 'easy',
                'coins': 5
            },
            {
                'question': 'Сколько секунд в минуте?',
                'answer': '60',
                'hint': 'В минуте 60 секунд',
                'difficulty': 'easy',
                'coins': 5
            },
            {
                'question': 'Какое число пропущено: 10, 20, ?, 40',
                'answer': '30',
                'hint': 'Каждое число увеличивается на 10',
                'difficulty': 'medium',
                'coins': 8
            },
            {
                'question': 'Найди закономерность: 2, 4, 8, 16, ?',
                'answer': '32',
                'hint': 'Каждое число умножается на 2',
                'difficulty': 'hard',
                'coins': 15
            }
        ]
        
        selected_tasks = random.sample(logic_tasks, min(count, len(logic_tasks)))
        
        for i, task in enumerate(selected_tasks):
            examples.append({
                'id': f"logic_{i}",
                'question': task['question'],
                'answer': task['answer'],
                'hint': task['hint'],
                'difficulty': task['difficulty'],
                'category': 'logic',
                'coins': task['coins']
            })
        
        return examples
    
    def generate_all_examples(self, total_count=20):
        """Генерирует все типы примеров"""
        # Распределяем количество по категориям
        math_count = random.randint(6, 10)
        eng_count = random.randint(4, 6)
        geo_count = random.randint(3, 5)
        logic_count = total_count - math_count - eng_count - geo_count
        
        if logic_count < 2:
            logic_count = 2
            math_count = total_count - eng_count - geo_count - logic_count
        
        # Генерируем примеры
        all_examples = []
        all_examples.extend(self.generate_math_examples(math_count))
        all_examples.extend(self.generate_english_examples(eng_count))
        all_examples.extend(self.generate_geometry_examples(geo_count))
        all_examples.extend(self.generate_logic_examples(logic_count))
        
        # Перемешиваем
        random.shuffle(all_examples)
        
        return all_examples[:total_count]
    
    def save_to_file(self, filename='random_examples.json'):
        """Сохраняет примеры в JSON файл"""
        examples = self.generate_all_examples()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'success': True,
                'count': len(examples),
                'examples': examples,
                'categories': ['math', 'english', 'geometry', 'logic'],
                'generated_at': str(random.randint(1000000000, 9999999999))
            }, f, ensure_ascii=False, indent=2)
        
        print(f"Сгенерировано {len(examples)} примеров и сохранено в {filename}")
        return examples

if __name__ == "__main__":
    generator = RandomExamplesGenerator()
    
    # Генерируем и сохраняем примеры
    examples = generator.save_to_file()
    
    # Показываем статистику
    categories = {}
    for example in examples:
        category = example['category']
        if category not in categories:
            categories[category] = 0
        categories[category] += 1
    
    print("\nСтатистика по категориям:")
    for category, count in categories.items():
        print(f"  {category}: {count} примеров")
    
    print(f"\nВсего примеров: {len(examples)}")
    print("Файл готов для использования в REST API!")
