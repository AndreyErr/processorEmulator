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
    """
    Выполняет первый проход по входному файлу, обрабатывая секции и команды.
    
    :param input_file: Открытый файл для чтения
    :param output_file: Открытый файл для записи
    :param jmp_markers: Словарь меток переходов и их позиций
    """
    logger.debug("Начало первого прохода")
    instruction_num = 0
    data_num = 0

    # Чтение данных из input_file
    for line in input_file:
        text = clean_text(line)  # Очищаем текст строки от пробелов
        if not text:  # Пропускаем пустые строки
            logger.debug("Пропущена пустая строка")
            continue
        elif text.startswith('.'):  # Если строка начинается с точки, это секция
            logger.debug(f"Найдена секция: {text}")
            if text == ".DATA":  # Если секция .DATA, обрабатываем данные
                logger.debug("Обработка секции .DATA")
                data_num = data_parser(input_file, output_file, data_num)
                continue
            logger.debug(f"Чтение секции: {text}")  # Обрабатываем команды
            instruction_num = instruct_reader(input_file, instruction_num, jmp_markers, text)
            continue
        else:  # Если секция неизвестна, выводим ошибку и завершаем работу
            logger.error(f"Неверная секция: {text}")
            exit(1)
    
    # Если данных не было, записываем пустую секцию
    if data_num == 0:
        write_bin(output_file, 0)


def instruct_reader(file, instruction_num: int, jmp_markers: Dict[str, int], currentLine) -> bool:
    """
    Обрабатывает секцию инструкций, обновляя словарь меток и подсчитывая количество инструкций.
    
    :param file: Открытый файл для чтения инструкций
    :param instruction_num: Текущий номер инструкции
    :param jmp_markers: Словарь меток переходов
    :return: True, если секция успешно обработана
    """
    section_name = clean_text(currentLine)[1:]  # Читаем имя секции и удаляем точку
    jmp_markers[section_name] = instruction_num  # Сохраняем метку перехода
    logger.debug(f"Сохранена секция: {section_name}, инструкция: {instruction_num}")
    
    for line in file:
        text = clean_text(line)
        if not text or text.startswith('.'):  # Если пустая строка или новая секция
            break
        
        parts = text.split(" ")  # Разделяем строку на части
        instruction = parts[0]
        
        if instruction not in INSTRUCTION_SET:  # Проверяем, является ли инструкция допустимой
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
    """
    Обрабатывает секцию .DATA, записывая данные в выходной файл.
    
    :param file: Открытый файл для чтения данных
    :param output_file: Открытый файл для записи данных
    :param data_num: Текущий номер данных
    :return: True, если секция успешно обработана
    """
    for line in file:
        text = clean_text(line)
        if not text or text.startswith('.'):  # Прерываем обработку, если началась новая секция
            break
        
        nums = text.split(" ")  # Разделяем строку на числа
        for num_str in nums:
            try:
                num = int(num_str)  # Конвертируем строку в число
            except ValueError:
                logger.error(f"Не удалось разобрать число: {num_str}")
                exit(1)
            write_bin(output_file, num)  # Записываем число в выходной файл
            data_num += 1

    logger.debug("Завершена обработка секции .DATA")
    return data_num
