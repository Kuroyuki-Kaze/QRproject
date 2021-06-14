alphaToDecTable = {0: 1}
decToAlphaTable = {}
GF = 256
PP = 285

for i in range(1, 256):
    alphaToDecTable[i] = alphaToDecTable[i - 1] * 2
    if alphaToDecTable[i] >= GF:
        alphaToDecTable[i] = alphaToDecTable[i] ^ PP
    decToAlphaTable[alphaToDecTable[i]] = i