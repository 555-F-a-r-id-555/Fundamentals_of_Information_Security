import hashlib

def calculate_file_hash(file_path, algorithm='sha256'):
    """Вычисляет хеш файла с использованием указанного алгоритма."""
    try:
        hash_func = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):  # Читаем файл блоками по 8KB
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        return "Ошибка: Файл не найден!"
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
            choice = int(input("\nВыберите алгоритм (номер): "))
            if 1 <= choice <= len(algorithms):
                return algorithms[choice - 1]
            print("Ошибка: введите номер из списка!")
        except ValueError:
            print("Ошибка: введите число!")

if __name__ == "__main__":
    print("=== Вычисление хеша файла ===")
    
    # Запрос пути к файлу
    file_path = input("\nВведите путь к файлу: ").strip()
    
    # Запрос алгоритма
    algorithm = get_algorithm_choice()
    
    # Вычисление и вывод результата
    print(f"\nВычисляю {algorithm.upper()} хеш для файла: {file_path}")
    result = calculate_file_hash(file_path, algorithm)
    
    print("\n" + "="*50)
    if "Ошибка" not in result:
        print(f"Алгоритм: {algorithm.upper()}")
        print(f"Файл: {file_path}")
        print(f"Хеш: {result}")
    else:
        print(result)
    print("="*50)