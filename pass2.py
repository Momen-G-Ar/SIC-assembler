import helper as helper


def run_pass2(PRGNAME: str, PRGLTH: str, LOCCTR: str, SYBTAB: dict, source_file, destination_file):
    '''Simulate the PASS2 in SIC assembler'''
    # Read and Write files
    file = open(str(source_file), 'r')
    write_file = open(str(destination_file), 'w')
    write_file_listing = open(str('listing.lst'), 'w')
    opcode_table = helper.read_opcode_table()

    # Define the needed variables
    ERROR = ''
    err = ''
    symbol_value = ''
    object_code = ''
    text_record = ''  # contains the text record: max is 60 half bytes
    locctr_of_text_record = LOCCTR

    # Read first line
    line = file.readline()
    while (line[0] == '.'):
        line = file.readline()
    locctr, label, opcode, operand = helper.get_info_from_pass2_line(line)
    if (opcode == 'START'):
        header = helper.generate_header_record(PRGNAME, operand, PRGLTH)
        write_file.write(header)
        helper.print_to_listing(locctr, label, opcode,
                                operand, '', '', write_file_listing)
        line = file.readline()

    while (opcode != 'END' and line != ''):
        # Read line by line from the intermediate file
        locctr, label, opcode, operand = helper.get_info_from_pass2_line(line)
        # If new text record --> save it location counter
        if (len(text_record) == 0):
            locctr_of_text_record = locctr
        # If not comment go
        if (line[0] != '.'):
            if (opcode in opcode_table):
                if (operand != ''):
                    if (operand in SYBTAB):
                        symbol_value = SYBTAB[operand]
                    elif operand[:-2] in SYBTAB:
                        symbol_value = SYBTAB[operand[:-2]]
                    else:
                        ERROR += ' undefined symbol {}\n'.format(operand)
                        err = 'undefined symbol {}\n'.format(operand)
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
                # it is BYTE with chars
                if (operand[0] == 'C'):
                    object_code = helper.get_hex_from_chars(operand)
                    locctr_of_text_record, text_record = helper.add_to_text_record(
                        text_record, object_code, write_file, locctr, locctr_of_text_record)
                # it is BYTE with Hex
                elif (operand[0] == 'X'):
                    object_code = operand[2: -1]
                    locctr_of_text_record, text_record = helper.add_to_text_record(
                        text_record, object_code, write_file, locctr, locctr_of_text_record)
                # it is WORD
                else:
                    object_code = helper.change_from_decimal_to_hex(
                        int(operand))
                    object_code = ('0' * (6 - len(object_code))) + object_code
                    locctr_of_text_record, text_record = helper.add_to_text_record(
                        text_record, object_code, write_file, locctr, locctr_of_text_record)
            # Empty space in object code
            else:
                if (len(text_record)):
                    line_in_obj = helper.generate_text_record(
                        locctr_of_text_record, len(text_record), text_record)
                    text_record = ''
                    object_code = ''
                    write_file.write(line_in_obj)
            # Print into listing file
            helper.print_to_listing(locctr, label, opcode,
                                    operand, object_code, err, write_file_listing)
            err = ''
        # Read new line
        line = file.readline()
    end = helper.generate_end_record(operand, SYBTAB)
    write_file.write(end)
    return ERROR
