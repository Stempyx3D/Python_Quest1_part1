from models import Transport, Car, Bus, Bicycle, ElectricCar
import sys
def transport_info(vehicles) -> None:
    for vehicle in vehicles:
        print(vehicle.info())
if __name__ == "__main__":
    vehicles = [
        Car(name="Легковий автомобіль", speed=120, capacity=5),
        Bus(name="Автобус", speed=80, capacity=50, passangers=45),
        Bicycle(name="Велосипед", speed=15),
        ElectricCar(name="Електромобіль", speed=100, capacity=4)
    ]
    transport_info(vehicles)
    sys.exit(0)