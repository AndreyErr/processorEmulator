import argparse
import logging
import os
import sys

# Добавляем корень проекта в системный путь для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from assembler.readers.firstFileProcess import first_read
from assembler.readers.secondFileProcess import second_read
from typing import TextIO 

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def print_map(jmp_markers: dict) -> str:
    return "\n".join(f"{key}: {value}" for key, value in jmp_markers.items())

def open_bin_file(output_filename: str) -> TextIO:
    """
    Создает или открывает файл BIN для записи.

    :param output_filename: Имя выходного файла
    :return: Объект файла, открытого для записи
    """
    try:
        output_file = open(output_filename, 'w')
        logger.debug(f"Файл создан: {output_filename}")
        return output_file
    except OSError as e:
        logger.error(f"Не удалось создать выходной файл: {e}")
        exit(1)

def open_asm_file(input_filename: str) -> TextIO:
    """
    Открывает файл ASM для чтения.

    :param input_filename: Имя входного файла
    :return: Объект файла, открытого для чтения
    """
    try:
        input_file = open(input_filename, 'r')
        logger.debug(f"Файл открыт: {input_filename}")
        return input_file
    except OSError as e:
        logger.error(f"Не удалось открыть входной файл: {e}")
        exit(1)

def main():
    """
    Главная функция программы. Выполняет конвертацию ассемблерного файла в бинарный файл.
    """
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description="Конвертер ассемблерных файлов в бинарные.")
    parser.add_argument("-f", "--input", default="arraysum.asm", help="Входной ассемблерный файл")
    parser.add_argument("-o", "--output", default="arraysum.bin", help="Выходной бинарный файл")
    args = parser.parse_args()

    try:
        input_file = open_asm_file(args.input)
        output_file = open_bin_file(args.output)
    except Exception as e:
        logger.error(f"Ошибка при открытии файлов: {e}")
        exit(1)

    # Инициализация словаря для jump-маркеров
    jmp_markers = {}

    first_read(input_file, output_file, jmp_markers)
    logger.debug(f"Завершен первый проход. Jump-маркеры: {print_map(jmp_markers)}")

    input_file.close()
    input_file = open_asm_file(args.input)

    second_read(input_file, output_file, jmp_markers)
    logger.debug("Завершен второй проход")

    output_file.close()
    input_file.close()
    logger.info(f"Конвертация завершена")

if __name__ == "__main__":
    main()
