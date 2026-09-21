class Dimensions:
    """Класс для хранения габаритов автомобиля."""

    def __init__(self, length=0.0, width=0.0, height=0.0):
        self.length = length
        self.width = width
        self.height = height

    def __str__(self):
        return (
            f"Длина: {self.length}\n"
            f"Ширина: {self.width}\n"
            f"Высота: {self.height}\n"
        )

    def input_manual(self):
        self.length = float(input("Введите длину в мм: "))
        self.width = float(input("Введите ширину в мм: "))
        self.height = float(input("Введите высоту в мм: "))

        return self

    def to_dict(self):
        return {
            "length": self.length,
            "width": self.width,
            "height": self.height,
        }
