from abc import ABC, abstractmethod

class Transport(ABC):
    def __init__(self, name: str, speed: int, capacity: int) -> None:
        if not isinstance(name, str):
            raise TypeError(f"Параметр 'name': {name} має бути рядком (str)")
        if not isinstance(speed, int) or speed <= 0:
            raise ValueError(f"Параметр 'speed': {speed} має бути додатним цілим числом (int)")
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError(f"Параметр 'capacity': {capacity} має бути додатним цілим числом (int)")
        self.name = name
        self.speed = speed
        self.capacity = capacity

    def move(self, distance: float) -> float:
        return distance / self.speed

    @abstractmethod
    def fuel_consumption(self, distance: float) -> float:
        pass

    def calculate_cost(self, distance: float, price_per_unit: float) -> float:
        return self.fuel_consumption(distance) * price_per_unit

    def info(self) -> str:
        return (f"Тип: {self.__class__.__name__}, Назва: {self.name}, Швидкість: {self.speed} км/год, Вантажопідйомність: {self.capacity} кг")

class Car(Transport):
    def fuel_consumption(self, distance: float) -> float:
        return distance * 0.07

class Bus(Transport):
    def __init__(self, name: str, speed: int, capacity: int, passangers: int) -> None:
        super().__init__(name, speed, capacity)
        self.passangers = passangers
    def check_passangers(self) -> str:
        if self.passangers > self.capacity:
            return "Перевантажено!"
        return "Місць достатньо"
    def fuel_consumption(self, distance: float) -> float:
        return distance * 0.15
    def info(self) -> str:
        base_info = super().info()
        return f"{base_info}, Кількість пасажирів: {self.passangers}, {self.check_passangers()}"

class Bicycle(Transport):
    def __init__(self, name: str, speed: int, capacity: int = 1) -> None:
        max_speed = min(speed, 20)
        super().__init__(name, max_speed, capacity)
    def fuel_consumption(self, distance: float) -> float:
        return 0.0

class ElectricCar(Car):
    def battery_usage(self, distance: float) -> float:
        return distance * 0.2
    def fuel_consumption(self, distance: float) -> float:
        return distance * 0.0
    def calculate_cost(self, distance: float, price_per_unit: float) -> float:
        return self.battery_usage(distance) * price_per_unit
    
        











