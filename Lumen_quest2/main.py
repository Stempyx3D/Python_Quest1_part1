from abc import ABC, abstractmethod
from typing import List, Optional, Dict

class Cargo(ABC):
    def __init__(self, batch: str, name: str, qty: int, weight_kg: float, sector: str, status: str):
        self.batch = batch
        self.name = name
        self.qty = qty
        self.weight_kg = weight_kg
        self.sector = sector
        self.status = status

    @abstractmethod
    def label(self) -> str:
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(batch={self.batch}, name='{self.name}', weight={self.weight_kg}kg)"

class AntibioticCargo(Cargo):
    def label(self) -> str:
        return "Антибактеріальний препарат"

class VitaminCargo(Cargo):
    def label(self) -> str:
        return "Вітамінний комплекс"

class VaccineCargo(Cargo):
    def label(self) -> str:
        return "Вакцина (термочутливий вантаж)"

class UnknownCargo(Cargo):
    def __init__(self, batch: str, name: str, qty: int, weight_kg: float, sector: str, status: str, original_category: str):
        super().__init__(batch, name, qty, weight_kg, sector, status)
        self.original_category = original_category

    def label(self) -> str:
        return f"[UNKNOWN: {self.original_category}] Невідомий вантаж (потребує експертизи)"

def cargo_factory(batch: str, name: str, category: str, qty: int, weight_kg: float, sector: str, status: str) -> Cargo:
    cat = category.strip().lower()
    if cat == "antibiotic":
        return AntibioticCargo(batch, name, qty, weight_kg, sector, status)
    elif cat == "vitamin":
        return VitaminCargo(batch, name, qty, weight_kg, sector, status)
    elif cat == "vaccine":
        return VaccineCargo(batch, name, qty, weight_kg, sector, status)
    else:
        return UnknownCargo(batch, name, qty, weight_kg, sector, status, original_category=category)

class WarehouseStorage(ABC):
    @abstractmethod
    def all(self) -> List[Cargo]:
        pass
    @abstractmethod
    def get(self, batch: str) -> Optional[Cargo]:
        pass
    @abstractmethod
    def by_sector(self, sector: str) -> List[Cargo]:
        pass

class FileWarehouseStorage(WarehouseStorage):
    def __init__(self, filepath: str):
        self._items: Dict[str, Cargo] = {}
        self.warnings: List[str] = []
        self.load(filepath)
    def load(self, filepath: str):
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        if not lines:
            return
        for idx, line in enumerate(lines[1:], start=2):
            raw_line = line.strip()
            if not raw_line:
                continue

            parts = [p.strip() for p in raw_line.split("|")]
            
            if len(parts) != 7:
                msg = f"Рядок {idx}: Очікувалося 7 колонок, знайдено {len(parts)} -> '{raw_line}'"
                self.warnings.append(msg)
                print(f"[ПОПЕРЕДЖЕННЯ] {msg}")
                continue

            batch, name, category, qty_str, weight_str, sector, status = parts

            if not batch:
                msg = f"Рядок {idx}: Відсутній номер партії (batch порожній)"
                self.warnings.append(msg)
                print(f"[ПОПЕРЕДЖЕННЯ] {msg}")
                continue

            try:
                qty = int(qty_str)
            except ValueError:
                msg = f"Рядок {idx}: Некоректне значення кількості qty='{qty_str}' (очікувалось ціле число)"
                self.warnings.append(msg)
                print(f"[ПОПЕРЕДЖЕННЯ] {msg}")
                continue

            try:
                weight_kg = float(weight_str.replace(",", "."))
            except ValueError:
                msg = f"Рядок {idx}: Некоректне значення ваги weight_kg='{weight_str}'"
                self.warnings.append(msg)
                print(f"[ПОПЕРЕДЖЕННЯ] {msg}")
                continue

            cargo = cargo_factory(batch, name, category, qty, weight_kg, sector, status)
            self._items[batch] = cargo

    def all(self) -> List[Cargo]:
        return list(self._items.values())

    def get(self, batch: str) -> Optional[Cargo]:
        return self._items.get(batch)

    def by_sector(self, sector: str) -> List[Cargo]:
        return [item for item in self._items.values() if item.sector.upper() == sector.upper()]

class InMemoryWarehouseStorage(WarehouseStorage):
    def __init__(self, items: Optional[List[Cargo]] = None):
        self._items: Dict[str, Cargo] = {item.batch: item for item in (items or [])}
    def add(self, item: Cargo):
        self._items[item.batch] = item
    def all(self) -> List[Cargo]:
        return list(self._items.values())
    def get(self, batch: str) -> Optional[Cargo]:
        return self._items.get(batch)
    def by_sector(self, sector: str) -> List[Cargo]:
        return [item for item in self._items.values() if item.sector.upper() == sector.upper()]

def generate_report(storage: WarehouseStorage):
    print("\n" + "=" * 60)
    print("           ЗВІТ: ЗГОРІЛІ ВАНТАЖІ В СЕКТОРІ С")
    print("=" * 60)

    sector_c_items = storage.by_sector("C")
    burned_items = [item for item in sector_c_items if item.status.lower() == "згоріло"]

    total_weight = 0.0

    print(f"{'Партія':<8} | {'Назва':<25} | {'Мітка':<20} | {'Вага (кг)':<10}")
    print("-" * 70)

    for item in burned_items:
        total_weight += item.weight_kg
        is_unknown = " (НЕВІДОМИЙ)" if isinstance(item, UnknownCargo) else ""
        print(f"{item.batch:<8} | {item.name:<25} | {item.label()}{is_unknown} | {item.weight_kg:>6.1f} кг")

    print("-" * 70)
    print(f"Всього згорілих партій: {len(burned_items)}")
    print(f"Загальна вага згорілого: {total_weight:.1f} кг")
    print("=" * 60 + "\n")

def test_in_memory_storage():
    storage = InMemoryWarehouseStorage()
    c1 = AntibioticCargo("T-1", "Тест-Антибіотик", 100, 15.0, "C", "згоріло")
    c2 = UnknownCargo("T-2", "Секретний реагент", 50, 10.5, "C", "згоріло", "alien_bio")
    c3 = VaccineCargo("T-3", "Вакцина", 20, 5.0, "A", "на складі")

    storage.add(c1)
    storage.add(c2)
    storage.add(c3)

    assert len(storage.all()) == 3
    assert storage.get("T-1") == c1
    assert len(storage.by_sector("C")) == 2
    assert len(storage.by_sector("A")) == 1
    assert isinstance(storage.get("T-2"), UnknownCargo)
    print("Усі тести для InMemoryWarehouseStorage успішно пройдено!")

if __name__ == "__main__":
    test_in_memory_storage()
    storage = FileWarehouseStorage("inventory_recovered.txt")
    generate_report(storage)




    