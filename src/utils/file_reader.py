#reads lol files

#
from typing import List

#remove inline BTW from the lines
def removeBTW(line:str) -> str:

    #initialize index counter and track if were inside a string literal
    i =0
    inString = False

    #Iterate each chracter in line
    while i < len(line):
        if line[i]== '"': #if double qoute, actve instring flag
            inString = not inString # then ignore btw inside strings
        elif not inString and line[i:i+3]== "BTW": #if not inside the strng
            return line [:i].rstrip() #return everything everything before BTW
        i +=1  #Then move
    return line.rstrip()  #return the full

#reads the .lol file and return list  of cleaned code lines.
def readLines(file_path:str) -> List[str]:
    #remove single line BTW comments

    cleanedLines=[]
    inblockComments = False

    with open (file_path, "r", encoding = "utf-8") as file:
        for rawLine in file:
            line = rawLine.rstrip("\n").strip()

            #handle multi line comments
            if line == "OBTW":
                inblockComments = True
                continue
            if line == "TLDR":
                inblockComments = False
                continue
            if inblockComments:
                continue #wil skip the content inside OBTW

            line = removeBTW(line)

            #skip empty lines
            if line.strip()=="":
                continue

            #add the clean lines to the results
            cleanedLines.append(line.strip())

    return cleanedLines

# test file
if __name__ == "__main__":
    testPath = "tests/testcase.lol"
    for i, line in enumerate(readLines(testPath), start=1):
        print(f"{i:02d}: {line}")


