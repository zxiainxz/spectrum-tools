#! python3

from PIL import Image
from bitarray import bitarray
import argparse, os, sys

# filename
# --mask=filename
# --interleave-mask
# --shifted
# --order=row|zigzag|column
# --output=filename

def CreateImageData(im):
    if im is None:
        return None

    px = im.load()

    # copy each row into a separate bit array as bits
    data = []
    for y in range(0, im.size[1]):
        ba = bitarray()

        for x in range(0, im.size[0]):
            ba.append(px[x, y])

        data.append(ba)

    return data

def OrderRow(data, maskdata):
    output = []

    for s in range(0, len(data)):
        lineoutput = []
        rowdata = data[s]
        if maskdata is not None:
            maskrowdata = maskdata[s]

        for i in range(0, len(rowdata)):
            row = rowdata[i].tobytes()

            if maskdata is not None:
                maskrow = maskrowdata[i].tobytes()

            for j in range(0, len(row)):
                if (maskdata is not None):
                    lineoutput.append(str(maskrow[j]))

                lineoutput.append(str(row[j]))

        output.append(lineoutput)

    return output

def OrderZigZag(data, maskdata, size, args):
    pass

def OrderColumn(data, maskdata, size, vertical):
    output = []

    vpadding = ['0','0','0','0','0','0','0','0']
    if maskdata is not None:
        vpadding = vpadding + vpadding

    for s in range(0, len(data)):

        rowdata = data[s]
        if maskdata is not None:
            maskrowdata = maskdata[s]

        columnCount = int((size[0] + 8) / 8)
        columns = []
        for i in range(0, columnCount):
            columns.append([])

        for i in range(0, len(rowdata)):
            row = rowdata[i].tobytes()

            if maskdata is not None:
                maskrow = maskrowdata[i].tobytes()

            for j in range(0, len(row)):
                if (maskdata is not None):
                    columns[j].append(str(maskrow[j]))
                columns[j].append(str(row[j]))

        lineoutput = []
        if vertical:
            lineoutput = vpadding
        
        i = 0
        for c in columns:
            lineoutput = lineoutput + c
            if vertical and i < columnCount - 1:
                lineoutput = lineoutput + vpadding

            i += 1

        output.append(lineoutput)

    if vertical:
        output.append(vpadding)

    return output

def Shift(data, s):
    shiftedrows = []

    for row in data:
        rowcopy = row.copy()
        rowcopy.extend([0,0,0,0,0,0,0,0])
        shiftedrow = rowcopy >> s

        shiftedrows.append(shiftedrow)

    return shiftedrows

def DisplayResults(data, args):
    base = os.path.basename(args.file)
    label = os.path.splitext(base)[0].replace('-','')

    if args.output is not None:
        originalStdout = sys.stdout
        outputFile = open(args.output, "w")
        sys.stdout = outputFile

    print("; File - " + args.file)
    if args.mask is not None:
        print("; Mask file - " + args.mask)
    print("; Order - " + args.order)
    print("; Shifted - Horizontal: " + str(args.shift) + " | Vertical: " + str(args.vertical_shift))

    for i in range(0, len(data)):
        row = data[i]
        db = ', '.join(row)

        if i == len(data) - 1 and args.vertical_shift:
            print(label + "Padding: db " + db)
        else:
            print(label + "Data" + str(i) + ": db " + db)

    if args.output is not None:
        sys.stdout = originalStdout
        outputFile.close()

def main():
    parser = argparse.ArgumentParser(description='Convert images to binary')
    parser.add_argument('file', metavar='FILE', help='source image')
    parser.add_argument('--mask', help='mask image')
    parser.add_argument('--output', help='output file')
    parser.add_argument('--shift', action='store_true', help='shift the sprite horizontally')
    parser.add_argument('--vertical-shift', action='store_true', help='shift the sprite vertically')
    parser.add_argument('--order', choices=['row', 'zigzag', 'column'], default='row', help='the order the data should be sorted in')

    args = parser.parse_args()

    im = Image.open(args.file)
    size = im.size

    maskim = None
    masksize = None
    if args.mask is not None:
        maskim = Image.open(args.mask)
        masksize = maskim.size

        if masksize != size:
            sys.exit('mask size mismatch')

    imdata = CreateImageData(im)
    maskdata = CreateImageData(maskim)

    shiftedimagedata = []
    shiftedmaskdata = []

    if args.shift:
        for s in range(0, 8):
            shiftedimdata = Shift(imdata, s)
            shiftedimagedata.append(shiftedimdata)

            if maskdata is not None:
                shiftedmdata = Shift(maskdata, s)
                shiftedmaskdata.append(shiftedmdata)
            else:
                shiftedmaskdata = None
    else:
        shiftedimagedata.append(imdata)
        if maskdata is not None:
            shiftedmaskdata.append(maskdata)
        else:
            shiftedmaskdata = None

    output = []
    if args.order == 'row':
        output = OrderRow(shiftedimagedata, shiftedmaskdata)
    elif args.order == 'zigzag':
        OrderZigZag(shiftedimagedata, shiftedmaskdata, size, args)
    elif args.order == 'column':
        output = OrderColumn(shiftedimagedata, shiftedmaskdata, size, args.vertical_shift)
    else:
        sys.exit('unknown order')

    DisplayResults(output, args)

if __name__ == "__main__":
    main()
