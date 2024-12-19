import logging
import sys
from computer.processor.processor import MEMORY, SHIFT

def memory_fill(bin_file):
    """Заполняет память процессора значениями из бинарного файла."""
    global MEMORY, SHIFT
    is_inst = False  # Флаг, чтобы определить, где заканчиваются данные и начинаются инструкции
    counter = 0
    counterData = 0
    for line in bin_file:
        text = line.strip()
        if counterData != -1:
            if counter == 0:
                counterData = int(line, 2)
            elif counterData != 0:
                counterData-=1
            else:
                is_inst = True
                counter = 0
                counterData = -1
        try:
            data = int(line, 2)  # Преобразуем строку в число по основанию 2
        except ValueError:
            logging.error(f"Неверное двоичное значение: {text}")
            sys.exit(1)
        logging.debug(f"Заполнение памяти: isInst={is_inst}, data={data}")

        if is_inst:
            MEMORY[counter] = data
        else:
            MEMORY[counter + SHIFT] = data
        counter += 1