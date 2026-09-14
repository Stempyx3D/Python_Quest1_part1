import sys
def clients_sort(clients_data):
    for name, amount, status in clients_data:
        name_print = f"Клієнт: {name}"
        if not isinstance(amount, (int, float)):
            amount_print = "Сума: Фальшиві дані"
        else:
            if amount < 100:
                category = "Дрібнота"
            elif 100 <= amount <= 999:
                category = "Середнячок"
            else:
                category = "Великий клієнт"
            amount_print = f"Сума: {amount} — {category}"

        match status:
            case "clean":
                action = "Працювати без питань"
            case "suspicious":
                action = "Перевірити документи"
            case "fraud":
                action = "У чорний список"
            case _:
                action = "Невідомий статус"
        print(f"{name_print}, {amount_print}, Дія: {action}")
        pass

clients_data = [
    ("Олексій", 45, "clean"),
    ("Марія", 350.50, "suspicious"),
    ("Іван", 1200, "fraud"),
    ("Олена", "сто", "clean"),
    ("Дмитро", 150, "СБУ"),
    ("Анна", 588, "clean"),
    ("Сергій", 200, "suspicious"),
    ("Катерина", 500, "fraud"),
    ("Віктор", 75.25, "clean"),
    ("Наталія", 300, "suspicious"),
    ("Андрій", 1000, "fraud"),
    ("Ірина", 722, "clean"),
    ("Олександра", 250, "НАБУ")
]
clients_sort(clients_data)
sys.exit(0)