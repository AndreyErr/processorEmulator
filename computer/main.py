import argparse
import logging
import os
import sys

# Добавляем корень проекта в системный путь для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from computer.processor.processor import init_processor, start_processor, MEMORY
from computer.readers.memory_fill import memory_fill

def open_bin_file(bin_filename: str):
    """Открывает бинарный файл для чтения"""
    try:
        bin_file = open(bin_filename, 'r')  # Открываем файл для чтения бинарных данных
        logging.debug(f"Файл открыт: {bin_filename}")
        return bin_file
    except Exception as e:
        logging.error(f"Не удалось открыть бинарный файл: {e}")
        sys.exit(1)

def main():
    # Настройка логирования
    logging.basicConfig(level=logging.DEBUG)
    
    # Парсинг флагов командной строки
    parser = argparse.ArgumentParser(description="Эмулятор процессора")
    parser.add_argument("-f", "--file", default="arraysum.bin", help="Выходной бинарный файл")
    args = parser.parse_args()
    
    # Проверка существования файла
    if not os.path.exists(args.file):
        logging.error(f"Ошибка: Файл не найден по пути {args.file}")
        sys.exit(1)

    # Открытие бинарного файла
    bin_file = open_bin_file(args.file)
    
    # Инициализация процессора
    init_processor()
    
    # Заполнение памяти процессора
    memory_fill(bin_file)
    
    # Запуск процессора
    start_processor()

if __name__ == "__main__":
    main()
