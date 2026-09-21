from datetime import date

import Car_Сlass
from Car_Сlass import Car_Class
from Dimensions import Dimensions
from Engine import Engine
from Tire import Tire


class Car:
    """Класс, который описывает сущность автомобиля."""

    def __init__(self):
        self.id: int = 0
        self.brand: str = ""
        self.model: str = ""
        self.car_class: Car_Class | None = None
        self.color: str = ""
        self.max_speed: int = 0
        self.dimensions: Dimensions | None = None
        self.engine: Engine | None = None
        self.tire: Tire | None = None
        self.release: date | None = None
        self.designer: str = ""

    def __str__(self):
        release_str = self.release.strftime("%d.%m.%Y") if self.release else "Не указана"
        car_class_str = self.car_class.value if self.car_class else "Не выбран"

        return (
            f"ID: {self.id}\n"
            f"Бренд: {self.brand}\n"
            f"Модель: {self.model}\n"
            f"Класс: {car_class_str}\n"
            f"Цвет: {self.color}\n"
            f"Макс. скорость: {self.max_speed} км/ч\n"
            f"Габариты: {self.dimensions}\n"
            f"Двигатель: {self.engine}\n"
            f"Шины: {self.tire}\n"
            f"Дата выхода: {release_str}\n"
            f"Дизайнер: {self.designer}"
        )

    def input_manual(self):
        print("=== Ввод данных об автомобиле ===")
        self.id = int(input("Введите ID: "))
        self.brand = input("Введите бренд: ")
        self.model = input("Введите модель: ")
        self.car_class = Car_Сlass.choose_car_class()
        self.color = input("Введите цвет: ")
        self.max_speed = int(input("Введите максимальную скорость: "))
        self.dimensions = Dimensions().input_manual()
        self.engine = Engine().input_manual()
        self.tire = Tire().input_manual()

        self.release = date(
            int(input("Введите год выхода авто: ")),
            int(input("Введите месяц выхода авто: ")),
            int(input("Введите день выхода авто: ")),
        )

        self.designer = input("Введите дизайнера: ")
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "car_class": self.car_class.value if self.car_class else None,
            "color": self.color,
            "max_speed": self.max_speed,
            "dimensions": self.dimensions.to_dict() if self.dimensions else None,
            "engine": self.engine.to_dict() if self.engine else None,
            "tire": self.tire.to_dict() if self.tire else None,
            "release": self.release.strftime("%Y-%m-%d") if self.release else None,
            "designer": self.designer,
        }
