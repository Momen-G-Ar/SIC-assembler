import helper as helper
import sys

source_file = sys.argv[1]
destination_file = sys.argv[2]


def run_pass2(PRGNAME: str, PRGLTH: str, LOCCTR: str, SYBTAB: dict, source_file=source_file, destination_file=destination_file):
    '''Simulate the PASS2 in SIC assembler'''
    # Read and Write files
    file = open(str(source_file), 'r')
    write_file = open(str(destination_file), 'w')
    write_file_listing = open(str('listing.txt'), 'w')
    opcode_table = helper.read_opcode_table()
    ERROR = ''
    symbol_value = ''
    object_code = ''
    # Read first line
    line = file.readline()
    locctr, label, opcode, operand = helper.get_info_from_pass2_line(line)
    if (opcode == 'START'):
        header = helper.generate_header_record(PRGNAME, operand, PRGLTH)
        write_file.write(header)
        helper.print_to_listing(locctr, label, opcode,
                                operand, '', write_file_listing)
        line = file.readline()

    locctr, label, opcode, operand = helper.get_info_from_pass2_line(line)
    while (opcode != 'END'):
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
