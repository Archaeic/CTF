# MSEC CTF

## ez_enc

There are 27 exes in this challenge.

Checking out the first one
```cpp
int __fastcall main(int argc, const char **argv, const char **envp)
{
  unsigned __int64 v3; // rax
  __int64 v4; // rcx
  const char *v5; // rcx
  __int64 v7; // [rsp+20h] [rbp-28h] BYREF
  __int16 v8; // [rsp+28h] [rbp-20h]

  v7 = 0;
  v8 = 0;
  printf("password: ");
  sub_140001064("%8s", (const char *)&v7);
  v3 = -1i64;
  v4 = 0i64;
  do
    ++v3;
  while ( *((_BYTE *)&v7 + v3) );
  if ( v3 <= 8 )
  {
    do
    {
      *((_BYTE *)&v7 + v4) ^= byte_140028A80[v4];
      ++v4;
    }
    while ( v4 < 8 );
    v5 = "Correct\n";
    if ( v7 != qword_140028A88 )
      v5 = "Wrong\n";
    printf(v5, "Wrong\n");
  }
  else
  {
    printf("Wrong\n");
  }
  return 0;
}
```
The XOR is at `byte_140028A80` and checks at `qword_140028A88` 

```py
xor_key = [ 0x47, 0x7C, 0x21, 0x69, 0x74, 0x5C, 0x20, 0x56 ]
expected = [ 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11]

password = bytes([expected[i] ^ xor_key[i] for i in range(8)])
print(password.decode())
```

Repeat the same thing for other file we got this base64

```
Vm0weM1GbFdiRmRWV0doVVltczFWRll3YUVOamJGWnpWbTVrV0ZKc2NIbFhhMXBQVkcxS1IyTkZhRmRpV0ZKeVZtcEdZV05yTlZkYVJsWk9WbXhWZUZacVJsWmxSMUpJVm10V1dHSkhhRlJWYkZKWFZsWmtXR05GWkZSTlZtd3pWREZhWVdKR1NsVldhemxYWVdzMWNWUldSVGxRVVQwOQ==
```
![{C7152E49-4A51-42A4-A4DC-5782177D9AD3}](https://hackmd.io/_uploads/r1-85cRnbg.png)

## me_enc
Same as 'ez_enc'
```cpp
int __fastcall main(int argc, const char **argv, const char **envp)
{
  unsigned __int64 v3; // rax
  HMODULE ModuleHandleA; // rax
  FARPROC SystemFunction033; // rax
  int v6; // eax
  const char *v7; // rcx
  int v9; // [rsp+20h] [rbp-40h] BYREF
  void *v10; // [rsp+28h] [rbp-38h]
  int v11; // [rsp+30h] [rbp-30h] BYREF
  __int64 *p_Buf1; // [rsp+38h] [rbp-28h]
  __int64 Buf1; // [rsp+40h] [rbp-20h] BYREF
  __int16 v14; // [rsp+48h] [rbp-18h]

  Buf1 = 0;
  v14 = 0;
  printf("password: ");
  sub_140001064("%8s", (const char *)&Buf1);
  v3 = -1;
  do
    ++v3;
  while ( *((_BYTE *)&Buf1 + v3) );
  if ( v3 <= 8 )
  {
    ModuleHandleA = GetModuleHandleA("advapi32");
    if ( !ModuleHandleA )
      ModuleHandleA = LoadLibraryA("advapi32");
    SystemFunction033 = GetProcAddress(ModuleHandleA, "SystemFunction033");
    if ( SystemFunction033 )
    {
      v9 = 8;
      v10 = &key;
      v11 = 8;
      p_Buf1 = &Buf1;
      ((void (__fastcall *)(int *, int *))SystemFunction033)(&v11, &v9);
    }
    v6 = memcmp(&Buf1, &input, 8u);
    v7 = "Correct\n";
    if ( v6 )
      v7 = "Wrong\n";
    printf(v7);
  }
  else
  {
    printf("Wrong\n");
  }
  return 0;
}
```

RC4 

![{BDB80453-E320-4A4E-989D-B5A70E7868B1}](https://hackmd.io/_uploads/HJmpi50nZx.png)

In the 5th file we got TEA

```cpp
int __fastcall main(int argc, const char **argv, const char **envp)
{
  unsigned __int64 v3; // rax
  int v4; // r9d
  unsigned int v5; // edx
  __int64 v6; // rbx
  unsigned int v7; // r8d
  const char *v8; // rcx
  unsigned __int64 v10; // [rsp+20h] [rbp-28h] BYREF
  __int16 v11; // [rsp+28h] [rbp-20h]

  v10 = 0;
  v11 = 0;
  printf("password: ");
  sub_140001064("%8s", (const char *)&v10);
  v3 = -1;
  v4 = 0;
  do
    ++v3;
  while ( *((_BYTE *)&v10 + v3) );
  if ( v3 <= 8 )
  {
    v5 = v10;
    v6 = 32;
    v7 = HIDWORD(v10);
    do
    {
      v4 -= 1640531527;
      v5 += (v4 + v7) ^ (dword_140028A80 + 16 * v7) ^ (dword_140028A84 + (v7 >> 5));
      v7 += (v4 + v5) ^ (dword_140028A84 + (v5 >> 5)) ^ (dword_140028A80 + 16 * v5);
      --v6;
    }
    while ( v6 );
    v10 = __PAIR64__(v7, v5);
    v8 = "Correct\n";
    if ( __PAIR64__(v7, v5) != qword_140028A88 )
      v8 = "Wrong\n";
    printf(v8);
  }
  else
  {
    printf("Wrong\n");
  }
  return 0;
}
```

```py
import struct

DELTA = 0x9E3779B9
ROUNDS = 32

k0 = 0x81D19285  # dword_140028A80
k1 = 0x417EDE32  # dword_140028A84
target = 0x40ECCF2BE2ACA3FC  # qword_140028A88

def tea_decrypt(v0, v1):
    sum_ = (DELTA * ROUNDS) & 0xFFFFFFFF

    for _ in range(ROUNDS):
        v1 = (v1 - ((v0 + sum_) ^ (k1 + (v0 >> 5)) ^ (k0 + (v0 << 4)))) & 0xFFFFFFFF
        v0 = (v0 - ((v1 + sum_) ^ (k0 + (v1 << 4)) ^ (k1 + (v1 >> 5)))) & 0xFFFFFFFF
        sum_ = (sum_ - DELTA) & 0xFFFFFFFF

    return v0, v1

v0 = target & 0xFFFFFFFF
v1 = (target >> 32) & 0xFFFFFFFF
p0, p1 = tea_decrypt(v0, v1)

password = struct.pack("<II", p0, p1)
print(password.decode())

# YUVOamJG
```
I've come to the conclusion that `ez_enc` and `me_enc` have the same password, not going any further.

![{C7152E49-4A51-42A4-A4DC-5782177D9AD3}](https://hackmd.io/_uploads/r1-85cRnbg.png)

## Image
Main:
```cpp
LRESULT __stdcall sub_401130(HWND hWnd, UINT Msg, WPARAM wParam, unsigned int lParam)
{
  HDC v4; // eax
  HGDIOBJ v6; // eax
  HDC DC; // esi
  void *v8; // esi
  HRSRC ResourceA; // eax
  HGLOBAL Resource; // eax
  _BYTE *v11; // eax
  int v12; // edi
  _BYTE *v13; // ecx
  int v14; // eax
  _BYTE pv[4]; // [esp+8h] [ebp-80h] BYREF
  LONG v16; // [esp+Ch] [ebp-7Ch]
  UINT cLines; // [esp+10h] [ebp-78h]
  tagBITMAPINFO bmi; // [esp+20h] [ebp-68h] BYREF

  if ( Msg <= 0x111 )
  {
    if ( Msg != 273 )
    {
      switch ( Msg )
      {
        case 1u:
          DC = GetDC(hWnd);
          hbm = CreateCompatibleBitmap(DC, 200, 150);
          hdc = CreateCompatibleDC(DC);
          h = SelectObject(hdc, hbm);
          Rectangle(hdc, -5, -5, 205, 205);
          ReleaseDC(hWnd, DC);
          ::wParam = (WPARAM)CreateFontA(12, 0, 0, 0, 400, 0, 0, 0, 0x81u, 0, 0, 0, 0x12u, pszFaceName);
          dword_4084E0 = (int)CreateWindowExA(
                                0,
                                ClassName,
                                WindowName,
                                0x50000000u,
                                60,
                                85,
                                80,
                                28,
                                hWnd,
                                (HMENU)0x64,
                                hInstance,
                                0);
          SendMessageA((HWND)dword_4084E0, 0x30u, ::wParam, 0);
          return 0;
        case 2u:
          v6 = SelectObject(hdc, h);
          DeleteObject(v6);
          DeleteDC(hdc);
          PostQuitMessage(0);
          return 0;
        case 0xFu:
          v4 = BeginPaint(hWnd, (LPPAINTSTRUCT)bmi.bmiColors);
          BitBlt(v4, 0, 0, 200, 150, hdc, 0, 0, 0xCC0020u);
          EndPaint(hWnd, (const PAINTSTRUCT *)bmi.bmiColors);
          return 0;
      }
      return DefWindowProcA(hWnd, Msg, wParam, lParam);
    }
    if ( wParam == 100 )
    {
      GetObjectA(hbm, 24, pv);
      memset(&bmi, 0, 0x28u);
      bmi.bmiHeader.biHeight = cLines;
      bmi.bmiHeader.biWidth = v16;
      bmi.bmiHeader.biSize = 40;
      bmi.bmiHeader.biPlanes = 1;
      bmi.bmiHeader.biBitCount = 24;
      bmi.bmiHeader.biCompression = 0;
      GetDIBits(hdc, (HBITMAP)hbm, 0, cLines, 0, &bmi, 0);
      v8 = operator new(bmi.bmiHeader.biSizeImage);
      GetDIBits(hdc, (HBITMAP)hbm, 0, cLines, v8, &bmi, 0);
      ResourceA = FindResourceA(0, (LPCSTR)0x65, (LPCSTR)0x18);
      Resource = LoadResource(0, ResourceA);
      v11 = LockResource(Resource);
      v12 = 0;
      v13 = v8;
      v14 = v11 - (_BYTE *)v8;
      while ( *v13 == v13[v14] )
      {
        ++v12;
        ++v13;
        if ( v12 >= 90000 )
        {
          sub_401500(v8);
          return 0;
        }
      }
      MessageBoxA(hWnd, Text, Caption, 0x30u);
      sub_401500(v8);
      return 0;
    }
    return 0;
  }
  switch ( Msg )
  {
    case 0x200u:
      if ( dword_47D7F8 )
      {
        MoveToEx(hdc, x, y, 0);
        LineTo(hdc, (unsigned __int16)lParam, HIWORD(lParam));
        x = (unsigned __int16)lParam;
        y = HIWORD(lParam);
        InvalidateRect(hWnd, 0, 0);
      }
      return 0;
    case 0x201u:
      dword_47D7F8 = 1;
      y = HIWORD(lParam);
      x = (unsigned __int16)lParam;
      return 0;
    case 0x202u:
      dword_47D7F8 = 0;
      return 0;
    default:
      return DefWindowProcA(hWnd, Msg, wParam, lParam);
  }
}
```

Basically extract 90000 bytes to get the BMP 

```py
import struct, os  

path = r"C:\Users\Admin\Desktop\MSEC_CTF_2026\Image\ImagePrc.exe" 

with open(path, 'rb') as f:
    f.seek(0x9060)           
    raw = f.read(90000)      # read 90000 bytes

# Build bmp header 
header = (
    b'BM' +                                  
    struct.pack('<I', 54+90000) +             # Header (54) + pixel data (90000)
    b'\x00\x00\x00\x00' +                     #
    struct.pack('<I', 54) +                   # Offset 

    struct.pack('<IiiHHIIiiII',              
        40,        # biSize
        200,       # biWidth
        150,       # biHeight
        1,         # biPlanes
        24,        # biBitCount
        0,         # biCompression
        90000,     # biSizeImage
        2835,      # biXPelsPerMeter
        2835,      # biYPelsPerMeter
        0,         # biClrUsed
        0          # biClrImportant
    )
)

with open('IMG.bmp', 'wb') as f:  
    f.write(header + raw)            
```

![{3E254987-5761-48D5-83BA-8331E5BBD0FB}](https://hackmd.io/_uploads/HkgITj03bx.png)



## smile

![{7E15B24E-F60F-49AD-9104-EE2217B46FF1}](https://hackmd.io/_uploads/H19haq03bg.png)

Unpack it with UPX.

`a1` is our input so we got this key

![{8C137D9B-4F21-4A17-BDC9-41EC17DE22B8}](https://hackmd.io/_uploads/HyYTej03Wx.png)

`HOH.HOH.CCO.c1ccc(O)cc1.CCNC`

`Password check`
```cpp
unsigned __int64 __fastcall run_password_checker(__int64 a1)
{
  int v2; // [rsp+1Ch] [rbp-404h]
  char *s1; // [rsp+20h] [rbp-400h]
  char s[1000]; // [rsp+30h] [rbp-3F0h] BYREF
  unsigned __int64 v5; // [rsp+418h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  puts("=================================================================");
  puts("                    MEDVEDEV WORLD'S BEST ENCRYPTION SYSTEM");
  puts("=================================================================");
  printf("Enter your password: ");
  getchar();
  fgets(s, 1000, _bss_start);
  v2 = strlen(s);
  if ( v2 > 0 && s[v2 - 1] == 10 )
    s[v2 - 1] = 0;
  if ( s[0] )
  {
    s1 = (char *)encode_message(s, a1);
    puts("Verifying password...");
    if ( !strcmp(
            s1,
            "C=C.Sc1ccccc1.c1ccc(C)cc1.CC(C)F.C.CCOC.C1CCCC1.CC(C)S.Cc1ccccc1.CC(=O)C.c1ccc(S)cc1.C1CCCC1.c1ccc(S)cc1.BrC"
            "Br.CC(C)S.C1CCCCCS1.C1CCCO1.c1ccc(S)cc1.C=CF.c1ccc(C#C)cc1.CC(C)(C)N.C1CCCC1.CCOC.c1ccc(C#C)cc1.c1ccc(CC)cc1"
            ".c1ccc(S)cc1.BrF.OCc1ccccc1.c1ccc(S)cc1.C=CF.c1ccc(C#C)cc1.HOH.Cc1ccccc1.c1ccc(S)cc1.CCCCS.c1ccc(C#C)cc1.CC("
            "C)S.C1CCO1.HOH.Cc1ccccc1.c1ccc(CC)cc1.CF.Nc1ccccc1.c1ccc(S)cc1.CC(C)S.BrCBr.CCCCS.CF.Nc1ccccc1.N.c1ccc(CC)cc"
            "1.HOH.CC(C)(C)N.BrCBr.OO") )
    {
      puts("\n=================================================================");
      puts("                    VERIFICATION SUCCESS!");
      puts("=================================================================");
      puts("CORRECT!");
      puts("Access granted to Dr. Medvedev's secret research!");
      puts("Dont worry guys, I just went to Hawaii for a vacation, sorry for let you guys unknown about this :> \n");
      puts("I will bring some presents for all of youuu.\n");
    }
    else
    {
      puts("\n=================================================================");
      puts("                    VERIFICATION FAILED");
      puts("=================================================================");
      puts("INCORRECT!");
      puts("Access denied. The molecular structure doesn't match.");
      puts("Dr. Medvedev's secrets remain hidden...\n");
    }
    free(s1);
  }
  else
  {
    puts("Error: No password entered.");
  }
  return __readfsqword(0x28u) ^ v5;
}
```

The programme checks the input after encoded with 
 ```
"C=C.Sc1ccccc1.c1ccc(C)cc1.CC(C)F.C.CCOC.C1CCCC1.CC(C)S.Cc1ccccc1.CC(=O)C.c1ccc(S)cc1.C1CCCC1.c1ccc(S)cc1.BrC"
            "Br.CC(C)S.C1CCCCCS1.C1CCCO1.c1ccc(S)cc1.C=CF.c1ccc(C#C)cc1.CC(C)(C)N.C1CCCC1.CCOC.c1ccc(C#C)cc1.c1ccc(CC)cc1"
            ".c1ccc(S)cc1.BrF.OCc1ccccc1.c1ccc(S)cc1.C=CF.c1ccc(C#C)cc1.HOH.Cc1ccccc1.c1ccc(S)cc1.CCCCS.c1ccc(C#C)cc1.CC("
            "C)S.C1CCO1.HOH.Cc1ccccc1.c1ccc(CC)cc1.CF.Nc1ccccc1.c1ccc(S)cc1.CC(C)S.BrCBr.CCCCS.CF.Nc1ccccc1.N.c1ccc(CC)cc"
            "1.HOH.CC(C)(C)N.BrCBr.OO"
```

`Encoded_message`
```cpp
char *__fastcall encode_message(const char *a1, __int64 a2)
{
  char v3; // [rsp+1Fh] [rbp-431h]
  int i; // [rsp+20h] [rbp-430h]
  int j; // [rsp+24h] [rbp-42Ch]
  int v6; // [rsp+28h] [rbp-428h]
  char *dest; // [rsp+30h] [rbp-420h]
  char *src; // [rsp+38h] [rbp-418h]
  _DWORD v9[258]; // [rsp+40h] [rbp-410h] BYREF
  unsigned __int64 v10; // [rsp+448h] [rbp-8h]

  v10 = __readfsqword(0x28u);
  create_permutation(a2, v9);
  for ( i = 0; i <= 127; ++i )
    v9[v9[i] + 128] = i;
  v6 = strlen(a1);
  dest = (char *)malloc(50 * v6);
  *dest = 0;
  for ( j = 0; j < v6; ++j )
  {
    v3 = a1[j];
    if ( v3 < 0 )
      v3 = 42;
    src = (char *)*(&MOLECULE_DB + (int)v9[(unsigned __int8)v3 + 128]);
    if ( j > 0 )
      *(_WORD *)&dest[strlen(dest)] = 46;
    strcat(dest, src);
  }
  return dest;
}
```

`create_permutation`
```cpp
__int64 __fastcall create_permutation(__int64 a1, __int64 a2)
{
  __int64 result; // rax
  int i; // [rsp+1Ch] [rbp-14h]
  unsigned int v4; // [rsp+20h] [rbp-10h]
  int j; // [rsp+24h] [rbp-Ch]
  unsigned int v6; // [rsp+2Ch] [rbp-4h]

  for ( i = 0; i <= 127; ++i )
    *(_DWORD *)(a2 + 4LL * i) = i;
  result = hash_molecular_key(a1);
  v4 = result;
  for ( j = 127; j > 0; --j )
  {
    v4 = 16807 * v4
       - 0x7FFFFFFF
       * ((unsigned __int64)((((unsigned __int64)&unk_200000005 * (unsigned __int128)(16807 * (unsigned __int64)v4)) >> 64)
                           + ((unsigned __int64)(16807LL * v4
                                               - (((unsigned __int64)&unk_200000005
                                                 * (unsigned __int128)(16807 * (unsigned __int64)v4)) >> 64)) >> 1)) >> 30);
    v6 = *(_DWORD *)(4LL * j + a2);
    *(_DWORD *)(4LL * j + a2) = *(_DWORD *)(4LL * (int)(v4 % (j + 1)) + a2);
    result = v6;
    *(_DWORD *)(a2 + 4LL * (int)(v4 % (j + 1))) = v6;
  }
  return result;
}
```
It's using Fisher Yates shuffle  algorithm

Solve
```py
MOLECULE_DB = [
    "C","CC","CCC","O","CO","CCO","N","CN","CCN","S","CS","CCS",
    "F","CF","CCF","Cl","CCl","CCCl","Br","CBr","HOH","OO","OCO",
    "c1ccccc1","Cc1ccccc1","OCc1ccccc1","Nc1ccccc1","Sc1ccccc1",
    "c1ccc(C)cc1","c1ccc(O)cc1","c1ccc(N)cc1","c1ccc(S)cc1","c1ccc(F)cc1",
    "CC(C)C","CC(C)O","CC(C)N","CC(C)S","CC(C)F",
    "CCCC","CCCCO","CCCCN","CCCCS","CCCCF",
    "C1CC1","C1CCO1","C1CCN1","C1CCS1","C1CCF1",
    "C=C","C=CO","C=CN","C=CS","C=CF",
    "C#C","C#CO","C#CN","C#CS","C#CF",
    "c1ccncc1","c1ccnc(C)c1","c1ccnc(O)c1","c1ccnc(N)c1","c1ccnc(S)c1",
    "CC=C","CCC=C","CCCC=C","CCCCC=C","CCCCCC=C",
    "c1cccnc1","c1ccc(C=C)cc1","c1ccc(C#C)cc1","c1ccc(CC)cc1","c1ccc(CCC)cc1",
    "COC","CCOC","CCCOC","CCCCOC","CCCCCOC",
    "CNC","CCNC","CCCNC","CCCCNC","CCCCCNC",
    "CSC","CCSC","CCCSC","CCCCSC","CCCCCSC",
    "CFC","CCFC","CCCFC","CCCCFC","CCCCCFC",
    "ClCCl","BrCBr","ICl","ClF","BrF",
    "c1ccc2ccccc2c1","c1ccc2cc(C)ccc2c1","c1ccc2cc(O)ccc2c1",
    "c1ccc2cc(N)ccc2c1","c1ccc2cc(S)ccc2c1",
    "CC(C)(C)C","CC(C)(C)O","CC(C)(C)N","CC(C)(C)S","CC(C)(C)F",
    "C1CCC1","C1CCCO1","C1CCCN1","C1CCCS1","C1CCCF1",
    "C1CCCC1","C1CCCCO1","C1CCCCN1","C1CCCCS1","C1CCCCF1",
    "C1CCCCC1","C1CCCCCO1","C1CCCCCN1","C1CCCCCS1","C1CCCCCF1",
    "c1ccc(C(C)C)cc1","c1ccc(C(C)O)cc1","c1ccc(C(C)N)cc1",
    "CC(=O)C","CC(=O)O",
]
smiles_to_idx = {s: i for i, s in enumerate(MOLECULE_DB)}

def hash_molecular_key(s):
    h = 0
    for c in s.encode():
        h = (31 * h + c) & 0xFFFFFFFF
    return h & 0x7FFFFFFF

MOD = 0x7FFFFFFF
def lcg_next(v):
    return (16807 * v) % MOD

def create_permutation(seed):
    perm = list(range(128))
    v4 = seed
    for j in range(127, 0, -1):
        v4 = lcg_next(v4)
        swap_idx = v4 % (j + 1)
        perm[j], perm[swap_idx] = perm[swap_idx], perm[j]
    return perm

TARGET = ("C=C.Sc1ccccc1.c1ccc(C)cc1.CC(C)F.C.CCOC.C1CCCC1.CC(C)S.Cc1ccccc1.CC(=O)C."
          "c1ccc(S)cc1.C1CCCC1.c1ccc(S)cc1.BrCBr.CC(C)S.C1CCCCCS1.C1CCCO1.c1ccc(S)cc1."
          "C=CF.c1ccc(C#C)cc1.CC(C)(C)N.C1CCCC1.CCOC.c1ccc(C#C)cc1.c1ccc(CC)cc1.c1ccc(S)cc1."
          "BrF.OCc1ccccc1.c1ccc(S)cc1.C=CF.c1ccc(C#C)cc1.HOH.Cc1ccccc1.c1ccc(S)cc1.CCCCS."
          "c1ccc(C#C)cc1.CC(C)S.C1CCO1.HOH.Cc1ccccc1.c1ccc(CC)cc1.CF.Nc1ccccc1.c1ccc(S)cc1."
          "CC(C)S.BrCBr.CCCCS.CF.Nc1ccccc1.N.c1ccc(CC)cc1.HOH.CC(C)(C)N.BrCBr.OO")

tokens = TARGET.split('.')
mol_indices = [smiles_to_idx[t] for t in tokens]

KEY = "HOH.HOH.CCO.c1ccc(O)cc1.CCNC"
seed = hash_molecular_key(KEY)

perm = create_permutation(seed)
inv = [0] * 128
for i in range(128):
    inv[perm[i]] = i

password = ''.join(chr(perm[m]) for m in mol_indices)

print(password)
```

![{D87B3674-85C4-4005-AF08-E2D56792FBE5}](https://hackmd.io/_uploads/SJV0FjRn-l.png)







