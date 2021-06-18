import re
from dictsToUse import someDicts

#Creator: Kuroyuki Kaze, @kuroyuki_kaze (Twitter)
#Version: 1.1
#Licensing: GPLv3

#For any functions beside createQR, use with care.

class LengthError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class MaskError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(self.message)

def buildQR(qr: list, start: tuple, end: tuple, message: str, startbit: int, mask: int) -> list:
    bitcount = startbit
    for i in range(start[0], end[0] + ((1*(start[0] < end[0])) + (-1)*(start[0] > end[0])), (1*(start[0] < end[0])) + (-1)*(start[0] > end[0])):
        for j in range(start[1], end[1] - 1, -1):
            #print(f"({i}, {j}) =", end="")
            if mask == 0:
                if ((i + j) % 2) == 0:
                    qr[i][j] = ApplyMask(int(message[bitcount]))
                else:
                    qr[i][j] = int(message[bitcount])
                #print(f"{qr[i][j]}")
                #print(f"bitcount: {bitcount}")
                bitcount += 1
            else:
                raise MaskError("Invalid mask.")

    return qr


def printQR(qr: list) -> None:
    """Prints the QR code from a binary string."""

    print("⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜")
    for i in range(21):
        print("⬜⬜⬜⬜⬜", end="")
        for j in range(21):
            if qr[i][j] == 1:
                print("⬛", end="")
            else:
                print("⬜", end="")
        print("⬜⬜⬜⬜⬜\n", end="")
    print("⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜")

def ApplyMask(bit: int) -> int:
    """Apply Mask."""

    if bit == 0:
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

def createQR_part1(message: str) -> list:
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


    return messageString

def createQR_part2(messageString: str, maskNum: int) -> list:
    errorCorrection: list = createErrorCorrectionH(messageString)

    for num in errorCorrection:
        messageString += bin(num)[2:].zfill(8)
    
    m: str = messageString 
    
    qr: list = [
        #0v 1v 2v 3v 4v 5v 6v 7v 8v 9d Ad Bd Cd Dv Ev Fv Gv Hv Iv Jv Kv
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], #0block
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], #1block
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1], #2block
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1], #3block
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1], #4block
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], #5block
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1], #6block, timing
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #7block
        [0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1], #8block
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9hi data
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #Ahi data
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #Bhi data
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #Chi data
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #Dblock
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #Eblock
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #Fblock
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #Gblock
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #Hblock
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #Iblock
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #Jblock
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  #Kblock
    ]

    qr = buildQR(qr, (20, 20), (9, 19), m, 0, maskNum)
    qr = buildQR(qr, (9, 18), (20, 17), m, 24, maskNum)
    qr = buildQR(qr, (20, 16), (9, 15), m, 48, maskNum)
    qr = buildQR(qr, (9, 14), (20, 13), m, 72, maskNum)
    qr = buildQR(qr, (20, 12), (7, 11), m, 96, maskNum)
    qr = buildQR(qr, (5, 12), (0, 11), m, 124, maskNum)
    qr = buildQR(qr, (0, 10), (5, 9), m, 136, maskNum)
    qr = buildQR(qr, (7, 10), (20, 9), m, 148, maskNum)
    qr = buildQR(qr, (12, 8), (9, 7), m, 176, maskNum)
    qr = buildQR(qr, (9, 5), (12, 4), m, 184, maskNum)
    qr = buildQR(qr, (12, 3), (9, 2), m, 192, maskNum)
    qr = buildQR(qr, (9, 1), (12, 0), m, 200, maskNum)
    
    return qr


def createQR(message: str, maskNum: int) -> list:
    msg = createQR_part1(message)
    qr = createQR_part2(msg, maskNum)
    
    return qr

if __name__ == "__main__":
    print("You have to use this in as import package.")