import bcrypt
import re
import hashlib
import requests

def check_password_complexity(password):
    errors = []
    
    if len(password) < 8:
        errors.append("❌ Длина пароля должна быть не менее 8 символов")
    if not re.search(r'[A-ZА-Я]', password):
        errors.append("❌ Добавьте хотя бы одну заглавную букву (A-Z, А-Я)")
    if not re.search(r'[a-zа-я]', password):
        errors.append("❌ Добавьте хотя бы одну строчную букву (a-z, а-я)")
    if not re.search(r'[0-9]', password):
        errors.append("❌ Добавьте хотя бы одну цифру (0-9)")
    if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?/~`\-="\\]', password):
        errors.append("❌ Добавьте хотя бы один спецсимвол (!@#$%^&* и т. д.)")
    if len(set(password)) < 5:
        errors.append("❌ Используйте не менее 5 уникальных символов")
    
    weak_passwords = ["123456", "password", "qwerty", "123456789", "admin"]
    if password.lower() in weak_passwords:
        errors.append("❌ Пароль слишком простой (есть в списках утечек)")
    
    return (False, errors) if errors else (True, "✅ Пароль соответствует всем требованиям!")

def check_hibp(password):
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            hashes = [line.split(":")[0] for line in response.text.splitlines()]
            return suffix in hashes
        return False
    except requests.RequestException:
        return False

def generate_strong_password():
    import random
    import string
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(12))

def main():
    print("🔒 Проверка сложности пароля и его хеширование (bcrypt + HIBP)")
    password = input("Введите пароль: ")
    
    # Сначала проверяем HIBP
    if check_hibp(password):
        print("\n⚠️ Внимание! Этот пароль найден в утечках данных. Использовать его небезопасно!")
        print("Пример безопасного пароля:", generate_strong_password())
        return
    
    # Затем проверяем сложность
    is_strong, message = check_password_complexity(password)
    if not is_strong:
        print("\nОшибки в пароле:")
        for error in message:
            print(error)
        print("\nСоветы по исправлению:")
        print("- Добавьте заглавные и строчные буквы, цифры и спецсимволы.")
        print("- Пример пароля:", generate_strong_password())
        return
    
    # Хеширование и вывод
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print("\n✅ Пароль надёжный! Хеш (bcrypt):", hashed)

if __name__ == "__main__":
    main()