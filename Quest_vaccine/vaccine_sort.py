import sys
def check_vaccine_type(vaccine_data):
    for item in vaccine_data:
        name, quantity, category, temperature = item
        if not (isinstance(name, str) and isinstance(quantity, int)
                and isinstance(category, str) and category in ("antibiotic", "vitamin", "vaccine", "painkiller", "syrup")
                and isinstance(temperature, (int, float))):
            print(f"{name}: Неправильний тип даних.")
            continue
        if temperature < 5:
            temperature_status = "Надто холодно"
        elif temperature > 25:
            temperature_status = "Надто жарко"
        else:
            temperature_status = "Норма"

        match category:
            case "antibiotic":
                category_type = "Рецептурний препарат"
            case "vitamin":
                category_type = "Вільний продаж"
            case "vaccine":
                category_type = "Потребує спецзберігання"
            case _:
                category_type = "Невідома категорія"

        print(f"{name}: {category_type}, {temperature_status}")

vaccine_data = [
    ("Амоксицилін", 100, "antibiotic", 18.5),
    ("Вітамін C", "багато", "vitamin", 20.0),
    ("Вакцина БЦЖ", 50, "vaccine", 2.0),
    ("Парацетамол", 200, "painkiller", 26.5),
    ("Амоксиклав", 150, "antibiotic", 19.5),
    ("Аскорбінка", "100 упаковок", "vitamin", 22.0),
    ("Вакцина проти грипу", 40, "vaccine", 3.0),
    ("Риб'ячий жир", 80, "vitamin", 27.2),
    ("Невідомий сироп", 10, "syrup", 12.0)
]

check_vaccine_type(vaccine_data)
sys.exit(0)























