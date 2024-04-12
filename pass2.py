import helper as helper
import sys

source_file = sys.argv[1]
destination_file = sys.argv[2]


def run_pass2(START_ADDRESS: str, PRGNAME: str, PRGLTH: str, LOCCTR: str, SYBTAB: dict, source_file=source_file, destination_file=destination_file):
    '''Simulate the PASS2 in SIC assembler'''
    # Read and Write files
    file = open(str(source_file), 'r')
    write_file = open(str(destination_file), 'w')
    write_file_listing = open(str('listing.lst'), 'w')
    opcode_table = helper.read_opcode_table()
    ERROR = ''
    symbol_value = ''
    object_code = ''

    # Read first line
    line = file.readline()
    while (line[0] == '.'):
        line = file.readline()
    locctr, label, opcode, operand = helper.get_info_from_pass2_line(line)
    if (opcode == 'START'):
        header = helper.generate_header_record(PRGNAME, operand, PRGLTH)
        write_file.write(header)
        helper.print_to_listing(locctr, label, opcode,
                                operand, '', write_file_listing)
        line = file.readline()

    text_record = ''  # contains the text record: max is 60 half bytes
    locctr_of_text_record = LOCCTR
    while (opcode != 'END' and line != ''):
        locctr, label, opcode, operand = helper.get_info_from_pass2_line(line)
        if (len(text_record) == 0):
            locctr_of_text_record = locctr
        if (line[0] != '.'):
            if (opcode in opcode_table):
                if (operand != ''):
                    if (operand in SYBTAB):
                        symbol_value = SYBTAB[operand]
                    else:
                        ERROR += ' undefined symbol {}\n'.format(label)
                else:
                    symbol_value = '0000'
                # check if the mode is indexed or not
                if (operand.__contains__(',')):
                    object_code = helper.add_indexed_to_hex(
                        opcode_table[opcode] + symbol_value)
                else:
                    object_code = opcode_table[opcode] + symbol_value

                #  Try to add to text record
                locctr_of_text_record, text_record = helper.add_to_text_record(
                    text_record, object_code, write_file, locctr, locctr_of_text_record)

            elif (opcode == 'BYTE' or opcode == 'WORD'):
                if (operand[0] == 'C'):  # it is BYTE with chars
                    object_code = helper.get_hex_from_chars(operand)
                    locctr_of_text_record, text_record = helper.add_to_text_record(
                        text_record, object_code, write_file, locctr, locctr_of_text_record)
                elif (operand[0] == 'X'):  # it is BYTE with Hex
                    object_code = operand[2: -1]
                    locctr_of_text_record, text_record = helper.add_to_text_record(
                        text_record, object_code, write_file, locctr, locctr_of_text_record)
                else:  # it is WORD
                    object_code = helper.change_from_decimal_to_hex(
                        int(operand))
                    object_code = ('0' * (6 - len(object_code))) + object_code
                    locctr_of_text_record, text_record = helper.add_to_text_record(
                        text_record, object_code, write_file, locctr, locctr_of_text_record)
            else:  # empty space in object code
                if (len(text_record)):
                    line_in_obj = helper.generate_text_record(
                        locctr_of_text_record, len(text_record), text_record)
                    text_record = ''
                    object_code = ''
                    write_file.write(line_in_obj)
            helper.print_to_listing(locctr, label, opcode,
                                    operand, object_code, write_file_listing)
        line = file.readline()
    end = helper.generate_end_record(operand, SYBTAB)
    write_file.write(end)
