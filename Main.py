#import FileIO
import sys, os.path,operator

minSupport = -1
numberOfLines = -1

#dictionary to store the amount:
CountDictionary = {}




#Main Runner of the code
def Main():
    global minSupport
    arguments = GetArguments()
    File = readFile(arguments[1])
    minSupport = (int) (numberOfLines) * ((int) (arguments[2]) / 100)
    print("Minsup:", minSupport)
    Trim()
    print(CountDictionary)
    print(SortDictionary())

#get and manipulate arguemnts
def GetArguments():
    print("arguments: " + str(sys.argv))
    return sys.argv

#Reads files into the code
def readFile(fileName):
    global numberOfLines
    if(os.path.isfile(fileName)):

        file = open(fileName,"r")

        numberOfLines = int(file.readline())

        for i in range (0,numberOfLines):
            a = file.readline().split()
            a = a[2:]
            CheckDictionary(a)
        file.close()
        return file
    else:
        print("Not a file Path")

#check the dictionary and if they exist increase counter else ignore
def CheckDictionary(Elements):

    for i in range (0,len(Elements)):
        if(not (Elements[i] in CountDictionary)):
            #if not in the dictionary add it
            CountDictionary[Elements[i]] = 1
        else:
            #if in the dictionary increase by one
            x = CountDictionary.get(Elements[i]) + 1
            CountDictionary.update({Elements[i]:x})

#trim the dictionary for elements that are below the minimum support
def Trim():
    Delete = []
    for x,y in CountDictionary.items():
        if(y < minSupport):
            Delete.append(x)
    for x in Delete:
        CountDictionary.pop(x)

#sorts the dictionary based on values.
def SortDictionary():
    return sorted(CountDictionary.items(),key=operator.itemgetter(1))


def CreateTree():
    print("Todo")

def SortTransactions():
    print("Todo")














Main()
