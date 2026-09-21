import json

from datetime import datetime

from Car import Car
from Car_Сlass import Car_Class
from Dimensions import Dimensions
from Engine import Engine
from Tire import Tire


class CarsLib:
    """Класс, который управляет сущностями Car и работает с файлом JSON."""

    def __init__(self, path: str):
        self.path = path
        self.cars_list = []
        self.run_flag = False
        self.load()

    def start(self):

        self.run_flag = True

        while self.run_flag:
            print("=" * 40)
            print("1. Добавить авто")
            print("2. Редактировать авто")
            print("3. Удалить авто")
            print("4. Показать информацию об авто")
            print("5. Показать все авто")
            print("0. Закрыть программу")
            print("=" * 40)

            choice = input("Введите команду: ").strip()

            if choice == "1":
                self.add_car_manual()
            elif choice == "2":
                self.edit_car()
            elif choice == "3":
                self.remove_car()
            elif choice == "4":
                self.show()
            elif choice == "5":
                self.show_all()
            elif choice == "0":
                self.run_flag = False
                print("Программа завершена.")
            else:
                print("Такой команды нет!\n")

    def show(self):
        try:
            target_id = int(input("Введите реальный ID авто: "))
            car = self.find_car_by_id(target_id)

            if car:
                print("-" * 40)
                print(car)
                print("-" * 40)
            else:
                print(f"Автомобиль с ID {target_id} не найден!")
        except ValueError:
            print("Ошибка: нужно ввести числовое значение ID!")

    def find_car_by_id(self, target_id: int):
        for car in self.cars_list:
            if car.id == target_id:
                return car
        return None


    def show_all(self):
        print("\n" + "=" * 40)
        for index, car in enumerate(self.cars_list):
            print(f"ID записи в списке: {index}")
            print(car)
            print("-" * 40)

    def add_car_manual(self):
        """Ручной ввод машины и сохранение."""
        new_car = Car().input_manual()
        self.cars_list.append(new_car)
        self.save()
        print("Автомобиль успешно сохранен!\n")

    def edit_car(self):
        try:
            target_id = int(input("Введите ID авто для редактирования: "))
            car = self.find_car_by_id(target_id)

            if car is not None:
                print(f"\nРедактирование автомобиля с ID {target_id}:")
                car.input_manual()
                self.save()
                print("Данные успешно обновлены!\n")
            else:
                print(f"Автомобиль с ID {target_id} не найден!")
        except ValueError:
            print("Ошибка: нужно ввести число!")

    def remove_car(self):
        try:
            target_id = int(input("Введите ID авто для удаления: "))
            car = self.find_car_by_id(target_id)

            if car is not None:
                self.cars_list.remove(car)
                self.save()
                print(f"Автомобиль с ID {target_id} успешно удален!\n")
            else:
                print(f"Автомобиль с ID {target_id} не найден!")
        except ValueError:
            print("Ошибка: нужно ввести число!")

    def add_car_from_dict(self, data: dict):
        car = Car()
        car.id = data["id"]
        car.brand = data["brand"]
        car.model = data["model"]

        car_class_val = data["car_class"]
        car.car_class = None
        if car_class_val:
            for item in Car_Class:
                if item.value == car_class_val:
                    car.car_class = item
                    break
        car.color = data["color"]
        car.max_speed = data["max_speed"]

        if data["dimensions"]:
            d = data["dimensions"]
            car.dimensions = Dimensions(d["length"], d["width"], d["height"])

        if data["engine"]:
            e = data["engine"]
            car.engine = Engine(
                id=e["id"],
                brand=e["brand"],
                horsepower=e["horsepower"],
                torque=e["torque"],
                displacement=e["displacement"],
                fuel_type=e["fuel_type"],
                cylinders=e["cylinders"],
                layout=e["layout"],
            )

        if data["tire"]:
            t = data["tire"]
            car.tire = Tire(
                id=t["id"],
                width=t["width"],
                aspect_ratio=t["aspect_ratio"],
                diameter=t["diameter"],
                brand=t["brand"],
                season_tire=t["season_tire"],
                speed_index=t["speed_index"],
            )

        if data.get("release"):
            car.release = datetime.strptime(data["release"], "%Y-%m-%d").date()

        car.designer = data.get("designer", "")
        self.cars_list.append(car)

    def load(self):
        """Загрузка данных из JSON файла."""
        with open(self.path, "r", encoding="utf-8") as db:
            cars_raw = json.load(db)
            for item in cars_raw:
                self.add_car_from_dict(item)


    def save(self):
        """Сохранение списка авто в JSON файл."""
        cars_data = [car.to_dict() for car in self.cars_list]
        with open(self.path, "w", encoding="utf-8") as db:
            json.dump(cars_data, db, indent=4, ensure_ascii=False)
