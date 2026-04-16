import re

TABLE = [
    74, 151, 182, 234, 232, 27, 172, 253, 99, 177, 28, 113, 52, 81, 58, 218,
    149, 8, 181, 245, 118, 42, 122, 13, 57, 66, 86, 112, 110, 188, 229, 171,
    32, 162, 244, 47, 242, 55, 23, 16, 231, 102, 252, 174, 0, 173, 19, 166,
    129, 40, 205, 227, 249, 135, 184, 233, 85, 48, 105, 142, 100, 4, 127, 104,
    96, 200, 208, 152, 43, 106, 250, 11, 145, 203, 117, 239, 202, 150, 192, 134,
    148, 157, 201, 98, 21, 83, 108, 54, 41, 179, 72, 39, 51, 215, 79, 114, 220,
    75, 24, 126, 111, 15, 22, 95, 189, 195, 167, 9, 46, 251, 124, 223, 153, 180,
    155, 132, 30, 14, 128, 207, 68, 18, 63, 131, 190, 65, 80, 5, 224, 60, 64, 26,
    168, 70, 38, 125, 156, 59, 84, 56, 206, 212, 45, 199, 2, 71, 175, 10, 6, 209,
    61, 92, 20, 160, 194, 141, 226, 3, 82, 88, 103, 154, 1, 90, 236, 187, 191, 44,
    93, 178, 241, 138, 36, 247, 37, 101, 246, 158, 120, 243, 62, 159, 216, 7, 143,
    91, 77, 130, 76, 107, 225, 144, 94, 116, 170, 197, 140, 136, 121, 123, 214,
    255, 204, 213, 87, 193, 235, 12, 89, 146, 210, 183, 198, 211, 78, 69, 109,
    222, 163, 115, 240, 97, 164, 49, 219, 137, 73, 186, 169, 67, 221, 34, 17, 185,
    248, 29, 230, 238, 165, 139, 147, 133, 25, 196, 33, 217, 53, 176, 119, 237, 50,
    31, 228, 161, 254, 35
]

BYTECODE_SOURCE = "byte_8C020.txt"
OUTPUT_FILE = "disasm.txt"

OPNAMES = {
    0: "mov",
    1: "add",
    2: "sub",
    3: "mul",
    4: "shl",
    5: "shr",
    6: "xor",
    7: "and",
    8: "or",
    9: "push",
    10: "pop",
    11: "cmp",
    12: "jmp",
    13: "jz",
    14: "call",
    15: "ret",
}

def load_bytecode(source: str) -> list[int]:
    with open(source, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    vals = re.findall(r"0x[0-9a-fA-F]{1,2}|\b[0-9a-fA-F]{2}\b", text)
    if not vals:
        raise ValueError("No byte values found in bytecode source.")

    out = [int(v, 16) for v in vals]
    if len(out) == 0:
        raise ValueError("Parsed empty bytecode.")
    return out

def decode_code(encoded: list[int]) -> list[int]:
    return [TABLE[b] for b in encoded]

def h8(x: int) -> str:
    return f"0x{x:x}"

def label_name(addr: int) -> str:
    return f"loc_{addr:04x}"

def decode_operand_dst(mode: int, val: int) -> str:
    if (mode >> 2) != 0:
        return f"g[{h8(val)}]"
    return f"l[{h8(val)}]"

def decode_operand_src(mode: int, val: int) -> str:
    # In the VM:
    # mode == 0 -> immediate byte
    # mode == 1 -> ptr[val + 2]
    # otherwise -> v60[val]
    if mode == 0:
        return h8(val)
    if mode == 1:
        return f"l[{h8(val)}]"
    return f"g[{h8(val)}]"

def disassemble(code: list[int]) -> str:
    # First pass: collect jump/call targets for labels.
    labels = set()
    pc = 0
    while pc < len(code):
        op = code[pc]
        opcode = op >> 4
        mode = op & 0xF

        if opcode in range(0, 9) or opcode == 11:
            pc += 3
        elif opcode in (9, 10):
            pc += 2
        elif opcode in (12, 13, 14):
            if pc + 2 >= len(code):
                break
            tgt = code[pc + 1] | (code[pc + 2] << 8)
            labels.add(tgt)
            pc += 3
        elif opcode == 15:
            pc += 1
        else:
            pc += 1

    # Second pass: emit text.
    lines = []
    pc = 0
    while pc < len(code):
        if pc in labels:
            lines.append(f"{label_name(pc)}:")

        start = pc
        op = code[pc]
        opcode = op >> 4
        mode = op & 0xF
        mnem = OPNAMES.get(opcode, f"db_{opcode}")

        if opcode in range(0, 9) or opcode == 11:
            if pc + 2 >= len(code):
                lines.append(f"{start:04x}: {mnem} <truncated>")
                break
            a = code[pc + 1]
            b = code[pc + 2]
            dst = decode_operand_dst(mode, a)
            src = decode_operand_src(mode, b)
            lines.append(f"{start:04x}: {mnem} {dst}, {src}")
            pc += 3

        elif opcode == 9:  # push
            if pc + 1 >= len(code):
                lines.append(f"{start:04x}: push <truncated>")
                break
            a = code[pc + 1]
            src = decode_operand_src(mode, a)
            lines.append(f"{start:04x}: push {src}")
            pc += 2

        elif opcode == 10:  # pop
            if pc + 1 >= len(code):
                lines.append(f"{start:04x}: pop <truncated>")
                break
            a = code[pc + 1]
            dst = decode_operand_dst(mode, a)
            lines.append(f"{start:04x}: pop {dst}")
            pc += 2

        elif opcode in (12, 13, 14):
            if pc + 2 >= len(code):
                lines.append(f"{start:04x}: {mnem} <truncated>")
                break
            tgt = code[pc + 1] | (code[pc + 2] << 8)
            lines.append(f"{start:04x}: {mnem} {label_name(tgt)}")
            pc += 3

        elif opcode == 15:
            lines.append(f"{start:04x}: ret")
            pc += 1

        else:
            lines.append(f"{start:04x}: db {h8(op)}")
            pc += 1

    return "\n".join(lines)

def main():
    encoded = load_bytecode(BYTECODE_SOURCE)
    decoded = decode_code(encoded)
    asm = disassemble(decoded)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(asm)

    print(f"wrote {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
