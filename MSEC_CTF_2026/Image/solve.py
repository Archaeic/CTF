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
