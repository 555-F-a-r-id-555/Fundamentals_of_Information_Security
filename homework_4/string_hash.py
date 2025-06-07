import hashlib

def calculate_string_hash(input_string, algorithm='sha256'):
    """Вычисляет хеш строки с использованием указанного алгоритма."""
    try:
        hash_func = hashlib.new(algorithm)
        hash_func.update(input_string.encode('utf-8'))
        return hash_func.hexdigest()
    except Exception as e:
        return f"Ошибка: {e}"

def get_algorithm_choice():
    """Выводит меню выбора алгоритма и возвращает выбор пользователя."""
    print("\nДоступные алгоритмы хеширования:")
    algorithms = sorted(hashlib.algorithms_guaranteed)
    for i, algo in enumerate(algorithms, 1):
        print(f"{i}. {algo.upper()}")
    
    while True:
        try:
            choice = input("\nВыберите алгоритм (номер) или нажмите Enter для SHA-256: ").strip()
            if not choice:
                return 'sha256'
            choice = int(choice)
            if 1 <= choice <= len(algorithms):
                return algorithms[choice - 1]
            print("Ошибка: введите номер из списка!")
        except ValueError:
            print("Ошибка: введите число!")

def get_input_string():
    """Запрашивает у пользователя строку для хеширования."""
    print("\nВведите текст для хеширования (Ctrl+Z → Enter для завершения):")
    print("(Можно ввести несколько строк, завершите ввод комбинацией Ctrl+Z и Enter)")
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    return '\n'.join(lines)

if __name__ == "__main__":
    print("=== Вычисление хеша строки ===")
    
    # Запрос строки
    input_string = get_input_string()
    if not input_string:
        print("\nВы не ввели текст для хеширования!")
        exit()
    
    # Запрос алгоритма
    algorithm = get_algorithm_choice()
    
    # Вычисление и вывод результата
    print(f"\nВычисляю {algorithm.upper()} хеш для введенного текста...")
    result = calculate_string_hash(input_string, algorithm)
    
    print("\n" + "="*50)
    print(f"Алгоритм: {algorithm.upper()}")
    print(f"Исходный текст: {input_string[:50]}{'...' if len(input_string) > 50 else ''}")
    print(f"Хеш: {result}")
    print("="*50)