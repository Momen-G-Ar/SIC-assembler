import pass1 as pass1
import pass2 as pass2
import sys

source_file = sys.argv[1]
intermediate_file = sys.argv[2]
object_file = sys.argv[3]

PRGNAME, PRGLTH, LOCCTR, SYBTAB, ERROR1 = pass1.run_pass1(
    source_file, intermediate_file)
if (ERROR1 == ''):
    ERROR2 = pass2.run_pass2(PRGNAME, PRGLTH, LOCCTR,
                             SYBTAB, intermediate_file, object_file)
    if (ERROR2 == ''):
        print('Done')
    else:
        print('Error in Pass2: \n', ERROR2)
else:
    print('Error in Pass1: \n', ERROR1)
