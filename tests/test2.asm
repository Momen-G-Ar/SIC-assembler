.......... ......... ..................
.       MAIN SUBROUTINE
.......... ......... ..................
OPERAT     START     1000 
           LDA       ALPHA
           ADD       INCR
           SUB       ONE
           STA       BETA
           LDA       GAMMA
           ADD       INCR
           SUB       ONE
           STA       DELTA
ONE        WORD      1
.
ALPHA      RESW       1
BETA       RESW       1
GAMMA      RESW       1
DELTA      RESW       1
INCR       RESW       1
           END       FIRST