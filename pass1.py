import helper
import sys

source_file = sys.argv[1]
destination_file = sys.argv[2]
opcode_table = helper.read_opcode_table()


def run_pass1():
    '''Simulate the PASS1 in SIC assembler'''
    # Read and Write files
    file = open(str(source_file), 'r')
    write_file = open(str(destination_file), 'w')
    # Read first line
    line = file.readline()
    # Define the needed variables
    LOCCTR = '0000'
    START_ADDRESS = ''
    SYBTAB = {}
    PRGLTH = ''
    ERROR = ''
    PRGNAME = ''
    # Start the operation
    while line != '':
        # If it is not a comment
        if line[0] != '.':
            label, opcode, operand, comment = helper.get_info_from_pass1_line(
                line)
            # The start directive
            if opcode == 'START':
                START_ADDRESS = operand
                PRGNAME = label
                LOCCTR = START_ADDRESS
                write_file.write('{} {} {} {}\n'.format(
                    helper.add_end_spaces(LOCCTR, 4),
                    helper.add_end_spaces(label, 10),
                    helper.add_end_spaces(opcode, 9),
                    helper.add_end_spaces(operand, 18)
                ))
                line = file.readline()
            # Anything not start and not end (Do Operation)
            elif opcode != 'END':
                # Write information on intermediate file
                write_file.write('{} {} {} {}\n'.format(
                    helper.add_end_spaces(LOCCTR, 4),
                    helper.add_end_spaces(label, 10),
                    helper.add_end_spaces(opcode, 9),
                    helper.add_end_spaces(operand, 18)
                ))
                # Check the label
                if label != '':
                    if (label in SYBTAB):
                        ERROR += '  Duplicate Symbol {}\n'.format(label)
                    else:
                        SYBTAB[label] = LOCCTR
                # Check the opcode
                if opcode in opcode_table:
                    LOCCTR = helper.add_to_hex(LOCCTR, 3)
                elif opcode == 'WORD':
                    LOCCTR = helper.add_to_hex(LOCCTR, 3)
                elif opcode == 'RESW':
                    LOCCTR = helper.add_to_hex(LOCCTR, 3 * int(operand))
                elif opcode == 'BYTE':
                    if operand[0] == 'C':
                        LOCCTR = helper.add_to_hex(LOCCTR, len(operand) - 3)
                    elif operand[0] == 'X':
                        LOCCTR = helper.add_to_hex(
                            LOCCTR, (len(operand) - 3) // 2)
                    else:
                        LOCCTR = helper.add_to_hex(LOCCTR, 1)
                elif opcode == 'RESB':
                    LOCCTR = helper.add_to_hex(LOCCTR, int(operand))
                else:
                    ERROR += '  Invalid Operation Code {}\n'.format(opcode)

                line = file.readline()
            else:
                # End Directive
                write_file.write('{} {} {} {}\n'.format(
                    helper.add_end_spaces(LOCCTR, 4),
                    helper.add_end_spaces(label, 10),
                    helper.add_end_spaces(opcode, 9),
                    helper.add_end_spaces(operand, 18)
                ))
                PRGLTH = helper.change_from_decimal_to_hex(helper.change_from_hex_to_decimal(
                    LOCCTR) - helper.change_from_hex_to_decimal(START_ADDRESS))
                break
        else:
            line = file.readline()
            continue
    # Print the needed information
    print('PRGNAME =', PRGNAME)
    print('PRGLTH =', PRGLTH)
    print('LOCCTR =', LOCCTR)
    print('SYBTAB:')
    print('  ', helper.add_end_spaces('SYMBOL', 10), '|',
          helper.add_end_spaces('ADDRESS', 4))
    print('   --------------------')
    for key, value in (SYBTAB.items()):
        print('  ',
              helper.add_end_spaces(key, 10), '|',
              helper.add_end_spaces(value, 4),
              )
    # Print error if it occurs
    if ERROR != '':
        print('Error(s): ')
        print(ERROR)


# run Pass1
run_pass1()
