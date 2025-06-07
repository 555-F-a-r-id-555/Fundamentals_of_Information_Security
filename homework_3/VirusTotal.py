import base64
import requests
import os
import json
from datetime import datetime

API_KEY = 'Api_Key'  # Замени на свой API ключ
BASE_URL = 'https://www.virustotal.com/api/v3'

HEADERS = {
    'x-apikey': API_KEY
}


def check_ip(ip):
    url = f'{BASE_URL}/ip_addresses/{ip}'
    response = requests.get(url, headers=HEADERS)
    return response.json()


def check_url(url_to_check):
    encoded = base64.urlsafe_b64encode(url_to_check.encode()).decode().strip('=')
    url = f'{BASE_URL}/urls/{encoded}'
    response = requests.get(url, headers=HEADERS)
    return response.json()


def upload_file(filepath):
    if not os.path.exists(filepath):
        return {'error': 'Файл не найден.'}

    url = f'{BASE_URL}/files'
    with open(filepath, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, headers=HEADERS, files=files)
    return response.json()

def save_result_to_file(data, prefix):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    folder = './homework_3'
    os.makedirs(folder, exist_ok=True)  
    filename = f'{prefix}_result_{timestamp}.json'
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Результат сохранён в файл: {filepath}")




def main():
    print("\n=== VirusTotal CLI Проверка ===")
    print("Выберите тип анализа:")
    print("1. Проверить IP-адрес")
    print("2. Проверить URL")
    print("3. Загрузить файл")

    choice = input("\nВаш выбор (1/2/3): ").strip()

    if choice == '1':
        ip = input("Введите IP-адрес: ").strip()
        result = check_ip(ip)
        prefix = f'ip_{ip.replace(".", "_")}'
    elif choice == '2':
        url = input("Введите URL (с http/https): ").strip()
        result = check_url(url)
        prefix = 'url'
    elif choice == '3':
        path = input("Введите путь к файлу: ").strip()
        result = upload_file(path)
        filename_only = os.path.basename(path)
        prefix = f'file_{filename_only.replace(".", "_")}'
    else:
        print("❌ Неверный выбор.")
        return

    print("\n=== Результат анализа ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    save = input("\n💾 Хотите сохранить результат в файл? (y/n): ").strip().lower()
    if save == 'y':
        save_result_to_file(result, prefix)
    else:
        print("Результат не сохранён.")


if __name__ == '__main__':
    main()
