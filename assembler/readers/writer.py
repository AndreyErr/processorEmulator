import os
import logging
import sys

# Добавляем корень проекта в системный путь для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from utils.consts import DATA_SIZE

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def clean_text(text: str) -> str:
    """
    Удаляет комментарии и лишние пробелы из строки.

    :param text: Исходная строка
    :return: Очищенная строка без комментариев
    """
    parts = text.split('#')
    text = parts[0].strip()
    return text

def write_bin(output_file, value: int):
    """
    Записывает данные в бинарный формат.
    
    :param output_file: Открытый файл для записи
    :param value: Значение данных
    """
    # Преобразуем index и value в бинарные строки и дополняем их нулями
    value_bin = format(value, f"0{DATA_SIZE}b")    # Форматируем значение в двоичную строку

    # Записываем двоичные строки в файл в текстовом формате
    output_file.write(f"{value_bin}\n")
    
    logger.debug(f"Запись в выходной файл: значение={value_bin}")
