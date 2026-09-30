# KMA CTF II

## ASM101
```asm
check_flag:
    sub esp, 4
    mov [esp], ecx
    test ecx, ecx 	
    jz fail
    mov eax, 0xA5A5F00D
    mov ecx, [esp]
    mov edx, [ecx+0]	
    xor edx, eax
    ror edx, 7
    add edx, 0x9E3779B9
    mov ecx, edx
    shr ecx, 16
    xor edx, ecx
    mov ecx, eax
    ror ecx, 11
    add edx, ecx
    cmp edx, 0x2DB9FFD8
    jne fail			
    add eax, 0x6D2B79F5		
    mov ecx, edx		
    ror ecx, 3		
    xor eax, ecx	

    mov ecx, [esp]		
    mov edx, [ecx+4]		
    xor edx, eax		
    ror edx, 7
    add edx, 0x9E3779B9
    mov ecx, edx
    shr ecx, 16
    xor edx, ecx
    mov ecx, eax
    ror ecx, 11
    add edx, ecx
    cmp edx, 0x61A5876C
    jne fail		
    add eax, 0x6D2B79F5	
    mov ecx, edx		
    ror ecx, 3			
    xor eax, ecx		

    mov ecx, [esp]
    mov edx, [ecx+8]
    xor edx, eax
    ror edx, 7
    add edx, 0x9E3779B9
    mov ecx, edx
    shr ecx, 16
    xor edx, ecx
    mov ecx, eax
    ror ecx, 11
    add edx, ecx
    cmp edx, 0xE973C190
    jne fail	
    add eax, 0x6D2B79F5 
    mov ecx, edx		
    ror ecx, 3			
    xor eax, ecx		
    mov ecx, [esp]
    mov edx, [ecx+12]
    xor edx, eax
    ror edx, 7
    add edx, 0x9E3779B9
    mov ecx, edx
    shr ecx, 16
    xor edx, ecx
    mov ecx, eax
    ror ecx, 11
    add edx, ecx
    cmp edx, 0xA79EBD1F
    jne fail	
    add eax, 0x6D2B79F5
    mov ecx, edx
    ror ecx, 3
    xor eax, ecx

    mov ecx, [esp]
    mov edx, [ecx+16]
    xor edx, eax
    ror edx, 7
    add edx, 0x9E3779B9
    mov ecx, edx
    shr ecx, 16
    xor edx, ecx
    mov ecx, eax
    ror ecx, 11
    add edx, ecx
    cmp edx, 0x984A61DC		
    jne fail
    add eax, 0x6D2B79F5
    mov ecx, edx
    ror ecx, 3
    xor eax, ecx
    mov ecx, [esp]
    mov edx, [ecx+20]
    xor edx, eax
    ror edx, 7
    add edx, 0x9E3779B9
    mov ecx, edx
    shr ecx, 16
    xor edx, ecx
    mov ecx, eax
    ror ecx, 11
    add edx, ecx
    cmp edx, 0xA1DE2F85
    jne fail		
    add eax, 0x6D2B79F5
    mov ecx, edx
    ror ecx, 3
    xor eax, ecx
    mov ecx, [esp]
    mov edx, [ecx+24]
    xor edx, eax
    ror edx, 7
    add edx, 0x9E3779B9
    mov ecx, edx
    shr ecx, 16
    xor edx, ecx
    mov ecx, eax
    ror ecx, 11
    add edx, ecx
    cmp edx, 0x6E1CED6C
    jne fail	
    add eax, 0x6D2B79F5
    mov ecx, edx
    ror ecx, 3
    xor eax, ecx
    mov ecx, [esp]
    mov edx, [ecx+28]
    xor edx, eax
    ror edx, 7
    add edx, 0x9E3779B9
    mov ecx, edx
    shr ecx, 16
    xor edx, ecx
    mov ecx, eax
    ror ecx, 11
    add edx, ecx
    cmp edx, 0x7E7957EC
    jne fail		
    add eax, 0x6D2B79F5
    mov ecx, edx
    ror ecx, 3
    xor eax, ecx
    mov ecx, [esp]
    mov edx, [ecx+32]
    xor edx, eax
    ror edx, 7
    add edx, 0x9E3779B9
    mov ecx, edx
    shr ecx, 16
    xor edx, ecx
    mov ecx, eax
    ror ecx, 11
    add edx, ecx
    cmp edx, 0xF7D801A2
    jne fail		
    add eax, 0x6D2B79F5
    mov ecx, edx
    ror ecx, 3
    xor eax, ecx
    mov ecx, [esp]
    movzx edx, word ptr [ecx+36]
    xor edx, eax
    ror edx, 5
    add edx, 0x85EBCA6B
    mov ecx, edx
    shr ecx, 13
    xor edx, ecx
    mov ecx, eax
    shl ecx, 1
    add edx, ecx
    cmp edx, 0x0C4B6704
    jne fail				

    mov ecx, [esp]
    cmp byte ptr [ecx+38], 0
    jne fail

    mov eax, 1
    add esp, 4
    ret

fail:
    xor eax, eax
    add esp, 4
    ret
```

The Assembly code works like this:
```cpp
eax = 0xA5A5F00D;
edx = p[0];

edx ^= eax;
edx = ror32(edx, 7);
edx += 0x9E3779B9;

ecx = edx;
ecx >>= 16;
edx ^= ecx;

ecx = eax;
ecx = ror32(ecx, 11);
edx += ecx;

if (edx != 0x2DB9FFD8)
    return 0;

eax += 0x6D2B79F5;

ecx = edx;
ecx = ror32(ecx, 3);
eax ^= ecx;

return eax; 
```

So, there are 9 chunks in total each chunks are basically the same.
Though this chunk is different.

```asm
 movzx edx, word ptr [ecx+36]
    xor edx, eax
    ror edx, 5
    add edx, 0x85EBCA6B
    mov ecx, edx
    shr ecx, 13
    xor edx, ecx
    mov ecx, eax
    shl ecx, 1
    add edx, ecx
    cmp edx, 0x0C4B6704
    jne fail				

    mov ecx, [esp]
    cmp byte ptr [ecx+38], 0
    jne fail

    mov eax, 1
    add esp, 4
    ret
```

Which can translate to

```cpp
edx ^= eax;
edx = ror32(edx, 5);
edx += 0x85EBCA6B;

ecx = edx;
ecx >>= 13;
edx ^= ecx;

ecx = eax;
ecx <<= 1;
edx += ecx;

if (edx != 0x0C4B6704)
    return 0;
```

It's pretty simple now. Those `cmp edx` are the expected value after the transformation for each chunks, and for the first 9 chunks it reads 4 bytes each chunk.

Also, to "reverse" this part:
```asm
    add edx, 0x9E3779B9
    mov ecx, edx
    shr ecx, 16
    xor edx, ecx
    mov ecx, eax
```
You must understand how shifting works
So, `ecx = edx` then `ecx >>= 16` which means shift the 16 bits of `0x9E3779B9` to right `0x00009E37`
. 

Next `xor edx, ecx` and since we have `ecx = edx` that means 
```
0000 9E37
XOR
9E37 79B9
---------
9E37 E78E
```


Solve:
```py
MASK = 0xFFFFFFFF


def ror32(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def rol32(x, n):
    return ((x << n) | (x >> (32 - n))) & MASK


targets = [
    0x2DB9FFD8,
    0x61A5876C,
    0xE973C190,
    0xA79EBD1F,
    0x984A61DC,
    0xA1DE2F85,
    0x6E1CED6C,
    0x7E7957EC,
    0xF7D801A2
]


eax = 0xA5A5F00D
flag = bytearray()


for target in targets:

    edx = target

    ecx = eax
    ecx = ror32(ecx, 11)

    edx = edx - ecx
    edx &= MASK


    high = (edx >> 16) & 0xFFFF #gets upper 16 bits
    new_low = edx & 0xFFFF

    old_low = new_low ^ high

    edx = (high << 16) | old_low #rebuild 


    edx = edx - 0x9E3779B9
    edx &= MASK


    edx = rol32(edx, 7)


    edx = edx ^ eax
    edx &= MASK


    block = edx.to_bytes(4, "little")

    flag += block


    eax = eax + 0x6D2B79F5
    eax &= MASK

    ecx = target
    ecx = ror32(ecx, 3)

    eax = eax ^ ecx
    eax &= MASK


# Final 2-byte block

target = 0x0C4B6704

edx = target


ecx = eax
ecx = (ecx << 1) & MASK

edx = edx - ecx
edx &= MASK


y = edx

edx = y
edx ^= y >> 13
edx ^= y >> 26
edx &= MASK


edx = edx - 0x85EBCA6B
edx &= MASK


edx = rol32(edx, 5)


edx = edx ^ eax
edx &= MASK


last_two = (edx & 0xFFFF).to_bytes(2, "little")

flag += last_two


print()
print("FLAG:", flag.decode())

# KCSC{f926b3e222d7afee57071b2256839701}

```


## Crackme

Shift + f12 to find strings related to the challenge and you will find the main function.

```cpp
__int64 __fastcall sub_7FF6298D1EE0(const CHAR *a1, HWND a2, struct _COMMCONFIG *a3)
{
  int v3; // eax
  __m128i v4; // xmm1
  __m128i v5; // xmm1
  FILE *v6; // rax
  size_t v7; // rax
  __int8 v8; // cl
  size_t Size; // [rsp+30h] [rbp-D0h] BYREF
  void *Buf1; // [rsp+38h] [rbp-C8h] BYREF
  __m128 v12; // [rsp+40h] [rbp-C0h] BYREF
  char Buffer[256]; // [rsp+50h] [rbp-B0h] BYREF

  v3 = sub_7FF6298D19A0(a1, a2, a3);
  v12.m128_u64[0] = 0x408B602B6BDFD5EDLL;
  v12.m128_u64[1] = 0x810EBBF651A0AC50uLL;
  if ( v3 )
  {
    v4 = _mm_cvtsi32_si128((char)v3);
    v5 = _mm_unpacklo_epi8(v4, v4);
    v12 = _mm_xor_ps(
            (__m128)_mm_loadu_si128((const __m128i *)&v12),
            (__m128)_mm_shuffle_epi32(_mm_unpacklo_epi16(v5, v5), 0));
  }
  memset(Buffer, 0, sizeof(Buffer));
  Buf1 = 0;
  LODWORD(Size) = 0;
  sub_7FF6298D1020("Enter flag: ");
  v6 = _acrt_iob_func(0);
  if ( fgets(Buffer, 256, v6) )
  {
    v7 = strlen(Buffer);
    if ( v7 )
    {
      do
      {
        v8 = v12.m128_i8[v7 + 15];
        if ( v8 != 10 && v8 != 13 )
          break;
        if ( --v7 >= 0x100 )
          _report_rangecheckfailure();
        Buffer[v7] = 0;
      }
      while ( v7 );
      if ( v7 )
        sub_7FF6298D1B40((__int64)&v12, (__int64)Buffer, (const CHAR *)(unsigned int)v7, (__int64)&Buf1, (__int64)&Size);
    }
    sub_7FF6298D1020("Wrong!\n");
  }
  return 0;
}
```

Checking the `sub_7FF6298D19A0`
```cpp
__int64 __fastcall sub_7FF6298D19A0(const CHAR *a1, HWND a2, struct _COMMCONFIG *a3)
{
  BOOL v3; // ebx
  int v4; // edi
  HWND v5; // rdx
  LPCWSTR v6; // rcx
  LPCOMMCONFIG v7; // r8
  ULONG v8; // eax
  struct _PEB *v9; // rax
  unsigned int v10; // ebx
  HMODULE ModuleHandleA; // rax
  HWND v12; // rdx
  const WCHAR *v13; // rcx
  struct _COMMCONFIG *v14; // r8
  void *v15; // r9
  NTSTATUS (__stdcall *NtQueryInformationProcess)(HANDLE, PROCESSINFOCLASS, PVOID, ULONG, PULONG); // rdi
  __int64 v17; // rax
  HWND v18; // rdx
  const WCHAR *v19; // rcx
  struct _COMMCONFIG *v20; // r8
  __int64 v21; // rax
  __int64 v22; // rax
  void *v23; // rdx
  const CHAR *v24; // rcx
  DWORD v25; // r8d
  void *v26; // r9
  __int64 v27; // rdi
  __int64 v28; // rax
  __int64 v29; // rcx
  __int64 result; // rax
  DWORD nOutBufferSize; // [rsp+20h] [rbp-38h]
  DWORD *v32; // [rsp+28h] [rbp-30h]
  LPVOID lpFiber; // [rsp+30h] [rbp-28h] BYREF
  int i; // [rsp+38h] [rbp-20h] BYREF
  int v35; // [rsp+3Ch] [rbp-1Ch] BYREF

  v35 = 0;
  v3 = CommConfigDialogA(a1, a2, a3);
  v4 = v3 + 10;
  v8 = CommConfigDialogW(v6, v5, v7);
  AddVectoredContinueHandler(v8, (PVECTORED_EXCEPTION_HANDLER)&v35);
  if ( v35 )
    v4 = v3 + 11;
  v9 = NtCurrentPeb();
  if ( v9 )
  {
    v10 = v4 + 1;
    if ( !v9->BeingDebugged )
      v10 = v4;
  }
  else
  {
    v10 = v4;
  }
  ModuleHandleA = GetModuleHandleA("ntdll.dll");
  if ( ModuleHandleA )
  {
    NtQueryInformationProcess = (NTSTATUS (__stdcall *)(HANDLE, PROCESSINFOCLASS, PVOID, ULONG, PULONG))GetProcAddress(ModuleHandleA, "NtQueryInformationProcess");
    if ( NtQueryInformationProcess )
    {
      i = 0;
      LODWORD(v17) = CommConfigDialogW(v13, v12, v14);
      if ( ((int (__fastcall *)(__int64, __int64, int *, __int64, _QWORD))NtQueryInformationProcess)(v17, 7, &i, 4, 0) >= 0
        && i )
      {
        ++v10;
      }
      lpFiber = 0;
      LODWORD(v21) = CommConfigDialogW(v19, v18, v20);
      nOutBufferSize = 0;
      if ( ((int (__fastcall *)(__int64, __int64, LPVOID *, __int64))NtQueryInformationProcess)(v21, 30, &lpFiber, 8) >= 0 )
      {
        v13 = (const WCHAR *)lpFiber;
        if ( lpFiber )
        {
          DeleteFiber(lpFiber);
          ++v10;
        }
      }
    }
  }
  if ( qword_7FF6298D5138 )
    v22 = qword_7FF6298D5138();
  else
    LODWORD(v22) = CallNamedPipeA((LPCSTR)v13, v12, (DWORD)v14, v15, nOutBufferSize, v32, (DWORD)lpFiber);
  v27 = v22;
  for ( i = 0; i < 100000; ++i )
    ;
  if ( qword_7FF6298D5138 )
    v28 = qword_7FF6298D5138();
  else
    LODWORD(v28) = CallNamedPipeA(v24, v23, v25, v26, nOutBufferSize, v32, (DWORD)lpFiber);
  v29 = v28;
  result = v10 + 1;
  if ( (unsigned __int64)(v29 - v27) <= 0xC8 )
    return v10;
  return result;
}
```

We can see that it's calling some random functions. But what's interesting is, that's not the actual function the programme was calling, it's actually calling `IsDebuggerPresent` 

![image](https://hackmd.io/_uploads/S1oiTh5tMg.png)

Same goes for those:

![{DF885BE9-53B8-4688-9492-D653F36947AA}](https://hackmd.io/_uploads/ByP0ahqYfg.png)

This is some IAT decoy technique where the actual API calling isn't present when we only do static analyst 

More on how this works later.

Now we can confirm that `ComConfigDialogA` is actually an antidebug check, by walking through it, our register returned 1.

![{CFBEBE84-27ED-4414-A2C0-D4C59DC94A9C}](https://hackmd.io/_uploads/ryt-0U1qGl.png)

Then it's adding `0A` and for each antidbg check it'll continue adding 1.

So to completely bypass the antidebug check we just have to set the `RAX` register to `0A`.

The rest of the challenge is inside `sub_7FF6298D1B40` which 

```cpp
void __fastcall __noreturn sub_7FF66E8F1B40(__int64 a1, __int64 a2, const CHAR *a3, __int64 a4, __int64 a5)
{
  int v5; // edx
  __int64 v6; // rcx
  int v7; // edx
  __int64 v8; // rcx
  signed int v9; // edx
  __int64 v10; // rcx
  int v11; // eax
  const CHAR *dwFlags; // [rsp+20h] [rbp-E0h]
  ULONG cbIV; // [rsp+28h] [rbp-D8h]
  BCRYPT_ALG_HANDLE hAlgorithm; // [rsp+68h] [rbp-98h]
  int v15; // [rsp+70h] [rbp-90h]
  char v16; // [rsp+74h] [rbp-8Ch]
  ULONG dwTable[2]; // [rsp+78h] [rbp-88h]
  UCHAR pbOutput[4]; // [rsp+80h] [rbp-80h]
  int Size; // [rsp+84h] [rbp-7Ch]
  int Size_4; // [rsp+88h] [rbp-78h]
  UCHAR pbIV[16]; // [rsp+90h] [rbp-70h]
  WCHAR pszContext[4]; // [rsp+A0h] [rbp-60h]
  wchar_t String[8]; // [rsp+A8h] [rbp-58h]
  __int128 v24; // [rsp+B8h] [rbp-48h]
  int v25; // [rsp+C8h] [rbp-38h]
  WCHAR pszProperty[16]; // [rsp+D0h] [rbp-30h] BYREF

  *(__m128i *)pbIV = _mm_load_si128((const __m128i *)&xmmword_7FF66E8F3380);
  Size = (int)a3;
  memset(pszProperty, 0, 28);
  v5 = 0;
  *(_DWORD *)pbOutput = 397332;
  hAlgorithm = (BCRYPT_ALG_HANDLE)0x323B3C3B3C343D16LL;
  v15 = 808532504;
  v16 = 0;
  *(_QWORD *)pszContext = 0;
  *(_OWORD *)String = 0;
  v25 = 0;
  v24 = 0;
  do
  {
    v6 = v5++;
    pszContext[v6] = (char)(pbOutput[v6] ^ 0x55);
  }
  while ( pbOutput[v5] );
  pszContext[v5] = 0;
  v7 = 0;
  do
  {
    v8 = v7++;
    pszProperty[v8] = (char)(*((_BYTE *)&hAlgorithm + v8) ^ 0x55);
  }
  while ( *((_BYTE *)&hAlgorithm + v7) );
  pszProperty[v7] = 0;
  v9 = 0;
  do
  {
    v10 = v9++;
    String[v10] = (char)(pbIV[v10] ^ 0x55);
  }
  while ( pbIV[v9] );
  String[v9] = 0;
  *(_QWORD *)dwTable = 0;
  hAlgorithm = 0;
  *(_DWORD *)pbOutput = 0;
  Size_4 = 0;
  *(_DWORD *)pbIV = -58783138;
  *(_DWORD *)&pbIV[4] = 700098896;
  *(_DWORD *)&pbIV[8] = 1962973908;
  *(_DWORD *)&pbIV[12] = 900696333;
  v11 = CompareStringA(v9, v9, a3, 0, dwFlags, cbIV);
  FatalExit(v11);
}
```
When passing through the loop, the programme resolved this cryptographic function as "AES Chainingmode CBC"

The key is (starts at offset `rax`)
`E7DFD561216A814A5AA6AA5BFCB1048B`

Our IV is stored inside `sub_7FF66E8F1B40`
`5E0A7FFC50A9BA29D49A00750D89AF35`

Cipher `unk_7FF66E8F5080`
`19AD4F480470300337C6912FA49FDB3A56A187D707C8738E5F7E2779CC79F54F6F2F736997B9C10B89F482308B3B9A8A3799D604CAEF54D4A35826BF606AEC22`

![{AF637CBB-0091-448A-8101-9AB66CC0310A}](https://hackmd.io/_uploads/Sk0_m_J5fl.png)


`KMACTF{3A5677AD6791A04BD7E6EAD48303766619819323}`


Now, if we trace back to the `initterm` we can observe how this thing works.

The function `sub_7FF70BB11500` is a massive IAT, which will resolved once we run it. 


![{1AA2BA8C-06D3-44BB-A080-76A230F50C37}](https://hackmd.io/_uploads/SJIhBJecfe.png)

![{D1726CCC-0DF5-4CD6-A519-70A2552B7151}](https://hackmd.io/_uploads/HyWhDkx9zg.png)

![{19609CD7-EAAB-4CDB-B1A4-5196F37B7D7C}](https://hackmd.io/_uploads/Hy9aPyl5Ge.png)

I believe it works like this:

hash fake import name -> switch -> hashed real import name

```
if (hash(importName) == hash("fakeahhimportname"))
{
    targethash = hash("realcoolimportname");
}
```

## DECAGRAMMATON

### Stage 1

![{C673CF0B-5B5F-4536-87A9-CB105738D1BB}](https://hackmd.io/_uploads/B1izTmV5Ge.png)

We are provided with a custom packed exe with no IAT

But if you look at `(Heur)Packer: Compressed or packed data[Section 2 (".data") compressed]` DIE suggest that we have to do something with the `.data` section here.

We don't know what API are imported nor the address of IAT, so we know it's going to resolve APIs. But what API? this challenge is filled with junk code and is heavily obfuscated. 

How do we get the payload then? As we know the packed payload is in `.data`.  And so the programme must be unpacking itself during the execution, which is probably exist somewhere in the memory.

Now windows actually preloaded some APIs and one of them is `NtAllocateVirtualMemory`. Why this API specifically? Because the loader might allocate a new memory buffer to unpack its data into, and `NtAllocateVirtualMemory` allocates memory.


![{20D3A6FA-F0D1-4307-B1D1-EC9C3BC9113B}](https://hackmd.io/_uploads/Sy--z8Nqzg.png)

```
__kernel_entry NTSYSCALLAPI NTSTATUS NtAllocateVirtualMemory(
  [in]      HANDLE    ProcessHandle,
  [in, out] PVOID     *BaseAddress,
  [in]      ULONG_PTR ZeroBits,
  [in, out] PSIZE_T   RegionSize,
  [in]      ULONG     AllocationType,
  [in]      ULONG     Protect
);
```

![{19F8CF19-D2B1-4855-A09D-960EAE96A0EA}](https://hackmd.io/_uploads/H1fr9I45Gl.png)

![{F54564AD-D0FE-4C15-8DEC-8F5054E7CE6C}](https://hackmd.io/_uploads/BklP5UVcGe.png)


That means our payload size is `4A00`





We got `006A8D07` as our return address when the bp hits `ZwAllocateVirtualMemory` once we run to that return address


![{39EB499B-6E58-4CDE-AD37-AEE9D2428EDB}](https://hackmd.io/_uploads/H1WcmI4cfg.png)

We can see that the EDX is holding our allocated buffer address

![{54111516-3848-4510-8559-2A973066B835}](https://hackmd.io/_uploads/HkfpQ84qMx.png)

So this is our payload from `00EC0000` to `00EC4A00`

Problem is our payload doesn't have a header, so we're going to try to recover it

Our metadata is actually compressed and it's at the start of ".data" in loader 

`
04 E1 43 01 40 81 09 2C 99 0F 80 06 10 8E 0F 24 03 14 01 F1 0C 47 8C 08 18 01 13 70 CD 06 E0 10 0A 01 8A 80 34 42 88 43 07 38 0A 01 D4 28 C8 42 6A 85 01 B1 1B 74 01 5A 31 D0 8D 90 A1 8A 2A 2C 4E 08 2E 91 12 29 60 10 95 04 94 9C 11 44 38 02 52 01 BF 60 00 00 00 00
`

![{46C34DEA-BF77-4D3F-AEED-13B4FDF62A79}](https://hackmd.io/_uploads/rkgBnVd9Ml.png)

Converting this to code you can see the function where it's compressing our metadata

![{B76F54D9-C144-4FC9-AA41-47BEE2D3302C}](https://hackmd.io/_uploads/HyXd34O9Mx.png)

After rebuilding the metadata we can now recover the header from there, still I don't see the header ANYWHERE in the loader, I don't know if it's intended or not.

### Stage 2

We finally get the payload from the loader

Main:

```cpp

int __stdcall sub_402380(int a1, int a2, int a3, int a4)
{
  unsigned __int16 *v4; // eax
  unsigned __int16 *v5; // edi
  unsigned __int16 *v6; // esi
  unsigned int v7; // eax
  unsigned int v8; // ecx
  unsigned __int16 *v9; // eax
  unsigned __int16 *v10; // edx
  unsigned int v11; // ecx
  unsigned int v12; // eax
  RPC_STATUS v13; // esi
  __int64 v15; // rdi
  __int64 v16; // kr00_8
  HCRYPTPROV v17; // ecx
  __int64 v18; // rax
  __int64 v19; // rax
  CHAR *v20; // eax
  CHAR *v21; // esi
  __int64 v22; // rax
  char *v23; // eax
  BYTE *v24; // eax
  char *v25; // ecx
  unsigned int v26; // eax
  void (__cdecl *v27)(void *); // esi
  unsigned int v28; // edi
  const char *v29; // ecx
  DWORD v30; // edx
  void **v31; // edi
  char v32; // [esp-8h] [ebp-1D0h]
  int v33; // [esp-4h] [ebp-1CCh]
  int v34; // [esp+10h] [ebp-1B8h] BYREF
  char *v35; // [esp+14h] [ebp-1B4h]
  unsigned int v36; // [esp+18h] [ebp-1B0h]
  const char **v37; // [esp+1Ch] [ebp-1ACh]
  BYTE *v38; // [esp+20h] [ebp-1A8h] BYREF
  DWORD cbBinary; // [esp+24h] [ebp-1A4h] BYREF
  unsigned int v40; // [esp+28h] [ebp-1A0h] BYREF
  _DWORD v41[3]; // [esp+2Ch] [ebp-19Ch] BYREF
  _DWORD v42[3]; // [esp+38h] [ebp-190h] BYREF
  RPC_WSTR StringBinding; // [esp+44h] [ebp-184h] BYREF
  RPC_BINDING_HANDLE Binding; // [esp+48h] [ebp-180h] BYREF
  DWORD pcchString; // [esp+4Ch] [ebp-17Ch] BYREF
  __int64 pbBinary; // [esp+50h] [ebp-178h] BYREF
  DWORD v47; // [esp+58h] [ebp-170h]
  unsigned int v48; // [esp+5Ch] [ebp-16Ch]
  __int64 v49; // [esp+60h] [ebp-168h]
  BYTE v50[4]; // [esp+68h] [ebp-160h] BYREF
  int v51; // [esp+6Ch] [ebp-15Ch]
  BYTE pbBuffer[4]; // [esp+70h] [ebp-158h] BYREF
  int v53; // [esp+74h] [ebp-154h] BYREF
  int v54[8]; // [esp+178h] [ebp-50h] BYREF
  char Buffer[20]; // [esp+198h] [ebp-30h] BYREF
  CPPEH_RECORD ms_exc; // [esp+1B0h] [ebp-18h]

  StringBinding = 0;
  Binding = 0;
  v4 = (unsigned __int16 *)malloc(0xAu);
  v5 = v4;
  if ( v4 )
  {
    *(_BYTE *)v4 = byte_406098 ^ byte_406240;
    *((_BYTE *)v4 + 1) = byte_406241 ^ byte_406099;
    *((_BYTE *)v4 + 2) = byte_406242 ^ byte_40609A;
    *((_BYTE *)v4 + 3) = byte_406243 ^ byte_40609B;
    *((_BYTE *)v4 + 4) = byte_406244 ^ byte_40609C;
    *((_BYTE *)v4 + 5) = byte_406245 ^ byte_40609D;
    *((_BYTE *)v4 + 6) = byte_406246 ^ byte_40609E;
    *((_BYTE *)v4 + 7) = byte_406247 ^ byte_40609F;
    *((_BYTE *)v4 + 8) = byte_406248 ^ byte_4060A0;
    *((_BYTE *)v4 + 9) = byte_406249 ^ byte_4060A1;
  }
  v6 = (unsigned __int16 *)malloc(0x20u);
  if ( v6 )
  {
    v7 = 0;
    v8 = (unsigned int)v6 + 31;
    if ( (v6 > (unsigned __int16 *)&unk_4061B7 || v8 < (unsigned int)&xmmword_406198)
      && (v6 > (unsigned __int16 *)&unk_4061D7 || v8 < (unsigned int)&xmmword_4061B8) )
    {
      do
      {
        *(__m128 *)((char *)v6 + v7) = _mm_xor_ps(
                                         *(__m128 *)((char *)&xmmword_4061B8 + v7),
                                         *(__m128 *)((char *)&xmmword_406198 + v7));
        v7 += 16;
      }
      while ( v7 < 0x20 );
    }
    for ( ; v7 < 0x20; ++v7 )
      *((_BYTE *)v6 + v7) = *((_BYTE *)&xmmword_406198 + v7) ^ *((_BYTE *)&xmmword_4061B8 + v7);
  }
  v9 = (unsigned __int16 *)malloc(0x1Au);
  v10 = v9;
  if ( v9 )
  {
    v11 = 0;
    v12 = (unsigned int)v9 + 25;
    if ( (v10 > &word_406095 || v12 < (unsigned int)&xmmword_40607C)
      && (v10 > word_406265 || v12 < (unsigned int)&xmmword_40624C) )
    {
      *(__m128 *)v10 = _mm_xor_ps((__m128)xmmword_40607C, (__m128)xmmword_40624C);
      v11 = 16;
    }
    do
    {
      *((_BYTE *)v10 + v11) = *((_BYTE *)&xmmword_40607C + v11) ^ *((_BYTE *)&xmmword_40624C + v11);
      ++v11;
    }
    while ( v11 < 0x1A );
  }
  if ( RpcStringBindingComposeW(0, v10, v6, v5, 0, &StringBinding) )
    return 1;
  v13 = RpcBindingFromStringBindingW(StringBinding, &Binding);
  RpcStringFreeW(&StringBinding);
  if ( v13 )
    return 1;
  if ( RpcBindingSetAuthInfoW(Binding, 0, 1u, 0, 0, 0) )
  {
    RpcBindingFree(&Binding);
    return 1;
  }
  v15 = sub_402190();
  v37 = (const char **)HIDWORD(v15);
  v16 = sub_402240(v15, HIDWORD(v15));
  v40 = HIDWORD(v16);
  pcchString = v16;
  v17 = hProv;
  if ( !hProv )
  {
    if ( !CryptAcquireContextW(&hProv, 0, 0, 1u, 0xF0000000) )
      goto LABEL_27;
    v17 = hProv;
  }
  if ( !CryptGenRandom(v17, 8u, pbBuffer) )
LABEL_27:
    ExitProcess(1u);
  v18 = sub_403770(*(_DWORD *)pbBuffer, v53, (int)v15 - 2, (unsigned __int64)(v15 - 2) >> 32);
  v38 = (BYTE *)((unsigned __int64)(v18 + 1) >> 32);
  cbBinary = v18 + 1;
  v19 = sub_401F40(pcchString, v40, (int)v18 + 1, v38, v15, HIDWORD(v15));
  pbBinary = v15;
  v47 = pcchString;
  v48 = v40;
  v49 = v19;
  pcchString = 0;
  if ( CryptBinaryToStringA((const BYTE *)&pbBinary, 0x18u, 0x40000001u, 0, &pcchString) )
  {
    v20 = (CHAR *)malloc(pcchString);
    v21 = v20;
    if ( v20 )
    {
      if ( !CryptBinaryToStringA((const BYTE *)&pbBinary, 0x18u, 0x40000001u, v20, &pcchString) )
        free(v21);
    }
  }
  ms_exc.registration.TryLevel = 0;
  pcchString = 0;
  sub_401000((char)Binding);
  if ( pcchString )
  {
    sub_401E10((LPCSTR)pcchString, v50);
    v22 = sub_401F40(*(_DWORD *)v50, v51, cbBinary, v38, v15, v37);
    v33 = HIDWORD(v22);
    v32 = v22;
    v23 = (char *)sub_4010A0(5u);
    sub_401080(Buffer, 0x11u, v23, v32);
    v24 = (BYTE *)sub_4018D0(v33);
    sub_401800(v24, strlen((const char *)v24), (int)v54);
    v40 = 0;
    v25 = (char *)sub_401200(&v40);
    v35 = v25;
    v26 = 0;
    v27 = free;
    while ( 1 )
    {
      v36 = v26;
      if ( v26 >= v40 )
        break;
      v38 = 0;
      cbBinary = 0;
      v37 = (const char **)&v25[4 * v26];
      v28 = strlen(*v37);
      sub_401460(&v38, &cbBinary);
      sub_401D70(v38, cbBinary, (int)&v34);
      v29 = *v37;
      v41[0] = v28;
      v41[1] = v28;
      v41[2] = v29;
      v42[0] = 32;
      v42[1] = 32;
      v42[2] = v54;
      SystemFunction032(v41, v42);
      v30 = v28;
      v31 = (void **)v37;
      sub_401D70((BYTE *)*v37, v30, (int)&v53);
      sub_401000((char)Binding);
      sub_401000((char)Binding);
      v27 = free;
      free(*v31);
      v26 = v36 + 1;
      v25 = v35;
    }
    v27(v25);
    v27((void *)pcchString);
  }
  ms_exc.registration.TryLevel = -2;
  if ( Binding )
    RpcBindingFree(&Binding);
  return 0;
}
```

Briefly look through the main function, we can see that it's calling lots of RPC APIs, so this part require us to use the pcap that the author provided. 

First we're solving the xor sequences

The first xor sequence
```cpp
    *(_BYTE *)v4 = byte_406098 ^ byte_406240;
    *((_BYTE *)v4 + 1) = byte_406241 ^ byte_406099;
    *((_BYTE *)v4 + 2) = byte_406242 ^ byte_40609A;
    *((_BYTE *)v4 + 3) = byte_406243 ^ byte_40609B;
    *((_BYTE *)v4 + 4) = byte_406244 ^ byte_40609C;
    *((_BYTE *)v4 + 5) = byte_406245 ^ byte_40609D;
    *((_BYTE *)v4 + 6) = byte_406246 ^ byte_40609E;
    *((_BYTE *)v4 + 7) = byte_406247 ^ byte_40609F;
    *((_BYTE *)v4 + 8) = byte_406248 ^ byte_4060A0;
    *((_BYTE *)v4 + 9) = byte_406249 ^ byte_4060A1;
``` 
Solves to port "4444"

The Second xor sequence

```cpp
if ( (v6 > (unsigned __int16 *)&unk_4061B7 || v8 < (unsigned int)&xmmword_406198)
      && (v6 > (unsigned __int16 *)&unk_4061D7 || v8 < (unsigned int)&xmmword_4061B8) )
    {
      do
      {
        *(__m128 *)((char *)v6 + v7) = _mm_xor_ps(
                                         *(__m128 *)((char *)&xmmword_4061B8 + v7),
                                         *(__m128 *)((char *)&xmmword_406198 + v7));

```
Solves to the IP "192.168.255.130"

The third xor sequence 
```cpp
if ( v9 )
  {
    v11 = 0;
    v12 = (unsigned int)v9 + 25;
    if ( (v10 > &word_406095 || v12 < (unsigned int)&xmmword_40607C)
      && (v10 > word_406265 || v12 < (unsigned int)&xmmword_40624C) )
    {
      *(__m128 *)v10 = _mm_xor_ps((__m128)xmmword_40607C, (__m128)xmmword_40624C);
      v11 = 16;
    }
```

This solves to a RPC protocal sequence "ncacn_ip_tcp".

The decoded XOR show us that:
```
Protocol: ncacn_ip_tcp
Server:   192.168.255.130
Port:     4444
```

![{E33F7389-CF68-4A8A-8D78-69FA62534990}](https://hackmd.io/_uploads/SJ0ExSKqGg.png)

Cilent send `s3C7GnVNGk+wK6G6RJv8CHzG+p2othA1` to the server then receive `xIUaAqoLDAc=` from server 

Back to the payload, at the begin of `004025F9` the main is calling `sub_402190` 

```cpp
__int64 sub_402190()
{
  HCRYPTPROV v0; // eax
  __int64 v1; // kr00_8
  __int64 pbBuffer; // [esp+10h] [ebp-10h] BYREF

  do
  {
    v0 = hProv;
    if ( !hProv )
    {
      if ( !CryptAcquireContextW(&hProv, 0, 0, 1u, 0xF0000000) )
        goto LABEL_8;
      v0 = hProv;
    }
    if ( !CryptGenRandom(v0, 8u, (BYTE *)&pbBuffer) )
LABEL_8:
      ExitProcess(1u);
    v1 = 2 * (pbBuffer | 0x2000000000000001LL) + 1;
  }
  while ( !sub_401FF0(pbBuffer | 1, HIDWORD(pbBuffer) | 0x20000000) || !sub_401FF0(v1, HIDWORD(v1)) );
  return v1;
}
``` 
Looks like it's generating random number with the `CryptGenRandom` API `CryptGenRandom(v0, 8u, (BYTE *)&pbBuffer)` is filling the pbBuffer with 8 random bytes

After that it goes in `sub_401FF0`, this sub is basically a prime check. It's actually checking 64bits but since the programme is 32bits, it divided to upper 32 and lower 32. BUT there's an API in `sub_401FF0` called `__PAIR64__` that combine those 2 bits then check prime as 64 bits not 32 bits.

Let's summarize what this does:

First given `a = (pbBuffer | 0x2000000000000001LL)`, which mean `v1 = 2* a + 1`. Then `sub_401FF0` will test `a` if it's a prime or not, if passed test `v1` if it's a prime or not if both passes it return v1.

after that 

```asm
.text:004025F9                 call    sub_402190
.text:004025FE                 mov     edi, eax
.text:00402600                 mov     esi, edx
.text:00402602                 mov     [ebp+var_1AC], esi
.text:00402608                 push    esi
.text:00402609                 push    edi
.text:0040260A                 call    sub_402240
```

The result v1 which is 64bits splits into 32bits that stored inside eax and edx, next we're checking `sub_402240`.

```cpp
__int64 __cdecl sub_402240(__int64 a1)
{
  __int64 i; // kr00_8
  HCRYPTPROV v2; // eax
  __int64 v3; // rax
  __int64 v4; // kr08_8
  BYTE pbBuffer[4]; // [esp+10h] [ebp-10h] BYREF
  int v7; // [esp+14h] [ebp-Ch]

  for ( i = a1; ; i = a1 )
  {
    v2 = hProv;
    if ( !hProv )
    {
      if ( !CryptAcquireContextW(&hProv, 0, 0, 1u, 0xF0000000) )
        goto LABEL_10;
      v2 = hProv;
    }
    if ( !CryptGenRandom(v2, 8u, pbBuffer) )
LABEL_10:
      ExitProcess(1u);
    v3 = sub_403770(*(_DWORD *)pbBuffer, v7, (int)i - 3, (unsigned __int64)(i - 3) >> 32);
    v4 = v3 + 2;
    if ( sub_401F40((int)v3 + 2, (unsigned __int64)(v3 + 2) >> 32, 2, 0, a1, HIDWORD(a1)) != 1
      && sub_401F40(
           v4,
           HIDWORD(v4),
           (unsigned __int64)(a1 - 1) >> 1,
           (unsigned int)((unsigned __int64)(a1 - 1) >> 32) >> 1,
           a1,
           HIDWORD(a1)) != 1 )
    {
      break;
    }
  }
  return v4;
}
```

Here `a1` is the value returned by `sub_402190`, the function generate another random number at `if ( !CryptGenRandom(v2, 8u, pbBuffer)`

Next ` v3 = sub_403770(*(_DWORD *)pbBuffer, v7, (int)i - 3, (unsigned __int64)(i - 3) >> 32);` basically doing this (random low, random high, (i−3) low, (i−3) high) 


Onto the next blob

```cpp
 if ( sub_401F40((int)v3 + 2, (unsigned __int64)(v3 + 2) >> 32, 2, 0, a1, HIDWORD(a1)) != 1
      && sub_401F40(
           v4,
           HIDWORD(v4),
           (unsigned __int64)(a1 - 1) >> 1,
           (unsigned int)((unsigned __int64)(a1 - 1) >> 32) >> 1,
           a1,
           HIDWORD(a1)) != 1 )
```

First let's put
```
g = v4
p = a1 (return value)
q = (p - 1) / 2
```
```cpp
if ( sub_401F40((int)v3 + 2, (unsigned __int64)(v3 + 2) >> 32, 2, 0, a1, HIDWORD(a1)) != 1
```



- `(int)v3 + 2, (unsigned __int64)(v3 + 2) >> 32` splits g into low32bits and high32bits.
- 2, 0 is exponent 2 as low half = 2.
- `a1, HIDWORD(a1)) != 1` splits p like g.

Then
```cpp
 (unsigned __int64)(a1 - 1) >> 1,
           (unsigned int)((unsigned __int64)(a1 - 1) >> 32) >> 1,
           a1,
           HIDWORD(a1)) != 1 )
```
That means this is the condition:
```py
if (powmod(g, 2, p) != 1 &&
    powmod(g, q, p) != 1)
```
Calculate g², divide by p, and check that the remainder is not 1.
Calculate g^q, divide by p, and check that the remainder is not 1.
Both must pass to accept g. Otherwise, choose another one.

After going through serveral function we can identify this as Diffie-Hellman technique

The call at `004026A3` (`sub_401F40`) calculates the client’s public value

After `004026A3` returns, the registers hold:
ESI:EDI = p
EDX:EAX = A (return value of `sub_401F40`)

Then

1. Write p into the first eight bytes
```asm
004026AB mov [ebp-178h], edi
004026B1 mov [ebp-174h], esi
```
EDI writes the lower 32 bits of p.
ESI writes the upper 32 bits of p.

2. Write g into the next eight bytes
```asm
004026B7 mov ecx, [ebp-17Ch]
004026BD mov [ebp-170h], ecx
004026C3 mov ecx, [ebp-1A0h]
004026C9 mov [ebp-16Ch], ecx
```
The first pair copies the saved lower half of g, the second copies its upper half.

Write A into the final eight bytes
```asm
004026CF mov [ebp-168h], eax
004026D5 mov [ebp-164h], edx
```
After that it being passed through an input buffer and call the API
```asm
004026E5 lea     eax, [ebp+pcchString]
004026EB push    eax             ; pcchString
004026EC push    0               ; pszString
004026EE push    40000001h       ; dwFlags
004026F3 push    18h             ; cbBinary
004026F5 lea     eax, [ebp+pbBinary]
004026FB push    eax             ; pbBinary
004026FC call    ds:CryptBinaryToStringA
```
This first call calculates the required output size while the second one at `00402731` actually writes the base64 encoded string. Which is that string in pcap that we see.
`s3C7GnVNGk+wK6G6RJv8CHzG+p2othA1`
Now where the Base64 string is sent?
```asm
00402758 lea  eax, [ebp-17Ch]
0040275E push eax
0040275F push esi     ; the string
00402760 push [ebp-180h]
00402766 call sub_401000
```
The string is being pushed to `sub_401000`, which is our RPC cilent wrapper
```cpp
CLIENT_CALL_RETURN __cdecl sub_401000(char a1)
{
  return NdrClientCall2(&pStubDescriptor, byte_404246, &a1);
}
```
After that, the server reply:
```asm
0040276E mov  ecx, [ebp-17Ch]
00402774 test ecx, ecx
00402776 je   00402952
0040277C lea  edx, [ebp-160h]
00402782 call sub_401E10
```
The server reply with `xIUaAqoLDAc=`

We already have p, g, A, and B from the PCAP.
We first calculate the exponent x: `g^x mod p = A`

`s3C7GnVNGk+wK6G6RJv8CHzG+p2othA1` produces 24bytes
```
B3 70 BB 1A 75 4D 1A 4F
B0 2B A1 BA 44 9B FC 08
7C C6 FA 9D A8 B6 10 35
```
And we know the order is p, g, A
```
p = 5699953443745788083;
g = 647563165925714864;
A = 3823756918958769788;
```
x = `1611401790918829382`

Now calculating the secret key with `s = B^x mod p`

s = `134A65F79BEDFCB4` 

Then we trace how it formats the shared secret, combines it with system information, and hashes that string.

The formating call is at `004027DC` in `sub_4018D0`

![{796127F8-F199-43F5-845F-AC555E92EAF9}](https://hackmd.io/_uploads/Ska06m9cfe.png)

The format is being held inside EDX

![image](https://hackmd.io/_uploads/rkkMA795fx.png)
![image](https://hackmd.io/_uploads/SylFgNq9Mx.png)
![image](https://hackmd.io/_uploads/HyntlVc5fx.png)
![image](https://hackmd.io/_uploads/ryBqgN5cfe.png)
![image](https://hackmd.io/_uploads/S1uplEq9Gx.png)
![image](https://hackmd.io/_uploads/SJy1-N9qfx.png)
![image](https://hackmd.io/_uploads/Hkjg-N5qGl.png)
![image](https://hackmd.io/_uploads/Hk2b-NqcMl.png)

### Stage 3 
That means the format is `shared_secret_hex -username @computername -major.minor.build-MAC`

Next it's calling `sub_401800` at `004027FF`

Which is a hashing function, so we're SHA-256 that string to get the key.

`383e0de5f706c1dcd2134a2dd5325495a3bbb37c33943adb9d2ef9a73715cc72`

Next, the `sub_401460` call at `0040287C` is where the sha-256 use as a key. This function encrypts a file using the 32-byte hash as an AES-256 key. For decryption, separate the last 16 bytes as the IV.

We're extracting RCP call ID 4 where client sends that file’s encrypted contents + IV. 
First b64 decode it
```py
import base64

with open("file", "r", encoding="utf-8") as f:
    file_content_string = f.read().strip()

blob = base64.b64decode(file_content_string, validate=True)

with open("decoded.bin", "wb") as f:
    f.write(blob)

print("Saved")

```
```
Ciphertext bytes: 2774256
IV: ac1ddf13f7fe3d3c59f1bde7a9583b27
```

Next is decrypting that file content
```cpp
import base64
import hashlib
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

root = Path(r"")

material = (
    "134A65F79BEDFCB4-TendouKei@LUM1N0U5-N0V4"
    "-10.0.19045-00:0C:29:97:27:1A"
)
key = hashlib.sha256(material.encode("ascii")).digest()

encoded = (root / "pcapb64content").read_bytes()
blob = base64.b64decode(encoded, validate=True)

ciphertext = blob[:-16]
iv = blob[-16:]

padded = AES.new(key, AES.MODE_CBC, iv=iv).decrypt(ciphertext)
plaintext = unpad(padded, AES.block_size)

output = root / "decrypted_file.bin"
output.write_bytes(plaintext)

print("Saved:", output)
```

Our decrypted file is a zip archive 

![{77AAD4E7-46DD-4862-A5E6-EE321C90CCDB}](https://hackmd.io/_uploads/H1ed9V99zx.png)

![{F1CB856C-15A1-4FEA-9D4A-4F98D580251C}](https://hackmd.io/_uploads/B1hK9V5qMl.png)

:sob::sob::sob::sob: :anger: 

Okay, looking back at the payload, at `004028E3` it called `SystemFunction032` which perform RC4 decryption directly on buffer, so we're going to get the original filename. First we extracting call id3, then RC4 uses the same key as AES,

```py
import base64
from Crypto.Cipher import ARC4

key = bytes.fromhex(
    "383e0de5f706c1dcd2134a2dd5325495a3bbb37c33943adb9d2ef9a73715cc72"
)

encoded = (
    "aFddF20wCi+cZPFF0wOCV7IEC3Pr9mgXJbwoOcYbVX/H2Rzxrq5s6NUG2OqPoYvq"
    "pcHkrKb2qJrs6VsOpjNmKqCu/e5I2OYepyjAQ+qDFQ=="
)

ciphertext = base64.b64decode(encoded)
filename = ARC4.new(key).decrypt(ciphertext).decode("utf-8")

print("Original filename:", filename)
```
```
C:\Users\TendouKei\Desktop\251405 Katakiri Rekka & Suzuyu - Girl meets Love.osz
```
And in id4 it's the encrypted content of that file

So we can conclude that
ID 3: victim's filepath that's encrypted with RC4, and encoded with b64.
ID 4: that file's contents that's AES encrypted and b64 encoded.

Then the next filename is at ID 5, which is `C:\Users\TendouKei\Desktop\7z2501-x64.exe` and ID 6 is the encrypted content of that files and so on

We can extract all the file name with this code:
```py
import base64
from pathlib import Path
from Crypto.Cipher import ARC4

from recover_files_from_pcap import requests

key = bytes.fromhex(
    "383e0de5f706c1dcd2134a2dd5325495a3bbb37c33943adb9d2ef9a73715cc72"
)

messages = requests(Path("captured.pcapng"))
next(messages)

with open("filenames.txt", "w", encoding="utf-8") as output:
    for filename_call, encoded_filename in messages:
        content_call, encoded_content = next(messages)

        encrypted = base64.b64decode(encoded_filename, validate=True)
        filename = ARC4.new(key).decrypt(encrypted).decode("utf-8")

        print(filename)
        output.write(filename + "\n")
```

We find a suspicious file
`Filename call 5547, content call 5548: C:\Users\TendouKei\Desktop\KCSC_CTF_2026\final.zip`

We'll just have to repeat the same step of base64 decode and recover the content with AES

To recover the final.zip we will need to get all the fragments of ID 5548 with this script
```py
import base64
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from recover_files_from_pcap import requests

key = bytes.fromhex(
    "383e0de5f706c1dcd2134a2dd5325495a3bbb37c33943adb9d2ef9a73715cc72"
)

for call_id, encoded in requests(Path("captured.pcapng")):
    if call_id != 5548:
        continue

    blob = base64.b64decode(encoded, validate=True)

    ciphertext = blob[:-16]
    iv = blob[-16:]

    plaintext = unpad(
        AES.new(key, AES.MODE_CBC, iv=iv).decrypt(ciphertext),
        16,
    )

    output_path = Path("final_recovered.zip")

    with open(output_path, "wb") as output:
        output.write(plaintext)

    print("Saved:", output_path)

    break
```
We did recovered it but the it required a password

![{C2A7FD25-E37B-4BC2-A07A-4C2516F00579}](https://hackmd.io/_uploads/SJHucccqMe.png)

Then I spot another suspicious file:
`Filename call 41, content call 42: C:\Users\TendouKei\Desktop\secrets.txt`
That's probably where our password is, repeat the same step as we did for ID 4, we got our secret.txt content

```
Name: Tendou Kei
School: Millennium Science School
Club: Super Phenomenon Task Force
Password: Longing's Echo
```

![{D851F7E2-31D8-41D5-8FBA-E3A7C14B0408}](https://hackmd.io/_uploads/r1ZHj5q9zx.png)

This did take years off my life, I'm too lazy to make this thing readable too.



A little bit of yapping ses on the current state of CTF this is probably my last ctf writeup (even tho i've been slacking and not updating much), still why "last" i'll still play ctf sometimes yeah, but not going to be too focused on it (THIS YEAR FLARE-ON WAS SOLVED IN AN HOUR SHARP BY ASTRA-6) of course I DO use AI for my ctf don't get me wrong, the difference is I don't use mcp and just say "get the flag, make no mistake" I used it to study about new techniques and assist me in coding

Me personally i'm not against AI at all, it's amazing, it did helped me a bunch in learning reverse engineer. But it's just no point if you just let your agents do all the work right? CTF is about gaining new knowledge, and deepen your understanding of that specific field. And don't get me started on the competition, it's just pay2win, it's not even fair dropping 100bucks on Claude will guarantee you first place in some CTF competition.

CTFs are losing their credibility as a way to hire talent. You can easily get scammed by someone claiming they won a CTF by clearing challenges that no human could realistically solve in 1 hour, look at flare-on that thing took my senior 7-8days to fully solved? freaking astra-6 did it in an hour :sob:

Reverse engineer have changed too, what used to take months of analysis and struggle can now be done in two Claude sessions. But for us student CTF is a place for us to learn DECAGRAMMATON probably took me 2 weeks to solve with the assist of Chatgpt.

Oh yeah, since people abuse AI too much, challenges author make the challenge impossible to solve as a human just so the competition last a little longer against clankers, pretty sad to see. I'll now get started on analyzing malware and stuff instead, mayb that will be more interesting, no one read my writeup, pointless writing this, i'm just using this to vent because i have no one (discord is `.bachy.` plz teach me malware stuff its supercool).
