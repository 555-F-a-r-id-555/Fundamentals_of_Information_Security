import bcrypt
import re

def check_password_complexity(password):
    errors = []
    
    # 1. Длина пароля (не менее 8 символов)
    if len(password) < 8:
        errors.append("Пароль должен содержать не менее 8 символов")
    
    # 2. Наличие заглавных букв
    if not re.search(r'[A-ZА-Я]', password):
        errors.append("Пароль должен содержать хотя бы одну заглавную букву")
    
    # 3. Наличие строчных букв
    if not re.search(r'[a-zа-я]', password):
        errors.append("Пароль должен содержать хотя бы одну строчную букву")
    
    # 4. Наличие цифр
    if not re.search(r'[0-9]', password):
        errors.append("Пароль должен содержать хотя бы одну цифру")
    
    # 5. Наличие спецсимволов
    if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?/~`\-="\\]', password):
        errors.append("Пароль должен содержать хотя бы один спецсимвол (!@#$%^&* и т. д.)")
    
    # 6. Проверка на слабые пароли
    weak_passwords = ["123456", "password", "qwerty", "123456789", "admin"]
    if password.lower() in weak_passwords:
        errors.append("Пароль слишком простой (используется в списках утечек)")
    
    # 7. Минимальное количество уникальных символов (не менее 5)
    if len(set(password)) < 5:
        errors.append("Пароль должен содержать не менее 5 уникальных символов")
    
    if errors:
        return False, "\n".join(errors)
    else:
        return True, "✅ Пароль соответствует всем требованиям сложности!"

def hash_password(password):
    # Генерация соли и хеширование пароля
    salt = bcrypt.gensalt()  # Автоматическая генерация "соли"
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()  # Возвращаем строку вместо bytes

def verify_password(password, hashed_password):
    # Проверка пароля против хеша
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def main():
    print("🔒 Проверка сложности пароля и его хеширование (bcrypt)")
    password = input("Введите пароль: ")
    
    is_strong, message = check_password_complexity(password)
    print(message)
    
    if is_strong:
        hashed = hash_password(password)
        print(f"🔐 Хешированный пароль (bcrypt): {hashed}")
        
        # Демонстрация проверки пароля
        test_password = input("\nПроверить пароль ещё раз (для верификации): ")
        if verify_password(test_password, hashed):
            print("✅ Пароль совпадает с хешем!")
        else:
            print("❌ Пароль не совпадает!")

if __name__ == "__main__":
    main()