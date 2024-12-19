import os
import logging
import sys
from typing import Dict, TextIO

# Добавляем корень проекта в системный путь для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from utils.consts import INSTRUCTION_SET
from assembler.readers.writer import clean_text, write_bin

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def second_read(input_file, output_file, jmp_markers: Dict[str, int]):
    """
    Выполняет второй проход по входному файлу, обрабатывая инструкции и записи переходов.

    :param input_file: Путь к входному файлу
    :param output_file: Путь к выходному файлу
    :param jmp_markers: Словарь с метками переходов и их адресами
    """
    logger.debug("Начало второго прохода")
    instruction_num = 0  # Начальный счетчик инструкций
    
    # Чтение каждой строки файла
    for line in input_file:
        text = clean_text(line)
        
        if not text:
            logger.debug("Пропущена пустая строка")
            continue
        if text.startswith('.'):
            logger.debug(f"Найдена секция: {text}")
            if text == ".DATA":
                logger.debug("Пропускаем секцию .DATA")
                line = next(input_file, '')
                text = clean_text(line)
                # Пропускаем все строки до конца секции .DATA
                while text and not text.startswith('.'):
                    line = next(input_file, '')
                    text = clean_text(line)
                continue
            logger.debug(f"Обработка секции: {text}")
            instruction_num = instruct_parser(input_file, output_file, instruction_num, jmp_markers, text)
            continue
        else:
            logger.error(f"Неверная секция: {text}")
            exit(1)
    
    # Если не было записано ни одной инструкции, записываем пустую секцию
    if instruction_num == 0:
        write_bin(output_file, 0)
    # output_file.write("\n")


def instruct_parser(file: TextIO, output_file: TextIO, instruction_num: int, jmp_markers: Dict[str, int], text) -> int:
    """
    Обрабатывает секцию инструкций, записывая их в выходной файл.

    :param file: Открытый файл для чтения
    :param output_file: Открытый файл для записи
    :param instruction_num: Текущий номер инструкции
    :param jmp_markers: Словарь с метками переходов
    :return: Обновленный счетчик инструкций
    """
    section_name = clean_text(text).strip()[1:]  # Удаляем точку из имени секции
    logger.debug(f"Начало обработки секции: {section_name}, инструкция: {instruction_num}")
    
    for line in file:
        text = clean_text(line)
        if not text or text.startswith('.'):
            break
        
        parts = text.split()
        instruction = parts[0]
        logger.debug(f"Найдена инструкция: {text}")
        
        if instruction == "PUSH":
            try:
                data = int(parts[1], 10)
            except ValueError:
                logger.error(f"Неверное значение для инструкции: {text}")
                exit(1)
            instruction_num = write_bin(output_file, INSTRUCTION_SET["PUSH"])
            instruction_num = write_bin(output_file, data)
        elif instruction in ["JMP", "JNZ"]:
            data = jmp_markers.get(parts[1])
            if data is None:
                logger.error(f"Неизвестная метка перехода: {parts[1]}")
                exit(1)
            instruction_num = write_bin(output_file, INSTRUCTION_SET["PUSH"])
            instruction_num = write_bin(output_file, data)
            instruction_num = write_bin(output_file, INSTRUCTION_SET[instruction])
        else:
            instruction_num = write_bin(output_file, INSTRUCTION_SET[instruction])
    
    logger.debug(f"Завершена обработка секции: {section_name}, инструкция: {instruction_num}")
    return instruction_num
