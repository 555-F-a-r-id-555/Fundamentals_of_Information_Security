# pip install openpyxl

import pandas as pd

# === Настройка ===
input_file = "./homework_2/List_of_generated_threats.csv"
output_file = "./homework_2/Protective_measures_with_points_v3.csv"
output_file_v2 = "./homework_2/Protective_measures_with_points_v3.xlsx"
encoding = "utf-8"  # Можно заменить на 'utf-8-sig' или 'cp1251', если будет ошибка

# === Загрузка файла ===
df = pd.read_csv(input_file, encoding=encoding, sep=None, engine="python")

# === Подсчёт количества мер защиты в каждой строке ===
def count_measures(cell):
    if pd.isna(cell):
        return 0
    return len([m for m in cell.split(";\r\n") if m.strip()])

# === Применение функции и сортировка ===
df["Количество мер защиты"] = df["Меры защиты"].apply(count_measures)
result_df = df[["Идентификатор", "Наименование", "Меры защиты", "Количество мер защиты"]]
result_df = result_df.sort_values(by="Количество мер защиты", ascending=False).reset_index(drop=True)

# === Сохраняем результат ===
result_df.to_csv(output_file, index=False, encoding="utf-8-sig")
# === Сохраняем результат в Excel ===
result_df.to_excel(output_file_v2, index=False)

print(f"Готово! Файл сохранён как: {output_file}")
print(f"Также Excel-файл сохранён как: {output_file_v2}")
