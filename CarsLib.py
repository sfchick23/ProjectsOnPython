import sqlite3

from datetime import datetime

from Car import Car
from Car_Сlass import Car_Class
from Dimensions import Dimensions
from Engine import Engine
from Tire import Tire


class CarsLib:
    """Класс, который управляет сущностями Car и работает с базой данных SQLite."""

    def __init__(self, path: str):
        self.path = path
        self.run_flag = False
        # Подключаемся к файлу базы данных (если файла нет, SQLite создаст его сам)
        self.connection = sqlite3.connect(self.path)
        # Позволяет обращаться к колонкам по имени: row["brand"]
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        """Создание таблиц, если их ещё нет."""
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS engines (
                id           INTEGER PRIMARY KEY,
                brand        TEXT,
                horsepower   INTEGER,
                torque       INTEGER,
                displacement REAL,
                fuel_type    TEXT,
                cylinders    INTEGER,
                layout       TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tires (
                id           INTEGER PRIMARY KEY,
                width        INTEGER,
                aspect_ratio INTEGER,
                diameter     INTEGER,
                brand        TEXT,
                season_tire  TEXT,
                speed_index  TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id        INTEGER PRIMARY KEY,
                brand     TEXT NOT NULL,
                model     TEXT NOT NULL,
                car_class TEXT,
                color     TEXT,
                max_speed INTEGER,
                length    REAL,
                width     REAL,
                height    REAL,
                engine_id INTEGER REFERENCES engines(id),
                tire_id   INTEGER REFERENCES tires(id),
                release   TEXT,
                designer  TEXT
            )
        """)

        self.connection.commit()

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
                self.connection.close()
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
        """READ: поиск одной машины по ID."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM cars WHERE id = ?", (target_id,))
        row = cursor.fetchone()

        if row is None:
            return None
        return self.car_from_row(row)

    def get_all_cars(self):
        """READ: получение всех машин из таблицы."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM cars ORDER BY id")
        return [self.car_from_row(row) for row in cursor.fetchall()]

    def show_all(self):
        cars = self.get_all_cars()

        print("\n" + "=" * 40)
        if not cars:
            print("Список автомобилей пуст.")
        for car in cars:
            print(car)
            print("-" * 40)

    def add_car_manual(self):
        """CREATE: ручной ввод машины и сохранение в базу."""
        try:
            new_car = Car().input_manual()
        except ValueError:
            print("Ошибка: введено некорректное значение!\n")
            return

        if self.find_car_by_id(new_car.id) is not None:
            print(f"Автомобиль с ID {new_car.id} уже существует!\n")
            return

        self.insert_car(new_car)
        print("Автомобиль успешно сохранен!\n")

    def edit_car(self):
        """UPDATE: редактирование машины."""
        try:
            target_id = int(input("Введите ID авто для редактирования: "))
            car = self.find_car_by_id(target_id)

            if car is not None:
                print(f"\nРедактирование автомобиля с ID {target_id}:")
                car.input_manual()

                if car.id != target_id and self.find_car_by_id(car.id) is not None:
                    print(f"Автомобиль с ID {car.id} уже существует!\n")
                    return

                self.update_car(target_id, car)
                print("Данные успешно обновлены!\n")
            else:
                print(f"Автомобиль с ID {target_id} не найден!")
        except ValueError:
            print("Ошибка: нужно ввести число!")

    def remove_car(self):
        """DELETE: удаление машины."""
        try:
            target_id = int(input("Введите ID авто для удаления: "))
            car = self.find_car_by_id(target_id)

            if car is not None:
                self.delete_car(target_id)
                print(f"Автомобиль с ID {target_id} успешно удален!\n")
            else:
                print(f"Автомобиль с ID {target_id} не найден!")
        except ValueError:
            print("Ошибка: нужно ввести число!")

    def save_engine_and_tire(self, car: Car):
        """Сохраняет двигатель и шины машины в их таблицы.

        INSERT OR REPLACE: если запись с таким ID уже есть, она перезаписывается.
        """
        cursor = self.connection.cursor()

        if car.engine:
            cursor.execute(
                "INSERT OR REPLACE INTO engines "
                "(id, brand, horsepower, torque, displacement, fuel_type, cylinders, layout) "
                "VALUES (:id, :brand, :horsepower, :torque, :displacement, :fuel_type, :cylinders, :layout)",
                car.engine.to_dict(),
            )

        if car.tire:
            cursor.execute(
                "INSERT OR REPLACE INTO tires "
                "(id, width, aspect_ratio, diameter, brand, season_tire, speed_index) "
                "VALUES (:id, :width, :aspect_ratio, :diameter, :brand, :season_tire, :speed_index)",
                car.tire.to_dict(),
            )

    def car_to_row(self, car: Car):
        """Превращает объект Car в набор значений для таблицы cars."""
        return {
            "id": car.id,
            "brand": car.brand,
            "model": car.model,
            "car_class": car.car_class.value if car.car_class else None,
            "color": car.color,
            "max_speed": car.max_speed,
            "length": car.dimensions.length if car.dimensions else None,
            "width": car.dimensions.width if car.dimensions else None,
            "height": car.dimensions.height if car.dimensions else None,
            "engine_id": car.engine.id if car.engine else None,
            "tire_id": car.tire.id if car.tire else None,
            "release": car.release.strftime("%Y-%m-%d") if car.release else None,
            "designer": car.designer,
        }

    def insert_car(self, car: Car):
        """Добавление новой машины в базу (INSERT)."""
        self.save_engine_and_tire(car)
        self.connection.execute(
            "INSERT INTO cars "
            "(id, brand, model, car_class, color, max_speed, length, width, height, "
            "engine_id, tire_id, release, designer) "
            "VALUES (:id, :brand, :model, :car_class, :color, :max_speed, :length, :width, :height, "
            ":engine_id, :tire_id, :release, :designer)",
            self.car_to_row(car),
        )
        self.connection.commit()

    def update_car(self, old_id: int, car: Car):
        """Изменение существующей машины в базе (UPDATE)."""
        self.save_engine_and_tire(car)
        params = self.car_to_row(car)
        params["old_id"] = old_id
        self.connection.execute(
            "UPDATE cars SET "
            "id = :id, brand = :brand, model = :model, car_class = :car_class, color = :color, "
            "max_speed = :max_speed, length = :length, width = :width, height = :height, "
            "engine_id = :engine_id, tire_id = :tire_id, release = :release, designer = :designer "
            "WHERE id = :old_id",
            params,
        )
        self.connection.commit()

    def delete_car(self, car_id: int):
        """Удаление машины из базы (DELETE)."""
        self.connection.execute("DELETE FROM cars WHERE id = ?", (car_id,))
        self.connection.commit()

    def car_from_row(self, row) -> Car:
        """Собирает объект Car из строки таблицы cars (+ двигатель и шины из своих таблиц)."""
        car = Car()
        car.id = row["id"]
        car.brand = row["brand"]
        car.model = row["model"]

        car.car_class = None
        if row["car_class"]:
            for item in Car_Class:
                if item.value == row["car_class"]:
                    car.car_class = item
                    break

        car.color = row["color"]
        car.max_speed = row["max_speed"]

        if row["length"] is not None:
            car.dimensions = Dimensions(row["length"], row["width"], row["height"])

        cursor = self.connection.cursor()

        if row["engine_id"] is not None:
            cursor.execute("SELECT * FROM engines WHERE id = ?", (row["engine_id"],))
            e = cursor.fetchone()
            if e:
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

        if row["tire_id"] is not None:
            cursor.execute("SELECT * FROM tires WHERE id = ?", (row["tire_id"],))
            t = cursor.fetchone()
            if t:
                car.tire = Tire(
                    id=t["id"],
                    width=t["width"],
                    aspect_ratio=t["aspect_ratio"],
                    diameter=t["diameter"],
                    brand=t["brand"],
                    season_tire=t["season_tire"],
                    speed_index=t["speed_index"],
                )

        if row["release"]:
            car.release = datetime.strptime(row["release"], "%Y-%m-%d").date()

        car.designer = row["designer"] or ""
        return car
