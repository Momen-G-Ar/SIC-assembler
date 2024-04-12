from io import TextIOWrapper


# <---------- Common Helpers ---------->
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


def add_end_spaces(value: str, required_length: int):
    value = value.strip()
    while len(value) < required_length:
        value += ' '
    return value


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


def add_end_spaces(value: str, required_length: int = 0):
    value = value.strip()
    while len(value) < required_length:
        value += ' '
    return value


# <---------- Pass #1 Helpers ---------->
def get_info_from_pass1_line(line: str):
    '''Extract the src code line information'''
    label = line[0:10].strip()
    opcode = line[11:20].strip()
    operand = line[21:39].replace('\n', '').strip()
    comment = line[39:].replace('\n', '').strip()
    return label, opcode, operand, comment


def print_to_intermediate(LOCCTR: str, label: str, opcode: str, operand: str, write_file: TextIOWrapper):
    write_file.write('{} {} {} {}\n'.format(
        add_end_spaces(LOCCTR, 4),
        add_end_spaces(label, 10),
        add_end_spaces(opcode, 9),
        add_end_spaces(operand, 18)
    ))


# <---------- Pass #2 Helpers ---------->
def get_info_from_pass2_line(line: str):
    '''Extract the src code line information'''
    locctr = line[0:5].strip()
    label = line[5:16].strip()
    opcode = line[16:26].strip()
    operand = line[26:44].replace('\n', '').strip()
    return locctr, label, opcode, operand


def add_indexed_to_hex(hex: str):
    '''Make the (X) bit to 1 ==> Indexed'''
    # (1000 << 12) --> (1000 0000 0000 0000) --> (add them to the hex number) --> fourth half byte become 1XXX
    return add_to_hex(hex, (8 << 12))


def generate_header_record(PRGNAME: str, START_ADDRESS: str, PRGLTH: str):
    start = START_ADDRESS
    length = PRGLTH
    while len(start) < 6:
        start = '0' + start
    while len(length) < 6:
        length = '0' + length
    return 'H^' + add_end_spaces(PRGNAME[0:7], 6) \
        + '^' + add_end_spaces(start, 6) \
        + '^' + add_end_spaces(length, 6) + '\n'


def generate_text_record(locctr: str, length: int, object_code: str):
    length_in_hex = change_from_decimal_to_hex(length / 2)
    while len(locctr) < 6:
        locctr = '0' + locctr
    return 'T^' + locctr + '^' + length_in_hex[2:4] + '^' + object_code + '\n'


def add_to_text_record(text_record: str, object_code: str, write_file: TextIOWrapper, locctr: str, locctr_of_text_record: str):
    if (len(text_record) + len(object_code) <= 60):
        text_record += object_code
    else:
        line_in_obj = generate_text_record(
            locctr_of_text_record, len(text_record), text_record)
        write_file.write(line_in_obj)
        text_record = object_code
        locctr_of_text_record = locctr
    return locctr_of_text_record, text_record


def generate_end_record(operand, SYBTAB):
    if (operand in SYBTAB):
        START_ADDRESS = SYBTAB[operand]
    else:
        START_ADDRESS = ''
    if (START_ADDRESS != ''):
        while len(START_ADDRESS) < 6:
            START_ADDRESS = '0' + START_ADDRESS
        return 'E^' + START_ADDRESS
    else:
        return 'E'


def print_to_listing(LOCCTR: str = '', label: str = '', opcode: str = '', operand: str = '', object_code: str = '', error: str = '', write_file: TextIOWrapper = ''):
    line = '{} {} {} {} {}'.format(
        add_end_spaces(LOCCTR, 4),
        add_end_spaces(label, 10),
        add_end_spaces(opcode, 9),
        add_end_spaces(operand, 18),
        add_end_spaces(object_code, 6),
    )
    if (error != ''):
        line += ' Error: ' + error + '\n'
    else:
        line += '\n'
    write_file.write(line)


def get_hex_from_chars(chars: str):
    hex = ''
    chars = chars[2: -1]
    for char in chars:
        ascii = format(ord(char), "x").upper()
        hex += ascii
    return hex
