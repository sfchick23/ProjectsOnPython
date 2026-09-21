from enum import Enum

class Car_Class(Enum):
    A_CLASS = "A-class"
    B_CLASS = "B-class"
    C_CLASS = "C-class"
    D_CLASS = "D-class"
    E_CLASS = "E-class"
    F_CLASS = "F-class"
    M_CLASS = "M-class"
    S_CLASS = "S-class"
    J_CLASS = "J-class"

def choose_car_class():

    items = list(Car_Class)
    print("Выберите класс автомобиля:")
    for idx, item in enumerate(items, start=1):
        print(f"{idx}. {item.value}")

    while True:
        choice = input("Введите номер класса: ").strip()
        if choice.isdigit():
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(items):
                return items[choice_idx]
        print("Некорректный выбор! Попробуйте снова.")