import os

from CarsLib import CarsLib

# Файл базы лежит рядом с Main.py, откуда бы программу ни запускали
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cars.db")

if __name__ == '__main__':
    cars_lib = CarsLib(DB_PATH).start()
