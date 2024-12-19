import os
import logging
import sys

# Добавляем корень проекта в системный путь для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from utils.consts import DATA_SIZE

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def clean_text(text: str) -> str:
    parts = text.split('#')
    text = parts[0].strip()
    return text

def write_bin(output_file, value: int):
    value_bin = format(value, f"0{DATA_SIZE}b")
    output_file.write(f"{value_bin}\n")
    logger.debug(f"Запись в бин файл: значение={value_bin}")
