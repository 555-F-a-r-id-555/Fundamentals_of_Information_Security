import bcrypt

def hash_password(password: str) -> bytes:
    # Генерация соли (salt) и хеширование пароля
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(password: str, hashed_password: bytes) -> bool:
    # Проверка пароля против хешированного значения
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

if __name__ == "__main__":
    # Пример использования
    password = input("Введите пароль: ")
    
    # Хешируем пароль
    hashed = hash_password(password)
    print(f"Хешированный пароль: {hashed.decode('utf-8')}")
    
    # Проверяем пароль
    test_password = input("Введите пароль для проверки: ")
    if check_password(test_password, hashed):
        print("Пароль верный!")
    else:
        print("Пароль неверный!")