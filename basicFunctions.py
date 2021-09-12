import hashlib

def getSha256(attributes):
    if (isinstance(attributes, str)):
        encodedStr = attributes.encode()
        return hashlib.sha256(encodedStr).hexdigest()
    elif (isinstance(attributes, list)):
        delimStr = getDelimitedString(attributes)
        encodedStr = delimStr.encode()
        return hashlib.sha256(encodedStr).hexdigest()
    else:
        raise Exception("Invalid type.")


def getDelimitedString(attributes):
    delimStr = ""

    for i in range(len(attributes)):
        if (i == 0):
            delimStr += attributes[i]
        else:
            delimStr += "|" + str(attributes[i])

    return delimStr

def compareHashes(str1, str2, dataList):
    if (str1.equals(str2)):
        dataList.append()
