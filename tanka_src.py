import struct
import tanka_tmpl

tmpl = open('tanka_tmpl.pyc').read()
assert tmpl[66:66 + 8] == '\x04\x00\x00\x00d\x00\x00S'

LC = 'd\x00\x00'  # LOAD_CONST 0
NOT = chr(12)  # UNARY_NOT
RET = 'S'  # RETURN_VALUE
POP = chr(1)  # POP_TOP
DUP = chr(4)  # DUP_TOP
NOP = chr(9)
POW = chr(19)  # BINARY_POWER
ADD = chr(23)  # BINARY_ADD
SUB = chr(24)  # BINARY_SUBTRACT
MUL = chr(20)  # BINARY_MULTIPLY
NEG = chr(11)  # UNARY_NEGATIVE
RT2 = chr(2)   # ROT_TWO
RT3 = chr(3)   # ROT_THREE
RT4 = chr(5)
PRINT = chr(71)  # PRINT_ITEM

tanka_body = ''.join([
        LC,
        NOT,
        DUP, # 1 1

        DUP, # 1 1 1
        DUP, # 1 1 1 1
        ADD, # 1 1 2
        DUP, # 1 1 2 2
        RT3, # 1 2 2 1
        ADD, # 1 2 3
        RT2, # 1 3 2

        DUP, # 1 3 2 2
        RT3, # 1 2 3 2
        ADD, # 1 2 5
        DUP, # 1 2 5 5
        RT3, # 1 5 2 5

        RT3, # 1 5 5 2
        DUP, # 1 5 5 2 2
        RT3, # 1 5 2 5 2
        RT3, # 1 5 2 2 5
        POW, # 1 5 2 X   (X = 32)
        DUP, # 1 5 2 X X
        DUP, # 1 5 2 X X X

        MUL, # 1 5 2 X Y   (Y = 1024)
        DUP, # 1 5 2 X Y Y
        ADD, # 1 5 2 X Z   (Z = 2048)
        SUB, # 1 5 2 -2016
        ADD, # -2014
        NEG, # 2014
        RET
])

print ' '.join('%02x' % ord(x) for x in tanka_body)


assert len(tanka_body) == 31

open('tanka.pyc', 'w').write(
    tmpl[:66] +
    struct.pack('i', len(tanka_body)) +
    tanka_body +
    tmpl[66 + 8:])

# run tanka
import tanka
print 'tanka result:', repr(tanka.tanka())
