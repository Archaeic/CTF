# Sneaky_VEH
Main:
```cpp
int __cdecl main(int argc, const char **argv, const char **envp)
{
  const WCHAR *CommandLineW; // eax
  unsigned int v5; // [esp+10h] [ebp-38h]
  LPWSTR *hMem; // [esp+18h] [ebp-30h]
  char v7[4]; // [esp+1Ch] [ebp-2Ch]
  wchar_t *EndPtr; // [esp+20h] [ebp-28h] BYREF
  int pNumArgs; // [esp+28h] [ebp-20h] BYREF
  CPPEH_RECORD ms_exc; // [esp+30h] [ebp-18h]

  sub_4B1040(Format);
  CommandLineW = GetCommandLineW();
  hMem = CommandLineToArgvW(CommandLineW, &pNumArgs);
  if ( hMem )
  {
    if ( pNumArgs == 5 )
    {
      *(_DWORD *)v7 = 0;
      while ( *(int *)v7 < pNumArgs - 1 )
      {
        v5 = wcstoul(hMem[*(_DWORD *)v7 + 1], &EndPtr, 16);
        sub_4B1040("KEY%d: %lx\n", *(_DWORD *)v7, v5);
        dword_4B7470[(*(_DWORD *)v7)++] = v5;
      }
      LocalFree(hMem);
      ms_exc.registration.TryLevel = 0;
      lpAddress = VirtualAlloc(0, 0x1000u, 0x3000u, 0x102u);
      if ( !lpAddress )
      {
        sub_4B1040(aVirtualallocFa);
        exit(-1);
      }
      memset(lpAddress, 0, 0x1000u);
      ms_exc.registration.TryLevel = -2;
      sub_4B1040(aSeeYa);
      return 0;
    }
    else
    {
      sub_4B1040(aTooFewArgument);
      return -1;
    }
  }
  else
  {
    sub_4B1040(aCommandlinetoa);
    return -1;
  }
}
```

There's nothing inside the main, but if we take a look at ASM here. We can actually see that there are some code blocks that aren't visible in the disassembly view.

![{83B1DF06-4BDE-46C2-A969-E154F0DF38E3}](https://hackmd.io/_uploads/ryQoMFL3We.png)


So the execution path jumps to exception handler at `0x401EAE` instead of continuing the flow.
- sub_431B50

```cpp
int __stdcall sub_431B50(int **a1)
{
  int v2; // [esp+4h] [ebp-2Ch]
  unsigned int v3; // [esp+Ch] [ebp-24h]
  int v4; // [esp+14h] [ebp-1Ch]
  unsigned int i; // [esp+18h] [ebp-18h]
  int v6; // [esp+20h] [ebp-10h]
  char v7; // [esp+27h] [ebp-9h]

  v6 = **a1;
  v2 = a1[1][46];
  if ( v6 != 0x80000001 && v6 != 0x80000003 && v6 != 0xC000001D )
    return 1;
  if ( !dword_43746C && v6 == 0x80000001
    || dword_43746C == 1 && v6 == 0x80000003
    || dword_43746C == 2 && v6 == 0x80000003
    || dword_43746C == 3 && v6 == 0xC000001D )
  {
    v4 = (int)*(&off_434020 + dword_43746C);
    v7 = HIBYTE(dword_437470[dword_43746C])
       ^ HIWORD(dword_437470[dword_43746C])
       ^ BYTE1(dword_437470[dword_43746C])
       ^ dword_437470[dword_43746C];
    v3 = dword_434128[dword_43746C];
    for ( i = 0; i < v3; ++i )
      *(_BYTE *)(i + v4) ^= v7;
    if ( dword_43746C > 0 && dword_43746C < 4 )
      memmove(
        (void *)(v2 & 4294967280),
        (const void *)(dword_434104[dword_43746C] + (v2 & 4294967280)),
        dword_434124[dword_43746C] - dword_434104[dword_43746C]);
  }
  ++dword_43746C;
  return 1;
}
```

The programme XOR 4 times with 4 exceptions

- `0x80000001` = STATUS_GUARD_PAGE_VIOLATION
- `0x80000003` = STATUS_BREAKPOINT
- `0x80000003` = STATUS_BREAKPOINT
- `0xC000001D` = STATUS_ILLEGAL_INSTRUCTION

Next, inside `sub_4015D0` we have `sub_4313B0`, which is a checker

```cpp
void *__stdcall sub_4313B0(int **a1)
{
  int v2; // [esp+8h] [ebp-30h]
  int v3; // [esp+Ch] [ebp-2Ch]
  _BYTE *v4; // [esp+1Ch] [ebp-1Ch]
  int v5; // [esp+20h] [ebp-18h]
  int j; // [esp+24h] [ebp-14h]
  unsigned int v7; // [esp+28h] [ebp-10h]
  int i; // [esp+2Ch] [ebp-Ch]
  int v9; // [esp+30h] [ebp-8h] BYREF

  v2 = **a1;
  v3 = 0;
  v7 = 0;
  v5 = 0;
  v9 = 0;
  for ( i = 0; i < 4; ++i )
  {
    v9 = dword_434138[i];
    v4 = lpAddress;
    if ( v2 == dword_434118[i] && !dword_437458[i] )
    {
      for ( j = 0; j < 4; ++j )
        v4[j] ^= *((_BYTE *)&v9 + j);
      switch ( i )
      {
        case 0:
          v7 = dword_437470[0];
          v5 = *(_DWORD *)algn_437474;
          break;
        case 1:
          v7 = *(_DWORD *)algn_437474;
          v5 = dword_437470[0];
          break;
        case 2:
          v7 = *(_DWORD *)&algn_437474[4];
          v5 = *(_DWORD *)&algn_437474[8];
          break;
        case 3:
          v7 = *(_DWORD *)&algn_437474[8];
          v5 = *(_DWORD *)&algn_437474[4];
          break;
        default:
          break;
      }
      if ( (v5 ^ ((v7 << 16) | (v7 >> 8) & 0xFF00 | HIBYTE(v7))) == dword_4340F8[i] )
      {
        dword_437458[i] = 1;
        return lpAddress;
      }
      return (void *)v3;
    }
  }
  return (void *)v3;
}
```

It's checking if the opcode matches with 4 exception cases then XOR 4 bytes

```cpp
 if ( (v5 ^ ((v7 << 16) | (v7 >> 8) & 0xFF00 | HIBYTE(v7))) == dword_4340F8[i] )
```

Here the programme is rearranging bytes so we'll check what `dword_4340F8` actually is.

![{CF20674D-D084-4BC0-9CE2-1DC886D0A231}](https://hackmd.io/_uploads/S18G-J4nZg.png)
 
So we have:

```
case 0: (arg2 ^ rotate(arg1)) == 0x252D0D17
case 1: (arg1 ^ rotate(arg2)) == 0x253F1D15
case 2: (arg4 ^ rotate(arg3)) == 0x0BEA57768
case 3: (arg3 ^ rotate(arg4)) == 0x0BAA5756E
```

Back to `sub_4015D0` I found `off_404160` is some typa array of 210 structs, each struct is 56 bytes.

![image](https://hackmd.io/_uploads/H1ZC_OS2-g.png)

VEH registered this array when exception occurs. So, IF exception keeps on occuring, every function in this array will be called.

While tracing, I found `sub_4012A0` have the same `algn_437474` as `sub_4313B0` and it's XOR with something so that must be our last checker.

- sub_4012A0

```cpp
int __stdcall sub_4012A0(_BYTE *a1)
{
  int v2; // [esp+0h] [ebp-18h]
  int v3; // [esp+4h] [ebp-14h]
  int v4; // [esp+8h] [ebp-10h]
  int v5; // [esp+Ch] [ebp-Ch]

  if ( (unsigned __int8)(*a1 ^ algn_407474[0]) == 0x99 )
    v5 = 0;
  else
    v5 = 16;
  if ( (unsigned __int8)(a1[4] ^ algn_407474[8]) == 0x4F )
    v4 = 0;
  else
    v4 = 16;
  if ( (*(_DWORD *)algn_407474 ^ dword_407470[0]) == *(_DWORD *)a1 )
    v3 = 0;
  else
    v3 = 16;
  if ( (*(_DWORD *)&algn_407474[8] ^ *(_DWORD *)&algn_407474[4]) == *((_DWORD *)a1 + 1) )
    v2 = 0;
  else
    v2 = 16;
  return v2 | v3 | v4 | v5;
}
```
Now I'm just missing `dword_407470` and `algn_407474`

So I tried to continue tracing till the programme reaches `sub_4012A0`, but thats 210 structs and I kept getting `EXCEPTION_SINGLE_STEP`, so after a long exception-breaking session I found a string `ACSC2024` at `sub_4012A0`.

We're using z3 to solve 
```py
import pwn
import z3

def xor_as_bytes(d):
    return ((d >> 24) & 0xFF) ^ ((d >> 16) & 0xFF) ^ ((d >> 8) & 0xFF) ^ ((d >> 0) & 0xFF)

solver = z3.Solver()
arg1 = z3.BitVec("arg1", 8 * 4)
arg2 = z3.BitVec("arg2", 8 * 4)
arg3 = z3.BitVec("arg3", 8 * 4)
arg4 = z3.BitVec("arg4", 8 * 4)

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

# case 0:
a = arg1
b = arg2
expected = 0x252D0D17
add_one(a, b, expected)

# case 1
a = arg2
b = arg1
expected = 0x253F1D15
add_one(a, b, expected)

# case 2
a = arg3
b = arg4
expected = 0x0BEA57768
add_one(a, b, expected)

# case 3
a = arg4
b = arg3
expected = 0x0BAA5756E
add_one(a, b, expected)

# 004012A0
expected = b"ACSC2024"
solver.add(expected[0] ^ (arg2 & 0xFF) == 0x99)
solver.add(expected[4] ^ (arg4 & 0xFF) == 0x4F)
solver.add((arg1 ^ arg2) == pwn.unpack(expected[0:4]))
solver.add((arg3 ^ arg4) == pwn.unpack(expected[4:8]))

if solver.check() == z3.sat:
    model = solver.model()
    print(
    f'0x{model[arg1].as_long():08X}',
    f'0x{model[arg2].as_long():08X}',
    f'0x{model[arg3].as_long():08X}',
    f'0x{model[arg4].as_long():08X}'
)
else:
    raise Exception("Not found!")
```

![image](https://hackmd.io/_uploads/Hyrdr7Ih-g.png)

![{F66B8B69-66E6-4CE1-BE6A-BE03D77431DD}](https://hackmd.io/_uploads/ry0YrXI3Zg.png)

# Magic
Main:
```cpp
__int64 __fastcall main(int a1, char **a2, char **a3)
  v26 = __readfsqword(0x28u);
  srand(0x1337u);
  v17 = 0;
  v18 = 0;
  v19 = 0;
  v20 = 0;
  v21 = 0;
  v22 = 0;
  v23 = 0;
  v24 = 0;
  v25 = 0;
  printf("flag: ");
  __isoc99_scanf("%64s", s);
  v17 = *(_QWORD *)s;
  v18 = v9;
  v19 = v10;
  v20 = v11;
  v21 = v12;
  v22 = v13;
  v23 = v14;
  v24 = v15;
  v25 = v16;
  if ( strlen(s) != 64 )
    goto LABEL_2;
  v4 = 1;
  for ( i = 0; i <= 63; ++i )
  {
    if ( s[i] > 47 && s[i] <= 57 )
    {
      s[i] -= 48;
    }
    else
    {
      if ( s[i] > 102 || s[i] <= 96 )
      {
        v4 = 0;
        break;
      }
      s[i] -= 87;
    }
  }
  if ( v4 != 1 )
  {
LABEL_2:
    puts("Wrong");
    return 0;
  }
  else
  {
    for ( j = 0; j <= 31; ++j )
      v7[j] = s[2 * j + 1] | (16 * s[2 * j]);
    if ( (unsigned __int8)sub_7A96D(v7) )
      printf("Correct! Flag is DH{%s}\n", (const char *)&v17);
    else
      puts("Wrong");
    return 0;
  }
}
```
Now let's see `sub_7A96D`

```cpp
__int64 __fastcall sub_7A96D(const void *a1)
{
  dest[33] = __readfsqword(0x28u);
  v45 = 0;
  memset(v60, 0, sizeof(v60));
  v17 = 0;
  memset(dest, 0, 256);
  v47 = 32;
  memcpy(dest, a1, 0x20u);
  ptr = (_BYTE *)sub_7A87C(0, 0);
  while ( 2 )
  {
    v1 = v45;
    v46 = v45 + 1;
    v41 = sub_7A8DA(a1, byte_8C020[v1]);
    switch ( v41 >> 4 )
    {
      case 0:
        v18 = sub_7A8DA(a1, byte_8C020[v46]);
        v2 = v46 + 1;
        v45 = v46 + 2;
        v30 = sub_7A8DA(a1, byte_8C020[v2]);
        if ( (unsigned __int8)(v41 & 0xF) >> 2 )
          v49 = (unsigned __int8 *)v60 + v18;
        else
          v49 = &ptr[v18 + 2];
        if ( (v41 & 3) != 0 )
        {
          if ( (v41 & 3) == 1 )
            v30 = ptr[v30 + 2];
          else
            v30 = *((_BYTE *)v60 + v30);
        }
        *v49 = v30;
        continue;
      case 1:
        v19 = sub_7A8DA(a1, byte_8C020[v46]);
        v3 = v46 + 1;
        v45 = v46 + 2;
        v31 = sub_7A8DA(a1, byte_8C020[v3]);
        if ( (unsigned __int8)(v41 & 0xF) >> 2 )
          v50 = (char *)v60 + v19;
        else
          v50 = &ptr[v19 + 2];
        if ( (v41 & 3) != 0 )
        {
          if ( (v41 & 3) == 1 )
            v31 = ptr[v31 + 2];
          else
            v31 = *((_BYTE *)v60 + v31);
        }
        *v50 += v31;
        continue;
      case 2:
        v20 = sub_7A8DA(a1, byte_8C020[v46]);
        v4 = v46 + 1;
        v45 = v46 + 2;
        v32 = sub_7A8DA(a1, byte_8C020[v4]);
        if ( (unsigned __int8)(v41 & 0xF) >> 2 )
          v51 = (char *)v60 + v20;
        else
          v51 = &ptr[v20 + 2];
        if ( (v41 & 3) != 0 )
        {
          if ( (v41 & 3) == 1 )
            v32 = ptr[v32 + 2];
          else
            v32 = *((_BYTE *)v60 + v32);
        }
        *v51 -= v32;
        continue;
      case 3:
        v21 = sub_7A8DA(a1, byte_8C020[v46]);
        v5 = v46 + 1;
        v45 = v46 + 2;
        v33 = sub_7A8DA(a1, byte_8C020[v5]);
        if ( (unsigned __int8)(v41 & 0xF) >> 2 )
          v52 = (char *)v60 + v21;
        else
          v52 = &ptr[v21 + 2];
        if ( (v41 & 3) != 0 )
        {
          if ( (v41 & 3) == 1 )
            v33 = ptr[v33 + 2];
          else
            v33 = *((_BYTE *)v60 + v33);
        }
        *v52 *= v33;
        continue;
      case 4:
        v22 = sub_7A8DA(a1, byte_8C020[v46]);
        v6 = v46 + 1;
        v45 = v46 + 2;
        v34 = sub_7A8DA(a1, byte_8C020[v6]);
        if ( (unsigned __int8)(v41 & 0xF) >> 2 )
          v53 = (char *)v60 + v22;
        else
          v53 = &ptr[v22 + 2];
        if ( (v41 & 3) != 0 )
        {
          if ( (v41 & 3) == 1 )
            v34 = ptr[v34 + 2];
          else
            v34 = *((_BYTE *)v60 + v34);
        }
        *v53 = (unsigned __int8)*v53 << v34;
        continue;
      case 5:
        v23 = sub_7A8DA(a1, byte_8C020[v46]);
        v7 = v46 + 1;
        v45 = v46 + 2;
        v35 = sub_7A8DA(a1, byte_8C020[v7]);
        if ( (unsigned __int8)(v41 & 0xF) >> 2 )
          v54 = (char *)v60 + v23;
        else
          v54 = &ptr[v23 + 2];
        if ( (v41 & 3) != 0 )
        {
          if ( (v41 & 3) == 1 )
            v35 = ptr[v35 + 2];
          else
            v35 = *((_BYTE *)v60 + v35);
        }
        *v54 = (int)(unsigned __int8)*v54 >> v35;
        continue;
      case 6:
        v24 = sub_7A8DA(a1, byte_8C020[v46]);
        v8 = v46 + 1;
        v45 = v46 + 2;
        v36 = sub_7A8DA(a1, byte_8C020[v8]);
        if ( (unsigned __int8)(v41 & 0xF) >> 2 )
          v55 = (char *)v60 + v24;
        else
          v55 = &ptr[v24 + 2];
        if ( (v41 & 3) != 0 )
        {
          if ( (v41 & 3) == 1 )
            v36 = ptr[v36 + 2];
          else
            v36 = *((_BYTE *)v60 + v36);
        }
        *v55 ^= v36;
        continue;
      case 7:
        v25 = sub_7A8DA(a1, byte_8C020[v46]);
        v9 = v46 + 1;
        v45 = v46 + 2;
        v37 = sub_7A8DA(a1, byte_8C020[v9]);
        if ( (unsigned __int8)(v41 & 0xF) >> 2 )
          v56 = (char *)v60 + v25;
        else
          v56 = &ptr[v25 + 2];
        if ( (v41 & 3) != 0 )
        {
          if ( (v41 & 3) == 1 )
            v37 = ptr[v37 + 2];
          else
            v37 = *((_BYTE *)v60 + v37);
        }
        *v56 &= v37;
        continue;
      case 8:
        v26 = sub_7A8DA(a1, byte_8C020[v46]);
        v10 = v46 + 1;
        v45 = v46 + 2;
        v38 = sub_7A8DA(a1, byte_8C020[v10]);
        if ( (unsigned __int8)(v41 & 0xF) >> 2 )
          v57 = (char *)v60 + v26;
        else
          v57 = &ptr[v26 + 2];
        if ( (v41 & 3) != 0 )
        {
          if ( (v41 & 3) == 1 )
            v38 = ptr[v38 + 2];
          else
            v38 = *((_BYTE *)v60 + v38);
        }
        *v57 |= v38;
        continue;
      case 9:
        if ( (unsigned __int16)v47 > 0xFFu )
        {
          fwrite("[+] VM ERR: Stack Overflow\n", 1u, 0x1Bu, stderr);
          exit(1);
        }
        v11 = v46;
        v45 = v46 + 1;
        v39 = sub_7A8DA(a1, byte_8C020[v11]);
        if ( (v41 & 0xF) != 0 )
        {
          if ( (v41 & 0xF) == 1 )
            v39 = ptr[v39 + 2];
          else
            v39 = *((_BYTE *)v60 + v39);
        }
        v12 = v47++;
        *((_BYTE *)dest + v12) = v39;
        continue;
      case 10:
        if ( !v47 )
        {
          fwrite("[+] VM ERR: Stack Underflow\n", 1u, 0x1Cu, stderr);
          exit(1);
        }
        v13 = v46;
        v45 = v46 + 1;
        v27 = sub_7A8DA(a1, byte_8C020[v13]);
        if ( (v41 & 0xF) != 0 )
          v58 = (char *)v60 + v27;
        else
          v58 = &ptr[v27 + 2];
        *v58 = *((_BYTE *)dest + (unsigned __int16)--v47);
        continue;
      case 11:
        v28 = sub_7A8DA(a1, byte_8C020[v46]);
        v14 = v46 + 1;
        v45 = v46 + 2;
        v40 = sub_7A8DA(a1, byte_8C020[v14]);
        if ( (unsigned __int8)(v41 & 0xF) >> 2 )
          v29 = *((_BYTE *)v60 + v28);
        else
          v29 = ptr[v28 + 2];
        if ( (v41 & 3) != 0 )
        {
          if ( (v41 & 3) == 1 )
            v40 = ptr[v40 + 2];
          else
            v40 = *((_BYTE *)v60 + v40);
        }
        v17 = v29 == (char)v40;
        continue;
      case 12:
        LOBYTE(v42) = sub_7A8DA(a1, byte_8C020[v46]);
        HIBYTE(v42) = sub_7A8DA(a1, byte_8C020[(unsigned __int16)(v46 + 1)]);
        v45 = v42;
        continue;
      case 13:
        LOBYTE(v43) = sub_7A8DA(a1, byte_8C020[v46]);
        v15 = v46 + 1;
        v45 = v46 + 2;
        HIBYTE(v43) = sub_7A8DA(a1, byte_8C020[v15]);
        if ( v17 )
          v45 = v43;
        continue;
      case 14:
        LOBYTE(v44) = sub_7A8DA(a1, byte_8C020[v46]);
        HIBYTE(v44) = sub_7A8DA(a1, byte_8C020[(unsigned __int16)(v46 + 1)]);
        ptr = (_BYTE *)sub_7A87C(ptr, (unsigned __int16)(v46 + 2));
        v45 = v44;
        continue;
      case 15:
        v45 = *(_WORD *)ptr;
        v59 = (_BYTE *)*((_QWORD *)ptr + 33);
        free(ptr);
        if ( v59 )
        {
          ptr = v59;
          continue;
        }
        return LOBYTE(v60[0]);
      default:
        fwrite("[+] VM ERR: Undefined Opcode\n", 1u, 0x1Du, stderr);
        exit(1);
    }
  }
}
```
This function does a lot of switch cases and seems like it operates like a VM, there are 16 OPcode for 16 switch cases
```
OP_MOV = 0
OP_ADD = 1
OP_SUB = 2
OP_MUL = 3
OP_SHL = 4
OP_SHR = 5
OP_XOR = 6
OP_AND = 7
OP_OR = 8
OP_PUSH = 9
OP_POP = 10
OP_CMP = 11
OP_JMP = 12
OP_JZ = 13
OP_CALL = 14
OP_RET = 15

```
Let's see `sub_7A8DA`
```cpp
__int64 __fastcall sub_7A8DA(__int64 a1, unsigned __int8 a2)
{
  int v3; // [rsp+1Ch] [rbp-4h]

  v3 = rand();
  return ((__int64 (__fastcall *)(_QWORD, _QWORD, _QWORD))funcs_7A968[a2])(
           *(unsigned __int8 *)((v3 & 0x1F) + a1),
           *(unsigned __int8 *)(((v3 >> 5) & 0x1F) + a1),
           *(unsigned __int8 *)(((v3 >> 10) & 0x1F) + a1));
}
```

`funcs_7A968` calls a bunch of function that looks like this
```cpp
__int64 __fastcall sub_79956(unsigned __int8 a1, unsigned __int8 a2, unsigned __int8 a3)
{
  int v3; // ebx
  int v4; // r12d
  int v5; // r12d
  int v6; // ebx
  int v7; // r12d
  unsigned int v8; // ebx
  __int64 v9; // rax
  int v10; // r12d
  unsigned int v11; // ebx
  int v12; // r12d
  int v13; // ebx

  v3 = sub_5EB48(a1, a2, a3);
  v4 = (~a3 & a2) * sub_5E805(a1, a2, a3);
  v5 = v3 + v4 + (unsigned __int8)(a1 | a2) * (unsigned int)sub_59C5F(a1, a2, a3);
  v6 = ~(unsigned __int8)(a2 ^ a1) * sub_522F6(a1, a2, a3);
  v7 = v6 + (~a1 & a2) * sub_522F6(a1, a2, a3) + v5;
  v8 = (unsigned __int8)(a2 & a3) * (unsigned int)sub_49ABF(a1, a2, a3);
  v9 = sub_55E06(a1, a2, a3);
  LOWORD(v9) = a3 * (unsigned __int8)v9;
  v10 = v8 + v9 + v7;
  v11 = (unsigned __int8)(a2 ^ a3) * (unsigned int)sub_57264(a1, a2, a3);
  v12 = v11 + ~a2 * sub_5EE97(a1, a2, a3) + v10;
  v13 = ~(unsigned __int8)(a2 & a3) * sub_4CECB(a1, a2, a3);
  return v12 + v13 + ~(unsigned __int8)(a2 | a1) * (unsigned int)sub_5E64A(a1, a2, a3);
}
```
Lastly, `byte_8C020` is VM commands

Basically the programme is doing these:

1. Receive a 64 char hex string from the user and convert it into 32 bytes of data.
2. Place those 32 bytes, corresponding to the input, onto the VM stack.
3. Execute VM instructions according to the data in `byte_8C020` and the input.
4. When the VM terminates, if the first value of the VM’s global variable is non-zero, the flag is obtained.

Now, using python with GDB we can actually extract the `byte_8C020` table 
```py
# gdb -q -batch -x script.py ./main
import gdb

ge = gdb.execute
gp = gdb.parse_and_eval

class set_parm(gdb.Breakpoint):
    def __init__(self, bp_addr):
        super(set_parm, self).__init__(spec=f"*{bp_addr}")
        self.count = 0

    def stop(self):

        new_rsi = self.count
        ge(f"set $rsi = {new_rsi}")
        self.count += 1

        return False

class hook_retval(gdb.Breakpoint):
    def __init__(self, bp_addr):
        super(hook_retval, self).__init__(spec=f"*{bp_addr}")
        self.retval = []

    def stop(self):
        retval = int(gp("$rax")) & 0xFF
        self.retval.append(retval)
        return True

IMAGE_BASE = 0x555555554000
set_parm(IMAGE_BASE + 0x7ACAD)
hooker = hook_retval(IMAGE_BASE + 0x7ACB2)

INPUT_DUMMY = "0"*64
for i in range(0x100):
    ge("run <<<" + INPUT_DUMMY, to_string=True)

with open("table.txt", "w") as f:
    f.write("table = " + str(hooker.retval))

```

We then can take the extracted table and byte_8C020 to get the assembly.
```py
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
```
```
0000:  CALL 01c4
0003:  CMP r0, #145
0006:  JE 000c
0009:  JMP 0129
...
011A:  CMP r31, #239
011D:  JE 0123
0120:  JMP 0129
0123:  MOV r0, #1
0126:  JMP 012c
0129:  MOV r0, #0
...
0186:  MOV r31, #0
0189:  RET

018A:  POP [1]
018C:  POP [0]
018E:  MOV [2], #8
0191:  SUB [2], [1]
0194:  MOV [3], [0]
0197:  SHL [3], [1]
019A:  MOV [4], [0]
019D:  SHR [4], [2]
01A0:  OR [3], [4]
01A3:  PUSH [3]
01A5:  RET

01A6:  POP [3]
01A8:  POP [2]
01AA:  POP [1]
01AC:  MOV [0], [1]
01AF:  ADD [0], [2]
01B2:  XOR [0], [3]
01B5:  PUSH [0]
01B7:  PUSH #4
01B9:  CALL 018a
01BC:  POP [0]
01BE:  ADD [0], #55
01C1:  PUSH [0]
01C3:  RET

01C4:  MOV [0], #0
01C7:  CMP [0], #32
01CA:  JE 0221
01CD:  MOV [1], [0]
01D0:  AND [1], #16
01D3:  CMP [1], #0
01D6:  JE 01f3
01D9:  MOV [1], [0]
01DC:  AND [1], #8
01DF:  CMP [1], #0
01E2:  JE 01ec
01E5:  PUSH #241
01E7:  PUSH #141
01E9:  JMP 020d
01EC:  PUSH #154
01EE:  PUSH #202
01F0:  JMP 020d
01F3:  MOV [1], [0]
01F6:  AND [1], #8
01F9:  CMP [1], #0
01FC:  JE 0206
01FF:  PUSH #39
0201:  PUSH #53
0203:  JMP 020d
0206:  PUSH #31
0208:  PUSH #85
020A:  JMP 020d
020D:  CALL 01a6
0210:  POP r0
0212:  CMP [0], #31
0215:  JE 0221
0218:  CALL 0222
021B:  ADD [0], #1
021E:  JMP 01c7
0221:  RET

0222:  MOV r31, r30
...
027C:  MOV r1, r0
027F:  RET
```
Solve:
```py
import subprocess

expected = [145, 71, 76, 180, 92, 18, 9, 153, 1, 135, 127, 4, 152, 26, 199, 60, 44, 7, 102, 139, 30, 71, 97, 77, 243, 117, 177, 100, 20, 59, 120, 239]

def rotr4(x: int) -> int:
    return ((x >> 4) | (x << 4)) % 0x100

flag = [0]*32
for index in range(32):     
    if index & 0x10:        
        if index & 0x08:    
            param_add = 241 
            param_xor = 141 
        else:               
            param_add = 154 
            param_xor = 202 
    else:                   
        if index & 0x08:    
            param_add = 39  
            param_xor = 53  
        else:               
            param_add = 31  
            param_xor = 85  
    rot = rotr4((expected[31 - index] - 55) % 0x100)
    flag[31 - index] = ((rot ^ param_xor) - param_add) % 0x100

hex_flag = bytes(flag).hex()
subprocess.run("./main", input=hex_flag.encode())

```
`379beb69ee3fafbacc35b47c425a29004311a049240d702d7f97d36869f622bf`

# natdo
Main:
```cpp
// Hidden C++ exception states: #wind=2
int __fastcall main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rdx
  unsigned __int8 v4; // al
  LPCVOID *v5; // rdx
  __int64 v6; // r8
  __int128 *v7; // rdx
  __int64 v8; // rbx
  __int64 v9; // rdx
  unsigned __int8 v10; // al
  void *v11; // rcx
  void *v12; // rcx
  DWORD NumberOfBytesWritten; // [rsp+30h] [rbp-D0h] BYREF
  DWORD NumberOfBytesRead; // [rsp+34h] [rbp-CCh] BYREF
  __int128 v16; // [rsp+38h] [rbp-C8h] BYREF
  __int64 v17; // [rsp+48h] [rbp-B8h]
  unsigned __int64 v18; // [rsp+50h] [rbp-B0h]
  LPCVOID lpBuffer[2]; // [rsp+58h] [rbp-A8h] BYREF
  __m128i nNumberOfBytesToWrite; // [rsp+68h] [rbp-98h]
  _BYTE Buffer[512]; // [rsp+80h] [rbp-80h] BYREF

  *(_OWORD *)lpBuffer = 0;
  nNumberOfBytesToWrite = _mm_load_si128((const __m128i *)&xmmword_1400226B0);
  LOBYTE(lpBuffer[0]) = 0;
  sub_1400014B0(&qword_140032550, "Enter flag: ", envp);
  LOBYTE(v3) = 10;
  v4 = sub_140003C40((char *)qword_1400324B0 + *(int *)(qword_1400324B0[0] + 4), v3);
  sub_140001E30(qword_1400324B0, lpBuffer, v4);
  NumberOfBytesWritten = 0;
  v5 = lpBuffer;
  if ( nNumberOfBytesToWrite.m128i_i64[1] > 0xFuLL )
    v5 = (LPCVOID *)lpBuffer[0];
  WriteFile(hFile, v5, nNumberOfBytesToWrite.m128i_u32[0], &NumberOfBytesWritten, 0);
  ReadFile(hFile, Buffer, 0x1FFu, &NumberOfBytesRead, 0);
  if ( NumberOfBytesRead >= 0x200uLL )
    sub_1400069C4();
  Buffer[NumberOfBytesRead] = 0;
  v16 = 0;
  v17 = 0;
  v18 = 0;
  v6 = -1;
  do
    ++v6;
  while ( Buffer[v6] );
  sub_140001760(&v16, Buffer);
  v7 = &v16;
  if ( v18 > 0xF )
    v7 = (__int128 *)v16;
  v8 = sub_140001870(&qword_140032550, v7, v17);
  LOBYTE(v9) = 10;
  v10 = sub_140003C40(v8 + *(int *)(*(_QWORD *)v8 + 4LL), v9);
  sub_1400037F0(v8, v10);
  sub_1400033A0(v8);
  if ( v18 > 0xF )
  {
    v11 = (void *)v16;
    if ( v18 + 1 >= 0x1000 )
    {
      v11 = *(void **)(v16 - 8);
      if ( (unsigned __int64)(v16 - (_QWORD)v11 - 8) > 0x1F )
        invalid_parameter_noinfo_noreturn();
    }
    j_j_free(v11);
  }
  v17 = 0;
  v18 = 15;
  LOBYTE(v16) = 0;
  if ( nNumberOfBytesToWrite.m128i_i64[1] > 0xFuLL )
  {
    v12 = (void *)lpBuffer[0];
    if ( (unsigned __int64)(nNumberOfBytesToWrite.m128i_i64[1] + 1) >= 0x1000 )
    {
      v12 = (void *)*((_QWORD *)lpBuffer[0] - 1);
      if ( (unsigned __int64)((char *)lpBuffer[0] - (char *)v12 - 8) > 0x1F )
        invalid_parameter_noinfo_noreturn();
    }
    j_j_free(v12);
  }
  return 0;
}
```

The programme is creating a `hFile` and read it, however `hFile` isn't a file but a `HANDLE` so it could be a file, a pipe or a socket!

Next we're going to trace what `hFile` really is.

The data xref leads us to this
```cpp
HANDLE sub_140001000()
{
  HANDLE result; // rax
  _QWORD v4[4]; // [rsp+60h] [rbp+0h] BYREF

  _RBP = (_QWORD *)((unsigned __int64)v4 & 0xFFFFFFFFFFFFFFE0uLL);
  *_RBP = 0x727C4525A6047FD9LL;
  _RBP[4] = *_RBP;
  *_RBP = 0x61CD781E152812A6LL;
  _RBP[5] = *_RBP;
  *_RBP = 0xB4CA96E7C820E1C7uLL;
  _RBP[6] = *_RBP;
  *_RBP = 0xEFE74E4E64E718A4uLL;
  _RBP[7] = *_RBP;
  *_RBP = 0x170C2C55FA2A2385LL;
  _RBP[8] = *_RBP;
  *_RBP = 0x55FF482C466151FALL;
  _RBP[9] = *_RBP;
  *_RBP = 0xB4CA96E7C820E1C7uLL;
  _RBP[10] = *_RBP;
  *_RBP = 0xEFE74E4E64E718A4uLL;
  _RBP[11] = *_RBP;
  __asm
  {
    vmovdqu ymm0, [rbp+70h+var_30]
    vpxor   ymm1, ymm0, [rbp+70h+var_50]
  }
  __asm
  {
    vmovdqa [rbp+70h+var_50], ymm1
    vzeroupper
  }
  result = CreateNamedPipeA(
             (LPCSTR)(((unsigned __int64)v4 & 0xFFFFFFFFFFFFFFE0uLL) + 32),
             3u,
             6u,
             0xFFu,
             0x200u,
             0x200u,
             0,
             0);
  if ( result == (HANDLE)-1LL )
    ExitProcess(0);
  hFile = result;
  return result;
}
```

![{7F773D83-01AD-4F9B-B211-FF3E927E32B6}](https://hackmd.io/_uploads/H1qFKMzpZl.png)

It's created pipe called `CIS2024`

For further inspection, I tried to run it on x64dbg and found this string that I couldn't find while debugging in IDA.

![{5031C6C0-1DE3-44D9-BAB2-EBFBF58DC91A}](https://hackmd.io/_uploads/Hk6gmozpZx.png)

I also noticed that there's a `_scrt_common_main_seh`, this runs before main, so we'll see what `innitterm` do.

![{D1EABA44-E731-4EBA-BD54-678A88AE848B}](https://hackmd.io/_uploads/S1284tGpZx.png)

The last function 
```cpp
void sub_140001130()
{
  HRSRC ResourceA; // rax
  HRSRC v1; // rbx
  HGLOBAL Resource; // rax
  const void *v3; // rdi
  DWORD v4; // eax
  DWORD v5; // ebx
  void *v6; // rsi
  int v7; // ebx
  __m128 v8; // [rsp+40h] [rbp-38h]
  CHAR Type[16]; // [rsp+50h] [rbp-28h] BYREF

  *(_QWORD *)Type = 0x170C2C55FA646AC7LL;
  *(_QWORD *)&Type[8] = 0x55FF482C466151FALL;
  v8.m128_u64[0] = 0x170C2C55FA2A2385LL;
  v8.m128_u64[1] = 0x55FF482C466151FALL;
  *(__m128 *)Type = _mm_xor_ps((__m128)_mm_load_si128((const __m128i *)Type), v8);
  ResourceA = FindResourceA(0, (LPCSTR)0x66, Type);
  v1 = ResourceA;
  if ( !ResourceA
    || (Resource = LoadResource(0, ResourceA)) == 0
    || (v3 = LockResource(Resource)) == 0
    || (v4 = SizeofResource(0, v1)) == 0 )
  {
    ExitProcess(1u);
  }
  v5 = v4;
  v6 = operator new(v4);
  memcpy(v6, v3, v5);
  v7 = 0;
  if ( CreateThread(0, 0, StartAddress, v6, 0, 0) )
    v7 = 1;
  else
    j_j_free(v6);
  dword_140032220 = v7;
}
```
What it's doing is, loads hidden resource then copies it and executes it in a new thread, which is `StartAddress`
```cpp
__int64 __fastcall StartAddress(char *lpThreadParameter)
{
  char *v3; // rbp
  char *v4; // rbx
  __int64 i; // rcx
  const CHAR *v6; // rsi
  unsigned int v7; // edi
  unsigned int *v8; // rbx
  const CHAR *v9; // r11
  const CHAR *v10; // r8
  __int64 v11; // rdx
  int v12; // r10d
  _WORD *v13; // r9
  const CHAR *j; // r14
  HMODULE LibraryA; // rbp
  int v16; // eax
  FARPROC *v17; // rbx
  __int64 *v18; // rdi
  bool v19; // sf
  const CHAR *v20; // rdx

  if ( *(_QWORD *)lpThreadParameter != 0x44332211EFBEADDELL )
    return 0;
  v3 = lpThreadParameter + 64;
  sub_1400039A0(lpThreadParameter + 64, *((unsigned int *)lpThreadParameter + 3), lpThreadParameter + 48, 16);
  v4 = &v3[40 * *((_DWORD *)lpThreadParameter + 11)];
  v6 = (const CHAR *)VirtualAlloc(
                       *((LPVOID *)lpThreadParameter + 4),
                       (unsigned int)(*((_DWORD *)v4 - 7) + *((_DWORD *)v4 - 6)),
                       0x3000u,
                       0x40u);
  if ( !v6 )
    v6 = (const CHAR *)VirtualAlloc(0, (unsigned int)(*((_DWORD *)v4 - 7) + *((_DWORD *)v4 - 6)), 0x3000u, 0x40u);
  v7 = 0;
  if ( *((_DWORD *)lpThreadParameter + 11) )
  {
    v8 = (unsigned int *)(lpThreadParameter + 84);
    do
    {
      memcpy((void *)&v6[*(v8 - 2)], &v3[*v8 - (unsigned __int64)*((unsigned int *)lpThreadParameter + 2)], *(v8 - 1));
      ++v7;
      v8 += 10;
    }
    while ( v7 < *((_DWORD *)lpThreadParameter + 11) );
  }
  v9 = &v6[-*((_QWORD *)lpThreadParameter + 4)];
  if ( v6 != *((const CHAR **)lpThreadParameter + 4) )
  {
    v10 = &v6[*((unsigned int *)lpThreadParameter + 6)];
    if ( v10 )
    {
      v11 = *((unsigned int *)v10 + 1);
      for ( i = (unsigned int)(v11 + *(_DWORD *)v10); *(_DWORD *)v10 + (_DWORD)v11; i = (unsigned int)(*(_DWORD *)v10 + v11) )
      {
        v12 = 0;
        v13 = v10 + 8;
        if ( ((v11 - 8) & 0xFFFFFFFFFFFFFFFEuLL) != 0 )
        {
          do
          {
            if ( (*v13 & 0xF000) == 0xA000 )
              *(_QWORD *)&v6[(*v13 & 0xFFF) + *(unsigned int *)v10] += v9;
            v11 = *((unsigned int *)v10 + 1);
            ++v12;
            ++v13;
          }
          while ( v12 < (unsigned __int64)(v11 - 8) >> 1 );
        }
        v10 += (unsigned int)v11;
        v11 = *((unsigned int *)v10 + 1);
      }
    }
  }
  for ( j = &v6[*((unsigned int *)lpThreadParameter + 4)]; *((_DWORD *)j + 3); j += 20 )
  {
    LibraryA = LoadLibraryA(&v6[*((unsigned int *)j + 3)]);
    v16 = *(_DWORD *)j;
    if ( !*(_DWORD *)j )
      v16 = *((_DWORD *)j + 4);
    v17 = (FARPROC *)&v6[*((unsigned int *)j + 4)];
    v18 = (__int64 *)&v6[v16];
    v19 = *v18 < 0;
    if ( *v18 )
    {
      i = *v18;
      do
      {
        if ( v19 )
          v20 = (const CHAR *)(unsigned __int16)i;
        else
          v20 = &v6[i + 2];
        ++v18;
        *v17++ = GetProcAddress(LibraryA, v20);
        i = *v18;
        v19 = *v18 < 0;
      }
      while ( *v18 );
    }
  }
  ((void (__fastcall *)(__int64))&v6[*((unsigned int *)lpThreadParameter + 10)])(i);
  return 1;
}
```
This is a PE loader, so we need to "reconstruct" it to get the actual code.

First I copied the address when the function about to jump to payload

![{13A4D237-8FBA-4EF0-A0BE-D9C6061F0BDD}](https://hackmd.io/_uploads/B1WHGjzpbe.png)

Next we'll dump it into a .bin using x64dbg

```cpp
// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_1000(__int64 a1, __int64 a2)
{
  __int64 v3; // r8
  __int64 v4; // rax
  __int64 v5; // rdx
  __int128 v6; // xmm1
  __int128 v7; // xmm0
  _OWORD *v8; // rbx
  __int64 v11; // rax
  __int64 v12; // rdx
  unsigned int v13; // eax
  __int64 v14; // rbx
  __int64 v15; // r8
  __int64 v16; // rcx
  __int64 v17; // rdx
  __int64 v18; // rdi
  __int64 v19; // rdx
  __int64 v20; // rcx
  int v21; // edx
  int v22; // r8d
  int v23; // r9d
  __int64 v24; // rcx
  int v25; // eax
  _QWORD *v26; // r9
  __int64 v28; // [rsp+70h] [rbp+0h] BYREF

  _RBP = (_QWORD *)((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL);
  strcpy((char *)(((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 144), "tin chuan chua");
  strcpy((char *)(((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 64), "the co lam duoc khong");
  if ( !(unsigned int)sub_14F3(a1, a2, L"SHA512", (unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL, 0, 8) )
  {
    v3 = -1;
    *(_OWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 96] = 0;
    v4 = -1;
    *(_OWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 112] = 0;
    *(_OWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 128] = 0;
    do
      ++v4;
    while ( *((_BYTE *)_RBP + v4 + 64) );
    do
      ++v3;
    while ( *((_BYTE *)_RBP + v3 + 144) );
    if ( !(unsigned int)sub_151D(a1, 0, _RBP + 18, *_RBP, v3, _RBP + 8) )
    {
      v6 = *(_OWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 112];
      *(_OWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 32] = *(_OWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 96];
      v7 = *(_OWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 128];
      *(_OWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 48] = v6;
      *(_OWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 64] = v7;
      v8 = (_OWORD *)sub_1524(a1, 0, v5, 64);
      *v8 = 0;
      v8[1] = 0;
      v8[2] = 0;
      v8[3] = 0;
      *_RBP = 0x3C51368C95C2D727LL;
      *(_QWORD *)&algn_40[(unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL] = *(_QWORD *)((unsigned __int64)&v28
                                                                                     & 0xFFFFFFFFFFFFFFE0LL);
      *_RBP = 0x8BE1224756C79450LL;
      *(_QWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 8] = *(_QWORD *)((unsigned __int64)&v28
                                                                                           & 0xFFFFFFFFFFFFFFE0LL);
      *_RBP = 0x48BD24C69A733775LL;
      *(_QWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 16] = *(_QWORD *)((unsigned __int64)&v28
                                                                                            & 0xFFFFFFFFFFFFFFE0LL);
      *_RBP = 0xEC23249F40BD14FELL;
      *(_QWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 24] = *(_QWORD *)((unsigned __int64)&v28
                                                                                            & 0xFFFFFFFFFFFFFFE0LL);
      *_RBP = 0x59215FFCC9EC8B7BLL;
      *(_QWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 96] = *(_QWORD *)((unsigned __int64)&v28
                                                                                            & 0xFFFFFFFFFFFFFFE0LL);
      *_RBP = 0xBFD31275058ED70CLL;
      *(_QWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 104] = *(_QWORD *)((unsigned __int64)&v28
                                                                                             & 0xFFFFFFFFFFFFFFE0LL);
      *_RBP = 0x48BD24C69A733775LL;
      *(_QWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 112] = *(_QWORD *)((unsigned __int64)&v28
                                                                                             & 0xFFFFFFFFFFFFFFE0LL);
      *_RBP = 0xEC23249F40BD14FELL;
      *(_QWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 120] = *(_QWORD *)((unsigned __int64)&v28
                                                                                             & 0xFFFFFFFFFFFFFFE0LL);
      __asm
      {
        vmovdqu ymm0, [rbp+0F0h+var_50]
        vpxor   ymm1, ymm0, [rbp+0F0h+var_B0]
        vmovdqa [rbp+0F0h+var_B0], ymm1
        vzeroupper
      }
      v11 = MEMORY[0x7FFF4D2A05F0](a1, 0, 3221225472LL, _RBP + 8, 1, 0);
      qword_1BB00 = v11;
      if ( v11 != -1 )
      {
        if ( (unsigned int)MEMORY[0x7FFF4D2A09A0](a1, 0, v8, v11, 64, (char *)_RBP + 12) )
        {
          *(__int64 *)((char *)&qword_18[1] + ((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL)) = *(unsigned int *)&algn_2[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 10];
          *(__int64 *)((char *)qword_18 + ((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL)) = (__int64)v8;
          *(_QWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 80] = 0;
          *_RBP = 0;
          *(_DWORD *)&algn_2[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 10] = 0;
          *(_DWORD *)((char *)&qword_10 + ((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL)) = 0;
          if ( !(unsigned int)sub_14F3(a1, 0, L"AES", _RBP + 18, 0, 0)
            && !(unsigned int)sub_14F9(
                                a1,
                                0,
                                L"ObjectLength",
                                *(_QWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 80],
                                (char *)_RBP + 12,
                                4) )
          {
            v13 = *(_DWORD *)&algn_2[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 10];
            if ( v13 )
            {
              v14 = sub_1524(a1, 0, v12, v13);
              if ( !(unsigned int)sub_14FF(
                                    a1,
                                    0,
                                    L"ChainingMode",
                                    *(_QWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 80],
                                    L"ChainingModeCBC",
                                    32)
                && !(unsigned int)sub_150B(
                                    a1,
                                    0,
                                    (unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL,
                                    *(_QWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 80],
                                    v14,
                                    *(unsigned int *)&algn_2[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 10]) )
              {
                v15 = *(unsigned int *)((char *)&qword_18[1] + ((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL));
                v16 = *_RBP;
                *(_DWORD *)&algn_2[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 6] = 0;
                if ( !(unsigned int)sub_1511(a1, 0, _RBP + 3, v16, v15, 0) )
                {
                  v18 = sub_1524(
                          a1,
                          0,
                          v17,
                          *(unsigned int *)&algn_2[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 6]);
                  if ( !(unsigned int)sub_1511(
                                        v18,
                                        0,
                                        *(__int64 *)((char *)qword_18 + ((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL)),
                                        *_RBP,
                                        *(unsigned int *)((char *)&qword_18[1]
                                                        + ((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL)),
                                        0) )
                  {
                    v20 = *_RBP;
                    *(__int64 *)((char *)&qword_18[1] + ((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL)) = *(unsigned int *)&algn_2[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 6];
                    *(__int64 *)((char *)qword_18 + ((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL)) = v18;
                    sub_1517(v18, 0, v19, v20);
                    sub_1505(v18, 0, 0, *(_QWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 80]);
                    sub_152C(v18, 0, v21, v14, v22, v23);
                    v24 = *(__int64 *)((char *)qword_18 + ((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL));
                    *(_DWORD *)&algn_40[(unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL] = 1142706397;
                    *(_DWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 4] = 1433943489;
                    *(_DWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 8] = 921397323;
                    *(_DWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 12] = 42407791;
                    *(_DWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 16] = 1514215304;
                    *(_DWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 20] = 1362471257;
                    *(_DWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 24] = 1637299534;
                    *(_DWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 28] = -336220085;
                    v25 = sub_F260(v18, 0, _RBP + 8, v24, 32);
                    v26 = _RBP + 2;
                    if ( !v25 )
                    {
                      MEMORY[0x7FFF4D2A0A90](v18, 0, "Correct\n", 0, 8, v26);
                      return 0;
                    }
                    MEMORY[0x7FFF4D2A0A90](v18, 0, "Wrong!\n", 0, 7, v26);
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  return 1;
}
```

We basically have everything this is a `PBKDF2-HMAC-SHA512`, we saw a crypto routine at the original exe.

But first we're converting this into bytes
```cpp
 *(_DWORD *)&algn_40[(unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL]        = 1142706397;
 *(_DWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 4]  = 1433943489;
 *(_DWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 8]  = 921397323;
 *(_DWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 12] = 42407791;
 *(_DWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 16] = 1514215304;
 *(_DWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 20] = 1362471257;
 *(_DWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 24] = 1637299534;
 *(_DWORD *)&algn_40[((unsigned __int64)&v28 & 0xFFFFFFFFFFFFFFE0LL) + 28] = -336220085;
```

```py
import struct

vals = [
    1142706397,
    1433943489,
    921397323,
    42407791,
    1514215304,
    1362471257,
    1637299534,
    -336220085 & 0xffffffff
]

cipher = b"".join(struct.pack("<I", v) for v in vals)
print(cipher.hex())

# dd501c44c13d78554b68eb366f1787028817415a59a935514e3597614bb0f5eb
```

Solve:

```py
from hashlib import pbkdf2_hmac
from Crypto.Cipher import AES

password = b"tin chuan chua"
salt = b"the co lam duoc khong"

dk = pbkdf2_hmac("sha512", password, salt, 10000, 48)
key, iv = dk[:32], dk[32:]

ct = bytes.fromhex("dd501c44c13d78554b68eb366f1787028817415a59a935514e3597614bb0f5eb")

pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
flag = pt[:-pt[-1]].decode()
print(flag)

# CIS2024{Ju57_51mpl3_p3_l04d3R}
```

 








