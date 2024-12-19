import os
import logging
from typing import Dict

# Для корректного импорта из других модулей добавляем корень проекта в системный путь
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from utils.consts import INSTRUCTION_SET
from assembler.readers.writer import clean_text, write_bin

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def first_read(input_file, output_file, jmp_markers: Dict[str, int]):
    logger.debug("Начало первого прохода")
    instruction_num = 0
    data_num = 0

    # Чтение данных из input_file
    for line in input_file:
        text = clean_text(line) 
        if not text:
            logger.debug("Пропущена пустая строка")
            continue
        elif text.startswith('.'):
            logger.debug(f"Секция: {text}")
            if text == ".DATA": 
                data_num = data_parser(input_file, output_file, data_num)
                continue
            instruction_num = instruct_reader(input_file, instruction_num, jmp_markers, text)
            continue
        else:
            logger.error(f"Неверная секция: {text}")
            exit(1)
    
    # Если данных не было, записываем пустую секцию
    if data_num == 0:
        write_bin(output_file, 0)


def instruct_reader(file, instruction_num: int, jmp_markers: Dict[str, int], currentLine) -> bool:
    section_name = clean_text(currentLine)[1:]
    jmp_markers[section_name] = instruction_num
    logger.debug(f"Секция: {section_name}, инструкция: {instruction_num}")
    
    for line in file:
        text = clean_text(line)
        if not text or text.startswith('.'):
            break
        
        parts = text.split(" ")
        instruction = parts[0]
        
        if instruction not in INSTRUCTION_SET:
            logger.error(f"Неверная инструкция: {instruction}")
            exit(1)
        
        # Увеличиваем счетчик инструкций в зависимости от типа команды
        if instruction == "PUSH":
            if len(parts) != 2:
                logger.error(f"Неверный формат инструкции: {text}")
                exit(1)
            instruction_num += 2
        elif instruction in ["JMP", "JNZ"]:
            if len(parts) != 2:
                logger.error(f"Неверный формат инструкции: {text}")
                exit(1)
            instruction_num += 3
        else:
            if len(parts) != 1:
                logger.error(f"Неверный формат инструкции: {text}")
                exit(1)
            instruction_num += 1
        
    logger.debug(f"Завершено чтение секции: {section_name}, инструкция: {instruction_num}")
    return instruction_num

def data_parser(file, output_file, data_num: int) -> bool:
    for line in file:
        text = clean_text(line)
        if not text or text.startswith('.'):
            break
        
        nums = text.split(" ")
        for num_str in nums:
            try:
                num = int(num_str)
            except ValueError:
                logger.error(f"Не удалось разобрать число: {num_str}")
                exit(1)
            write_bin(output_file, num)
            data_num += 1

    logger.debug("Завершена обработка секции .DATA")
    return data_num
