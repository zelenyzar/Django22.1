import json

input_file = "foodstuff.json"
output_file = "foodstuff_fixed.json"

try:
    with open(input_file, "rb") as f:
        raw = f.read()
    data = raw.decode("utf-8")
    print("Файл уже в UTF‑8.")
except UnicodeDecodeError:
    print("UTF‑8 не подошёл, пробуем CP1251...")
    data = raw.decode("cp1251")

obj = json.loads(data)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(obj, f, ensure_ascii=False, indent=2)

print(f"Готово: {output_file} (UTF‑8, без BOM)")
