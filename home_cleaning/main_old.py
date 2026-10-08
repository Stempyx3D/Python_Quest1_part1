
class JunkItem:
    def __init__(self, name: str, quantity: int, value: float):
        self.name = name
        self.quantity = quantity
        self.value = value

class JunkStorage:
    @staticmethod
    def serialize(items: list[JunkItem], filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            for item in items:
                if "|" in item.name:
                    raise ValueError("Назва предмета не може містити символ |")
                value = str(item.value).replace(".", ",")
                line = (f"{item.name}|"
                        f"{item.quantity}|"
                        f"{value}\n")
                file.write(line)
    @staticmethod
    def parse(filename: str) -> list[JunkItem]:
        items = []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for number, line in enumerate(file, start=1):
                    try:
                        parts = line.strip().split("|")
                        if len(parts) != 3:
                            raise ValueError("має бути рівно 3 поля")
                        name, quantity, value = parts
                        quantity = int(quantity)
                        value = float(value.replace(",", "."))
                        item = JunkItem(name,quantity,value)
                    except ValueError as error:
                        print(f"Попередження: рядок {number} "
                              f"пропущено: {line.strip()} "
                              f"({error})")
                    else:
                        items.append(item)
        except FileNotFoundError:
            return []
        return items
    
class StorageBackend:
    def save(self, items: list[JunkItem]) -> None:
        raise NotImplementedError
    def load(self) -> list[JunkItem]:
        raise NotImplementedError
    
class FileJunkStorage(StorageBackend):
    def __init__(self, filename: str):
        self.filename = filename
    def save(self, items: list[JunkItem]) -> None:
        JunkStorage.serialize(items,self.filename)
    def load(self) -> list[JunkItem]:
        return JunkStorage.parse(self.filename)
    
def add_item(storage: StorageBackend,item: JunkItem) -> None:
    items = storage.load()
    items.append(item)
    storage.save(items)
def find_item(storage: StorageBackend,name: str) -> JunkItem | None:
    items = storage.load()
    for item in items:
        if item.name == name:
            return item
    return None

storage = FileJunkStorage("junk.txt")

items = [
    JunkItem("Бляшанка", 5, 2.5),
    JunkItem("Стара плата", 3, 7.8),
    JunkItem("Купка дротів", 10, 1.2)
]

storage.save(items)
loaded_items = storage.load()

print("Предмети після читання:")

for item in loaded_items:
    print(item)

def assert_loaded_items(num, name, quantity, value) -> None:
    assert loaded_items[num].name == name
    assert loaded_items[num].quantity == quantity
    assert loaded_items[num].value == value
assert_loaded_items(0, "Бляшанка", 5, 2.5)
assert_loaded_items(1, "Стара плата", 3, 7.8)
assert_loaded_items(2, "Купка дротів", 10, 1.2)

print("Перевірка пройдена успішно!")