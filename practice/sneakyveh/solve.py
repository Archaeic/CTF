#!/usr/bin/env python3

import z3
import struct

def xor_as_bytes(d):
    return ((d >> 24) & 0xFF) ^ ((d >> 16) & 0xFF) ^ ((d >> 8) & 0xFF) ^ ((d >> 0) & 0xFF)

solver = z3.Solver()
arg1 = z3.BitVec("arg1", 32)
arg2 = z3.BitVec("arg2", 32)
arg3 = z3.BitVec("arg3", 32)
arg4 = z3.BitVec("arg4", 32)

solver.add(xor_as_bytes(arg1) == 24)
solver.add(xor_as_bytes(arg2) == 10)

def add_one(a, b, expected):
    eax = z3.LShR(a, 24) & 0xFF
    ecx = z3.LShR(a, 8) & 0xFF00
    eax |= ecx
    edx = (a << 16) & 0xFFFF0000
    eax |= edx
    eax ^= b
    solver.add(eax == expected)

# case 0
add_one(arg1, arg2, 0x252D0D17)

# case 1
add_one(arg2, arg1, 0x253F1D15)

# case 2
add_one(arg3, arg4, 0xBEA57768)

# case 3
add_one(arg4, arg3, 0xBAA5756E)

expected = b"ACSC2024"

solver.add(expected[0] ^ (arg2 & 0xFF) == 0x99)
solver.add(expected[4] ^ (arg4 & 0xFF) == 0x4F)

solver.add((arg1 ^ arg2) == struct.unpack("<I", expected[0:4])[0])
solver.add((arg3 ^ arg4) == struct.unpack("<I", expected[4:8])[0])

if solver.check() == z3.sat:
    m = solver.model()
    print(
        m[arg1].as_long(),
        m[arg2].as_long(),
        m[arg3].as_long(),
        m[arg4].as_long()
    )
else:
    raise Exception("Not found!")
