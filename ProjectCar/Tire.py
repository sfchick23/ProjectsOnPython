class Tire:
    """Класс для хранения параметров шин."""

    def __init__(self, id=0, width=0, aspect_ratio=0, diameter=0, brand="", season_tire="", speed_index=""):
        self.id = id
        self.width = width
        self.aspect_ratio = aspect_ratio
        self.diameter = diameter
        self.brand = brand
        self.season_tire = season_tire
        self.speed_index = speed_index


    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Марка: {self.brand}\n"
            f"Параметры: {self.width}/{self.aspect_ratio} R{self.diameter}\n"
            f"Сезонность: {self.season_tire}\n"
            f"Индекс скорости: {self.speed_index}"
        )

    def input_manual(self):
        print("\n--- Ввод данных шин ---")
        self.id = int(input("Введите ID шин: "))
        self.brand = input("Введите производителя шин: ")
        self.width = int(input("Введите ширину профиля (мм): "))
        self.aspect_ratio = int(input("Введите высоту профиля (%): "))
        self.diameter = int(input("Введите посадочный диаметр (дюймы, R): "))
        self.season_tire = input("Введите сезонность (Летние/Зимние/Всесезонные): ")
        self.speed_index = input("Введите индекс скорости (например, H, V, W): ")
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "width": self.width,
            "aspect_ratio": self.aspect_ratio,
            "diameter": self.diameter,
            "brand": self.brand,
            "season_tire": self.season_tire,
            "speed_index": self.speed_index,
        }