"""Скрипт для заполнения базы данных тестовыми автомобилями.

Запуск: python fill_db.py
"""
from datetime import date

from Car import Car
from Car_Сlass import Car_Class
from CarsLib import CarsLib
from Dimensions import Dimensions
from Engine import Engine
from Main import DB_PATH
from Tire import Tire


def make_car(id, brand, model, car_class, color, max_speed, dimensions, engine, tire, release, designer):
    car = Car()
    car.id = id
    car.brand = brand
    car.model = model
    car.car_class = car_class
    car.color = color
    car.max_speed = max_speed
    car.dimensions = dimensions
    car.engine = engine
    car.tire = tire
    car.release = release
    car.designer = designer
    return car


TEST_CARS = [
    make_car(
        1, "Toyota", "Camry", Car_Class.D_CLASS, "Белый", 210,
        Dimensions(4885, 1840, 1445),
        Engine(1, "Toyota", 249, 356, 3.5, "бензин", 6, "V-образный"),
        Tire(1, 235, 45, 18, "Bridgestone", "Летние", "W"),
        date(2018, 1, 8), "Масато Кацумата",
    ),
    make_car(
        2, "BMW", "M5", Car_Class.E_CLASS, "Синий", 305,
        Dimensions(4983, 1903, 1469),
        Engine(2, "BMW", 625, 750, 4.4, "бензин", 8, "V-образный"),
        Tire(2, 275, 35, 20, "Michelin", "Летние", "Y"),
        date(2017, 8, 21), "Карим Хабиб",
    ),
    make_car(
        3, "Lada", "Vesta", Car_Class.C_CLASS, "Серый", 182,
        Dimensions(4410, 1764, 1497),
        Engine(3, "ВАЗ", 106, 148, 1.6, "бензин", 4, "рядный"),
        Tire(3, 205, 55, 16, "Kama", "Всесезонные", "H"),
        date(2015, 9, 25), "Стив Маттин",
    ),
    make_car(
        4, "Volkswagen", "Polo", Car_Class.B_CLASS, "Красный", 198,
        Dimensions(4483, 1706, 1471),
        Engine(4, "Volkswagen", 110, 175, 1.4, "бензин", 4, "рядный"),
        Tire(4, 195, 55, 15, "Nokian", "Зимние", "T"),
        date(2020, 7, 1), "Клаус Бишофф",
    ),
    make_car(
        5, "Tesla", "Model 3", Car_Class.D_CLASS, "Черный", 261,
        Dimensions(4694, 1849, 1443),
        Engine(5, "Tesla", 513, 660, 0.0, "электро", 0, "два электромотора"),
        Tire(5, 235, 40, 19, "Pirelli", "Всесезонные", "W"),
        date(2017, 7, 28), "Франц фон Хольцхаузен",
    ),
    make_car(
        6, "Porsche", "911 Carrera", Car_Class.S_CLASS, "Желтый", 293,
        Dimensions(4519, 1852, 1298),
        Engine(6, "Porsche", 385, 450, 3.0, "бензин", 6, "оппозитный"),
        Tire(6, 305, 30, 21, "Pirelli", "Летние", "Y"),
        date(2019, 3, 5), "Михаэль Мауэр",
    ),
]


if __name__ == '__main__':
    lib = CarsLib(DB_PATH)

    added = 0
    for car in TEST_CARS:
        if lib.find_car_by_id(car.id) is None:
            lib.insert_car(car)
            added += 1

    print(f"Добавлено автомобилей: {added}")
    print(f"Всего в базе: {len(lib.get_all_cars())}")
    lib.connection.close()
