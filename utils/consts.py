# Размер данных
DATA_SIZE = 16

# Множество инструкций
INSTRUCTION_SET = {
    "HLT": 0x00,
    "PUSH": 0x01,
    "LOAD": 0x02,
    "ADD": 0x03,
    "ADC": 0x04,
    "LDC": 0x05,
    "STC": 0x06,
    "DECC": 0x07,
    "SWAP": 0x08,
    "JNZ": 0x09,
}

# Обратный словарь для инструкций
INSTRUCTION_SET_REV = {
    0x00: "HLT",
    0x01: "PUSH",
    0x02: "LOAD",
    0x03: "ADD",
    0x04: "ADC",
    0x05: "LDC",
    0x06: "STC",
    0x07: "DECC",
    0x08: "SWAP",
    0x09: "JNZ",
}
