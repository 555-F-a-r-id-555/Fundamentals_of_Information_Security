# pip install python-nmap
import os
import nmap
import json
from datetime import datetime

def nmap_scan(target, ports, arguments="-sV", output_file=None):
    """
    Функция для сканирования цели с помощью Nmap и сохранения результатов в файл.    
    :param target: Цель сканирования (IP или диапазон)
    :param ports: Порты для сканирования (например, "22,80,443" или "1-1000")
    :param arguments: Аргументы Nmap (по умолчанию: "-sV" для определения версий сервисов)
    :param output_file: Имя файла для сохранения результатов (если None, вывод только в консоль)
    :return: Результаты сканирования

    Усовершенствованная функция сканирования с сохранением в ./homework_6/
    Улучшения:
    1. Автоматическое создание папки homework_6
    2. Чёткое разделение JSON и текстового формата
    3. Проверка прав доступа к папке
    4. Корректная обработка путей для всех ОС
    """
    scanner = nmap.PortScanner()
    print(f"Сканирование {target} на портах {ports}...")
    
    try:
        # Создаём папку (если нужно)
        output_dir = "./homework_6"
        os.makedirs(output_dir, exist_ok=True)
        
        # Проверяем доступность папки
        if not os.access(output_dir, os.W_OK):
            raise PermissionError(f"Нет прав на запись в {output_dir}")

        # Сканирование
        scanner.scan(target, ports, arguments=arguments)
        
        # Формируем результаты
        scan_results = {
            "meta": {
                "target": target,
                "ports": ports,
                "arguments": arguments,
                "timestamp": datetime.now().isoformat()
            },
            "hosts": {
                host: {
                    "state": scanner[host].state(),
                    "protocols": {
                        proto: {
                            port: {
                                "state": scanner[host][proto][port]["state"],
                                "service": scanner[host][proto][port]["name"],
                                "details": {
                                    "product": scanner[host][proto][port].get("product", ""),
                                    "version": scanner[host][proto][port].get("version", "")
                                }
                            } for port in scanner[host][proto]
                        } for proto in scanner[host].all_protocols()
                    }
                } for host in scanner.all_hosts()
            }
        }

        # Вывод в консоль
        print("\nРезультаты сканирования:")
        print(json.dumps(scan_results, indent=2, ensure_ascii=False))

        # Сохранение в файл
        if output_file:
            full_path = os.path.join(output_dir, output_file)
            
            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    if output_file.lower().endswith('.json'):
                        json.dump(scan_results, f, indent=2, ensure_ascii=False)
                    else:
                        f.write(f"Отчёт сканирования\n{'='*30}\n")
                        f.write(f"Цель: {target}\nПорты: {ports}\nВремя: {scan_results['meta']['timestamp']}\n\n")
                        
                        for host, data in scan_results['hosts'].items():
                            f.write(f"[Хост] {host} ({data['state']})\n")
                            
                            for proto, ports_data in data['protocols'].items():
                                f.write(f"\n[Протокол] {proto.upper()}\n")
                                
                                for port, info in ports_data.items():
                                    f.write(f"\nПорт: {port}\nСтатус: {info['state']}\nСервис: {info['service']}\n")
                                    if info['details']['product']:
                                        f.write(f"Продукт: {info['details']['product']} {info['details']['version']}\n")

                print(f"\nФайл успешно сохранён: {os.path.abspath(full_path)}")
                
            except Exception as e:
                print(f"\nОшибка сохранения: {str(e)}")
                if isinstance(e, PermissionError):
                    print("Попробуйте запустить программу с правами администратора")

        return scan_results

    except nmap.PortScannerError as e:
        print(f"Ошибка Nmap: {str(e)}")
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
    return None

if __name__ == "__main__":
    target = input("Введите цель сканирования (IP или диапазон): ").strip()
    ports = input("Введите порты для сканирования (например '22,80,443'): ").strip()
    arguments = input("Введите аргументы Nmap (по умолчанию '-sV'): ").strip() or "-sV"
    
    while True:
        output_file = input("Введите имя файла (например 'scan_result.json'): ").strip()
        if output_file:  # Проверка на пустой ввод
            break
        print("Ошибка: имя файла не может быть пустым!")

    nmap_scan(target, ports, arguments, output_file)



# import os
# import nmap
# import json
# from datetime import datetime

# def nmap_scan(target, ports, arguments="-sV", output_file=None):
#     """
#     Функция для сканирования цели с помощью Nmap и сохранения результатов в файл.
    
#     :param target: Цель сканирования (IP или диапазон)
#     :param ports: Порты для сканирования (например, "22,80,443" или "1-1000")
#     :param arguments: Аргументы Nmap (по умолчанию: "-sV" для определения версий сервисов)
#     :param output_file: Имя файла для сохранения результатов (если None, вывод только в консоль)
#     :return: Результаты сканирования
#     """
#     scanner = nmap.PortScanner()
#     print(f"Сканирование {target} на портах {ports}...")
    
#     try:
#         # Создаём папку homework_6, если её нет
#         os.makedirs("./homework_6", exist_ok=True)
        
#         # Запуск сканирования
#         scanner.scan(target, ports, arguments=arguments)
        
#         # Собираем результаты в словарь
#         scan_results = {
#             "target": target,
#             "ports": ports,
#             "arguments": arguments,
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "hosts": {}
#         }
        
#         for host in scanner.all_hosts():
#             host_info = {
#                 "state": scanner[host].state(),
#                 "protocols": {}
#             }
            
#             for proto in scanner[host].all_protocols():
#                 ports_info = {}
                
#                 for port in scanner[host][proto].keys():
#                     ports_info[port] = {
#                         "state": scanner[host][proto][port]["state"],
#                         "service": scanner[host][proto][port]["name"],
#                         "product": scanner[host][proto][port].get("product", ""),
#                         "version": scanner[host][proto][port].get("version", ""),
#                     }
                
#                 host_info["protocols"][proto] = ports_info
            
#             scan_results["hosts"][host] = host_info
        
#         # Вывод в консоль
#         print("\nРезультаты сканирования:")
#         print(json.dumps(scan_results, indent=4, ensure_ascii=False))
    
#         #./homework_6/output_file.json
#         # Сохранение в файл (если указан output_file)
#         if output_file:
#             # Формируем полный путь: ./homework_6/{output_file}.json
#             if not output_file.endswith(".json"):
#                 output_file += ".json"
#             full_path = os.path.join("./homework_6", output_file)
#             try:
#                 with open(full_path, "w") as f:
#                     if output_file.endswith(".json"):
#                         json.dump(scan_results, f, indent=4, ensure_ascii=False)
#                     else:
#                         # Текстовый формат
#                         f.write(f"Результаты сканирования {target} ({datetime.now()})\n")
#                         f.write(f"Аргументы Nmap: {arguments}\n\n")
                        
#                         for host, info in scan_results["hosts"].items():
#                             f.write(f"Хост: {host} ({info['state']})\n")
                            
#                             for proto, ports in info["protocols"].items():
#                                 f.write(f"  Протокол: {proto}\n")
                                
#                                 for port, port_info in ports.items():
#                                     f.write(f"    Порт: {port}\tСостояние: {port_info['state']}\n")
#                                     f.write(f"    Сервис: {port_info['service']}\n")
#                                     if port_info["product"]:
#                                         f.write(f"    Продукт: {port_info['product']} {port_info['version']}\n")
#                                     f.write("\n")
                
#                 print(f"\nРезультаты сохранены в файл: {output_file}")
#             except Exception as e:
#                 print(f"Ошибка при сохранении файла: {e}")
        
#         return scan_results
    
#     except Exception as e:
#         print(f"Ошибка при сканировании: {e}")
#         return None

# if __name__ == "__main__":
#     target = input("Введите цель сканирования (IP или диапазон): ")
#     ports = input("Введите порты для сканирования (например '22,80,443'): ")
#     arguments = input("Введите аргументы Nmap (по умолчанию '-sV'): ") or "-sV"
#     output_file = input("Введите имя файла для сохранения (например 'scan_results.json'): ").strip() or None
    
#     nmap_scan(target, ports, arguments, output_file)


"""
Дополнительные аргументы Nmap:
-sS - SYN-сканирование (требует прав root)
-sV - определение версий сервисов
-O - определение ОС
-A - агрессивное сканирование (ОС, версии, скрипты)
-T4 - ускоренное сканирование

Если у вас нет прав root, используйте -sT (TCP-сканирование) вместо -sS.
Пример 1:
Введите цель сканирования: 192.168.1.1
Введите порты для сканирования: 80,443,22
Введите дополнительные аргументы Nmap: -sV
Пример 2:
Введите цель сканирования: 192.168.1.0/24
Введите порты для сканирования: 1-1000
Введите дополнительные аргументы Nmap: -sS -T4
"""