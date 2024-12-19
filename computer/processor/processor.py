import logging
import sys

from utils.consts import DATA_SIZE
from utils.consts import INSTRUCTION_SET_REV

# Глобальные переменные для состояния процессора
PC = 0  # Счётчик команд (Program Counter)
CX = 0  # Регистр CX
CARRYFLAG = False  # Флаги
MEMORY = [0] * 100  # Память
SHIFT = 50  # Шифт, если потребуется

# Константы
MAX_DATA_VAL = (1 << DATA_SIZE) - 1  # Максимальное значение данных


def init_processor():
    """Инициализация процессора"""
    global PC, CX, CARRYFLAG, MEMORY, SHIFT
    PC = 0
    CX = 0
    CARRYFLAG = False
    SHIFT = SHIFT


def start_processor():
    """Основной цикл выполнения процессора"""
    global PC, CX, CARRYFLAG, MEMORY  # Обеспечим, чтобы память не перезаписывалась
    stack = []
    while True:
        logging.info(repr_processor(stack, True))
        data = MEMORY[PC]
        inst = INSTRUCTION_SET_REV.get(data, None)
        if inst is None:
            logging.error(f"Неизвестная инструкция в PC {PC}")
            sys.exit(1)

        if inst == "HLT":
            result = 0
            for i, value in enumerate(reversed(stack)):
                result |= value << (16 * i)
            logging.critical(f"Ответ: {result}")
            return
        elif inst == "PUSH":
            PC += 1
            logging.info(repr_processor(stack, False))
            data = MEMORY[PC]
            stack.append(data)
        elif inst == "LOAD":
            t1 = stack.pop()
            stack.append(MEMORY[t1])
        elif inst == "ADD":
            t1 = stack.pop()
            t2 = stack.pop()
            tsum = (t1 + t2) & 0xFFFF
            stack.append(tsum)
            CARRYFLAG = t1 + t2 > MAX_DATA_VAL
        elif inst == "ADC":
            t1 = stack.pop()
            t2 = stack.pop()
            tsum = t1 + t2 + CARRYFLAG
            stack.append(tsum)
            if tsum > MAX_DATA_VAL:
                logging.error("ADC: Переполнение")
                sys.exit(1)
        elif inst == "LDC":
            CX = stack.pop()
        elif inst == "STC":
            stack.append(CX)
        elif inst == "DECC":
            CX -= 1
        elif inst == "SWAP":
            t1 = stack.pop()
            t2 = stack.pop()
            stack.append(t1)
            stack.append(t2)
        elif inst == "JNZ":
            t1 = stack.pop()
            logging.debug("------")
            if CX != 0:
                PC = t1
                continue
        else:
            logging.error(f"Неизвестная инструкция: {inst}")
            sys.exit(1)
        PC += 1


def bool2int(b):
    return 1 if b else 0


def repr_processor(stack, is_inst=False):
    """Возвращает строковое представление состояния процессора"""
    global PC, CX, CARRYFLAG

    # Декодируем память в PC
    decoded_pc_mem = str(MEMORY[PC])
    if is_inst:
        inst = INSTRUCTION_SET_REV.get(MEMORY[PC], "???")
        decoded_pc_mem = inst

    # Итоговая строка
    return f"{decoded_pc_mem} Стек: [{', '.join(f'0x{item:x}({item})' for item in stack)}] CARRYFLAG: {bool2int(CARRYFLAG)} / Исполняемая команда: {PC} / Счётчик обратного отсчёта: {CX}"
