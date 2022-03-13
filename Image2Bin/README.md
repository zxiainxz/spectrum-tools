# Image2Bin.py

Image2Bin.py converts images to a binary representation suitable for inclusion in a z80 code file. It is designed for ZX Spectrum sprites and handles various layout orders (row, column, zigzag) and preshifting both horizontally and vertically.

Requires Python 3 and uses Pillow and Bitarray

```
% ./Image2Bin.py --help
usage: Image2Bin.py [-h] [--mask MASK] [--output OUTPUT] [--shift] [--vertical-shift] [--order {row,zigzag,column}] FILE

Convert images to binary

positional arguments:
  FILE                  source image

optional arguments:
  -h, --help            show this help message and exit
  --mask MASK           mask image
  --output OUTPUT       output file
  --shift               shift the sprite horizontally
  --vertical-shift      shift the sprite vertically
  --order {row,zigzag,column}
                        the order the data should be sorted in
```

```
% ./Image2Bin.py ./test.gif
; File - ./test.gif
; Order - row
; Shifted - Horizontal: False | Vertical: False
testPadding: db 255, 1, 2, 4, 8, 16, 32, 64
```

```
% ./Image2Bin.py --shift ./test.gif       
; File - ./test.gif
; Order - row
; Shifted - Horizontal: True | Vertical: False
testData0: db 255, 0, 1, 0, 2, 0, 4, 0, 8, 0, 16, 0, 32, 0, 64, 0
testData1: db 127, 128, 0, 128, 1, 0, 2, 0, 4, 0, 8, 0, 16, 0, 32, 0
testData2: db 63, 192, 0, 64, 0, 128, 1, 0, 2, 0, 4, 0, 8, 0, 16, 0
testData3: db 31, 224, 0, 32, 0, 64, 0, 128, 1, 0, 2, 0, 4, 0, 8, 0
testData4: db 15, 240, 0, 16, 0, 32, 0, 64, 0, 128, 1, 0, 2, 0, 4, 0
testData5: db 7, 248, 0, 8, 0, 16, 0, 32, 0, 64, 0, 128, 1, 0, 2, 0
testData6: db 3, 252, 0, 4, 0, 8, 0, 16, 0, 32, 0, 64, 0, 128, 1, 0
testPadding: db 1, 254, 0, 2, 0, 4, 0, 8, 0, 16, 0, 32, 0, 64, 0, 128
```

```
% ./Image2Bin.py --shift --order=column ./test.gif
; File - ./test.gif
; Order - column
; Shifted - Horizontal: True | Vertical: False
testData0: db 255, 1, 2, 4, 8, 16, 32, 64, 0, 0, 0, 0, 0, 0, 0, 0
testData1: db 127, 0, 1, 2, 4, 8, 16, 32, 128, 128, 0, 0, 0, 0, 0, 0
testData2: db 63, 0, 0, 1, 2, 4, 8, 16, 192, 64, 128, 0, 0, 0, 0, 0
testData3: db 31, 0, 0, 0, 1, 2, 4, 8, 224, 32, 64, 128, 0, 0, 0, 0
testData4: db 15, 0, 0, 0, 0, 1, 2, 4, 240, 16, 32, 64, 128, 0, 0, 0
testData5: db 7, 0, 0, 0, 0, 0, 1, 2, 248, 8, 16, 32, 64, 128, 0, 0
testData6: db 3, 0, 0, 0, 0, 0, 0, 1, 252, 4, 8, 16, 32, 64, 128, 0
testPadding: db 1, 0, 0, 0, 0, 0, 0, 0, 254, 2, 4, 8, 16, 32, 64, 128
```

```
% ./Image2Bin.py --shift --order=column --vertical-shift ./test.gif
; File - ./test.gif
; Order - column
; Shifted - Horizontal: True | Vertical: True
testData0: db 0, 0, 0, 0, 0, 0, 0, 0, 255, 1, 2, 4, 8, 16, 32, 64, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
testData1: db 0, 0, 0, 0, 0, 0, 0, 0, 127, 0, 1, 2, 4, 8, 16, 32, 0, 0, 0, 0, 0, 0, 0, 0, 128, 128, 0, 0, 0, 0, 0, 0
testData2: db 0, 0, 0, 0, 0, 0, 0, 0, 63, 0, 0, 1, 2, 4, 8, 16, 0, 0, 0, 0, 0, 0, 0, 0, 192, 64, 128, 0, 0, 0, 0, 0
testData3: db 0, 0, 0, 0, 0, 0, 0, 0, 31, 0, 0, 0, 1, 2, 4, 8, 0, 0, 0, 0, 0, 0, 0, 0, 224, 32, 64, 128, 0, 0, 0, 0
testData4: db 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 1, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 240, 16, 32, 64, 128, 0, 0, 0
testData5: db 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 248, 8, 16, 32, 64, 128, 0, 0
testData6: db 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 252, 4, 8, 16, 32, 64, 128, 0
testData7: db 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 254, 2, 4, 8, 16, 32, 64, 128
testPadding: db 0, 0, 0, 0, 0, 0, 0, 0
```


