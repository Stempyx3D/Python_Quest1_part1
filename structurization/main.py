import sys
from models import Medicine, Antibiotic, Vitamin, Vaccine
def med_info(medicines) -> None:
    for medicine in medicines:
        print(medicine.info())
if __name__ == "__main__":
    medicines = [
        Antibiotic(name="Амоксицилін", quantity=10, price=120.0),
        Antibiotic(name="Азитроміцин", quantity=8, price=160.0),
        Antibiotic(name="Цефтріаксон", quantity=15, price=95.0),
        Antibiotic(name="Ципрофлоксацин", quantity=12, price=75.5),
        Vitamin(name="Вітамін D3", quantity=25, price=85.5),
        Vitamin(name="Вітамін C", quantity=50, price=30.0),
        Vitamin(name="Омега-3", quantity=20, price=210.0),
        Vitamin(name="Магній B6", quantity=30, price=145.0),
        Vitamin(name="Комплекс Мультивітамін", quantity=18, price=320.0),
        Vaccine(name="Вакцина проти грипу", quantity=5, price=450.0),
        Vaccine(name="Вакцина КПК (кір, паротит, краснуха)", quantity=7, price=680.0),
        Vaccine(name="Вакцина проти вітряної віспи", quantity=4, price=1250.0),
        Vaccine(name="Вакцина проти дифтерії та правця (АДП-М)", quantity=15, price=310.0)
    ]
    med_info(medicines)
    sys.exit(0)