import hashlib

def check_password_complexity(password):
    # Проверка длины пароля
    if len(password) < 8:
        return False, "Пароль должен содержать не менее 8 символов"
    
    has_upper = False
    has_lower = False
    has_digit = False
    
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
    
    # Проверка всех условий
    messages = []
    if not has_upper:
        messages.append("Пароль должен содержать хотя бы одну заглавную букву")
    if not has_lower:
        messages.append("Пароль должен содержать хотя бы одну строчную букву")
    if not has_digit:
        messages.append("Пароль должен содержать хотя бы одну цифру")
    
    if messages:
        return False, "\n".join(messages)
    else:
        return True, "Пароль соответствует требованиям сложности"

def hash_password(password):
    # Создание хэша SHA-256 (можно выбрать другой алгоритм)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def main():
    print("Проверка сложности пароля и его хэширование")
    password = input("Введите пароль: ")
    
    is_complex, message = check_password_complexity(password)
    print(message)
    
    if is_complex:
        hashed = hash_password(password)
        print(f"Хэшированный пароль (SHA-256): {hashed}")

if __name__ == "__main__":
    main()