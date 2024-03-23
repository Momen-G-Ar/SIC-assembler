map_from_char_to_number = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                           '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
map_from_number_to_char = ['0', '1', '2', '3', '4', '5', '6', '7',
                           '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']


def read_opcode_table():
    '''Read the mnemonic from file with its opcode'''
    file = open('opcode-table.txt', 'r')
    opcode_table = dict()
    x = file.readline()
    while x != '':
        mnemonic, opcode = x.split(' ')
        # store the key and value for each opcode
        opcode_table[mnemonic] = opcode.replace('\n', '')
        x = file.readline()
    return opcode_table


def get_info_from_pass1_line(line: str):
    '''Extract the src code line information'''
    label = line[0:10].strip()
    opcode = line[11:20].strip()
    operand = line[21:39].replace('\n', '').strip()
    comment = line[39:].replace('\n', '').strip()
    return label, opcode, operand, comment


def change_from_decimal_to_hex(value: int):
    hex_value = ''
    while value > 0:
        rem = int(value % 16)
        hex_value += map_from_number_to_char[rem]
        value //= 16
    if (len(hex_value) < 4):
        hex_value += ((4 - len(hex_value)) * '0')

    return hex_value[::-1]


def change_from_hex_to_decimal(hex: str):
    sum = 0
    ind = 0
    reversed_str = hex[::-1]
    for char in reversed_str:
        sum += map_from_char_to_number[char] * (16 ** ind)
        ind += 1
    return sum


def add_to_hex(hex_number: str, value: int):
    sum = change_from_hex_to_decimal(hex_number)
    sum += value
    return change_from_decimal_to_hex(sum)


def add_end_spaces(value: str, required_length: int):
    value = value.strip()
    while len(value) < required_length:
        value += ' '
    return value
