HAI
WAZZUP
    I HAS A counter ITZ 0
    I HAS A sum ITZ 0
BUHBYE

BTW Test 1: Basic UPPIN loop with TIL
VISIBLE "Counting from 0 to 4:"
IM IN YR loop1 UPPIN YR counter TIL BOTH SAEM counter AN 5
    VISIBLE counter
IM OUTTA YR loop1
VISIBLE "Done!"
VISIBLE ""

BTW Test 2: NERFIN loop with WILE
counter R 5
VISIBLE "Counting down from 5 to 1:"
IM IN YR loop2 NERFIN YR counter WILE BIGGR OF counter AN 0
    VISIBLE counter
IM OUTTA YR loop2
VISIBLE "Done!"
VISIBLE ""

BTW Test 3: Loop with calculation
counter R 1
sum R 0
VISIBLE "Sum of 1 to 5:"
IM IN YR loop3 UPPIN YR counter TIL BOTH SAEM counter AN 6
    sum R SUM OF sum AN counter
IM OUTTA YR loop3
VISIBLE sum

KTHXBYE
