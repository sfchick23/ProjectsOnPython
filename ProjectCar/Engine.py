class Engine:
    """Класс для хранения параметров двигателя автомобиля."""

    def __init__(self, id=0, brand="", horsepower=0, torque=0, displacement=0.0, fuel_type="", cylinders=0, layout=""):
        self.id = id
        self.brand = brand
        self.horsepower = horsepower
        self.torque = torque
        self.displacement = displacement
        self.fuel_type = fuel_type
        self.cylinders = cylinders
        self.layout = layout


    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Марка: {self.brand}\n"
            f"Мощность: {self.horsepower} л.с.\n"
            f"Крутящий момент: {self.torque} Н*м\n"
            f"Объем: {self.displacement} л\n"
            f"Тип топлива: {self.fuel_type}\n"
            f"Количество цилиндров: {self.cylinders}\n"
            f"Компоновка: {self.layout}"
        )

    def input_manual(self):
        print("\n--- Ввод данных двигателя ---")
        self.id = int(input("Введите ID двигателя: "))
        self.brand = input("Введите марку двигателя: ")
        self.horsepower = int(input("Введите мощность (л.с.): "))
        self.torque = int(input("Введите крутящий момент (Н*м): "))
        self.displacement = float(input("Введите рабочий объем (л): "))
        self.fuel_type = input("Введите тип топлива (бензин/дизель/электро): ")
        self.cylinders = int(input("Введите количество цилиндров: "))
        self.layout = input("Введите компоновку (рядный/V-образный/оппозитный): ")
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "horsepower": self.horsepower,
            "torque": self.torque,
            "displacement": self.displacement,
            "fuel_type": self.fuel_type,
            "cylinders": self.cylinders,
            "layout": self.layout,
        }