import re
from dictsToUse import someDicts

#Creator: Kuroyuki Kaze, @kuroyuki_kaze (Twitter)
#Version: 1.0
#Licensing: GPLv3

#For any functions beside createQR, use with care.

class LengthError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

def printQR(qr: list) -> None:
    """Prints the QR code from a binary string."""

    for i in range(21):
        for j in range(21):
            if qr[i][j] == 1:
                print("⬛", end="")
            else:
                print("⬜", end="")
        print("\n", end="")

def mask(b: int) -> int:
    """Apply Mask."""

    if b == 0:
        return 1
    else:
        return 0

def createErrorCorrectionH(message: str) -> str:
    """Create the Error Correction level H for a message binary string."""
    msgPoly: dict = {}
    genPoly: dict = {}
    count: int = 0

    genExpo: list = [0, 43, 139, 206, 78, 43, 239, 123, 206, 214, 147, 24, 99, 150, 39, 243, 163, 136]

    pat = r"(........)"

    founds = re.finditer(pat, message)

    for idx, found in enumerate(founds):
        msgPoly[25 - idx] = tuple(["dec", int(found.group(0), 2)])

    neededCount: int = len(msgPoly)
    
    for idx in range(16, -1, -1):
        msgPoly[idx] = tuple(["dec", 0])

    for idx, val in enumerate(genExpo):
        genPoly[17 - idx] = tuple(["alpha", val])

    while count < neededCount:
        newPoly: dict = {}

        modGenPoly: dict = {}
        for key in genPoly.keys():
            modGenPoly[key + 8 - count] = genPoly[key]
        
        #print("modGenPoly count {count}".format(count=count), modGenPoly, "\n\n")

        maxKey: int = max([key for key in msgPoly.keys()])
        alphaExponent: int = someDicts.decToAlphaTable[msgPoly[maxKey][1]]

        for key in modGenPoly.keys():
            newPoly[key] = tuple(["dec", someDicts.alphaToDecTable[(modGenPoly[key][1] + alphaExponent) % 255]])

        #print("newPoly count {count}".format(count=count), newPoly, "\n")
        #print("msgPoly count {count}".format(count=count), msgPoly, "\n\n")

        for key in newPoly.keys():
            newPoly[key] = tuple(["dec", newPoly[key][1] ^ msgPoly[key][1]])

        #print("newPoly after XOR count {count}".format(count=count), newPoly, "\n\n")
        
        maxKey: int = max([key for key in newPoly.keys()])
        del newPoly[maxKey]
        count += 1

        while True:
            maxKey: int = max([key for key in newPoly.keys()])
            if (newPoly[maxKey][1] == 0):
                del newPoly[maxKey]
                count += 1
            else:
                break
        
        msgPoly = newPoly.copy()
        minKey: int = min([key for key in msgPoly.keys()])
        for idx in range(minKey-1, -1, -1):
            msgPoly[idx] = tuple(["dec", 0])

    while max([key for key in msgPoly.keys()]) < 17:
        maxKey: int = max([key for key in msgPoly.keys()])
        msgPoly[maxKey + 1] = tuple(["dec", 0])

    sortedMsgPoly = sorted(msgPoly.items(), key=lambda x: x[0], reverse=True)

    return [i[1][1] for i in sortedMsgPoly][1:]

def createQR(message: str) -> list:
    """Creates a QR binary string from a message of no longer than 7 charcters."""

    messageString: str = "0100"

    messageLength: int = len(message)

    if (len(message) > 7):
        raise LengthError("The length of the message is too long. (more than 7 chars)")
    
    mlb: str = bin(messageLength)[2:].zfill(8)
    
    messageString += mlb

    for char in message:
        charBin: str = bin(ord(char))[2:].zfill(8)
        messageString += charBin

    mSLength: int = len(messageString)

    if (mSLength == 72):
        pass
    elif (mSLength == 71):
        messageString += "0"
    elif (mSLength == 70):
        messageString += "00"
    elif (mSLength == 69):
        messageString += "000"
    else:
        messageString += "0000"

    mSLength = len(messageString)
    
    while (mSLength < 72):
        messageString += "11101100"
        mSLength = len(messageString)
        if (mSLength < 72):
            messageString += "00010001"
            mSLength = len(messageString)

    errorCorrection: list = createErrorCorrectionH(messageString)

    for num in errorCorrection:
        messageString += bin(num)[2:].zfill(8)
    
    m: str = messageString 
    
    qr: list = [
        [1, 1, 1, 1, 1, 1, 1, 0, 1, m[137], m[136], m[135], m[134], 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, m[139], m[138], m[133], m[132], 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, m[141], m[140], m[131], m[130], 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, m[143], m[142], m[129], m[128], 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, m[145], m[144], m[127], m[126], 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, m[147], m[146], m[125], m[124], 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1,      0,      1,      0,      1, 0, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, m[149], m[148], m[123], m[122], 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 1, 1, 0, 1, m[151], m[150], m[121], m[120], 1, 0, 0, 0, 1, 0, 0, 1],
        [m[201], m[200], m[199], m[198], m[185], m[184], 0, m[183], m[182], m[153], m[152], m[119], m[118],  m[73], m[72], m[71], m[70], m[25], m[24], m[23], m[22]],
        [m[203], m[202], m[197], m[196], m[187], m[186], 1, m[181], m[180], m[155], m[154], m[117], m[116],  m[75], m[74], m[69], m[68], m[27], m[26], m[21], m[20]],
        [m[205], m[204], m[195], m[194], m[189], m[188], 0, m[179], m[178], m[157], m[156], m[115], m[114],  m[77], m[76], m[67], m[66], m[29], m[28], m[19], m[18]],
        [m[207], m[206], m[193], m[192], m[191], m[190], 1, m[177], m[176], m[159], m[158], m[113], m[112],  m[79], m[78], m[65], m[64], m[31], m[30], m[17], m[16]],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, m[161], m[160], m[111], m[110],  m[81], m[80], m[63], m[62], m[33], m[32], m[15], m[14]],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, m[163], m[162], m[109], m[108],  m[83], m[82], m[61], m[60], m[35], m[34], m[13], m[12]],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, m[165], m[164], m[107], m[106],  m[85], m[84], m[59], m[58], m[37], m[36], m[11], m[10]],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, m[167], m[166], m[105], m[104],  m[87], m[86], m[57], m[56], m[39], m[38],  m[9],  m[8]],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, m[169], m[168], m[103], m[102],  m[89], m[88], m[55], m[54], m[41], m[40],  m[7],  m[6]],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, m[171], m[170], m[101], m[100],  m[91], m[90], m[53], m[52], m[43], m[42],  m[5],  m[4]],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, m[173], m[172],  m[99],  m[98],  m[93], m[92], m[51], m[50], m[45], m[44],  m[3],  m[2]],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, m[175], m[174],  m[97],  m[96],  m[95], m[94], m[49], m[48], m[47], m[46],  m[1],  m[0]]
    ]
    #print(qr)

    bitmask: list = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,], #timing
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,], #hi data
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,], #hi data
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,], #hi data
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,], #hi data
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,],
    ]
    
    for i in range(21):
        for j in range(21):
            qr[i][j] = int(qr[i][j])
            if bitmask[i][j] == 1:
                qr[i][j] = mask(qr[i][j])
    
    return qr

if __name__ == "__main__":
    print("You have to use this in as import package.")