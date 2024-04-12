import pass1
import pass2
import sys

source_file = sys.argv[1]
intermediate_file = sys.argv[2]
object_file = sys.argv[3]

START_ADDRESS, PRGNAME, PRGLTH, LOCCTR, SYBTAB, ERROR1 = pass1.run_pass1(
    source_file, intermediate_file)
if (ERROR1 == ''):
    ERROR2 = pass2.run_pass2(START_ADDRESS, PRGNAME, PRGLTH, LOCCTR,
                             SYBTAB, intermediate_file, object_file)
    if (ERROR2 == ''):
        print('Done\n')
