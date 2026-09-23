from abc import ABC, abstractmethod

class Medicine(ABC):
    def __init__(self, name: str, quantity: str, price: float) -> None:
        if not isinstance(name, str):
            raise TypeError(f"Параметр name: {name} має бути str")
        if not isinstance(quantity, int):
            raise TypeError(f"Параметр quantity: {quantity} має бути int")
        if not isinstance(price, (int, float)):
            raise TypeError(f"Параметр price: {price} має бути float/int")
        self.name = name
        self.quantity = quantity
        self.price = price

    @abstractmethod
    def requires_prescription(self) -> bool:
        pass
    @abstractmethod
    def storage_requirements(self) -> str:
        pass
    def total_price(self) -> float:
        return self.quantity * self.price
    def info(self) -> str:
        text = None
        if self.requires_prescription():
            text = "Потріббен рецепт"
        else:
            text = "Без рецепта"
        return f"Тип: {self.__class__.__name__}, Назва: {self.name}, Кількість: {self.quantity}, Ціна: {self.price}, {text}, Умови зберігання: {self.storage_requirements()}"

class Antibiotic(Medicine):
    def requires_prescription(self) -> bool:
        return True
    def storage_requirements(self) -> str:
        return "8–15°C, темне місце"

class Vitamin(Medicine):
    def requires_prescription(self) -> bool:
        return False
    def storage_requirements(self) -> str:
        return "15–25°C, сухо"

class Vaccine(Medicine):
    def requires_prescription(self) -> bool:
        return True
    def storage_requirements(self) -> str:
        return "2–8°C, холодильник"

    def total_price(self) -> float:
        new_price = super().total_price()
        return round(new_price * 1.2, 2)
    
    










