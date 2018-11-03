import sys, os.path,operator

minSupport = -1
numberOfLines = -1
listOfNodes = []

#dictionary to store the amount:
CountDictionary = {}




#Main Runner of the code
def Main():
    addRoot()
    global minSupport
    arguments = GetArguments()
    currentFile = readFile(arguments[1])
    minSupport = (int) (numberOfLines) * ((int) (arguments[2]) / 100)
    print("Minsup:", minSupport)
    Trim()
    print(CountDictionary)
    print(SortDictionary())
    FPGrowth(arguments[1])

#get and manipulate arguemnts
def GetArguments():
    print("arguments: " + str(sys.argv))
    return sys.argv

#Reads files into the code
def readFile(fileName):
    if(os.path.isfile(fileName)):
        readIntoDictionary(fileName)
    else:
        print(fileName + " Not a file Path")
        exit(1)

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

#sorts the dictionary based on values, and returns theys
def SortDictionary():
    SortedDictionary = sorted(CountDictionary.items(),key=lambda t: t[1],reverse=True)
    sortedkeys = []
    for x in SortedDictionary:
        sortedkeys.append(x[0])
    return sortedkeys



#creates the tree structure
def CreateTree(Transaction):

    global listOfNodes
    for i in range(0,len(Transaction)):
        listOfNodes.append(Node(Transaction[i],1))
    print(listOfNodes)


def SortTransactions():
    print("Todo")

def FPGrowth(fileName):
    readIntoTree(fileName)

def readIntoDictionary(fileName):
    global numberOfLines
    file = open(fileName, "r")
    numberOfLines = int(file.readline())
    for i in range (0,numberOfLines):
        a = file.readline().split()
        a = a[2:]
        CheckDictionary(a)
    file.close()

def readIntoTree(fileName):
    file = open(fileName,"r")
    for i in range(0,int(file.readline())):
        a = file.readline().split()
        a = a[2:]
        CreateTree(a)

def addRoot():
    global listOfNodes
    root = Node("*", 0)
    listOfNodes.append(root)



#for the tree
#how the hell do I do classes? is this correct?

class Node(object):
    def __init__(self,data,amount):
        self.data = data
        self.amount = amount
        self.children = []

    def add_child(self,obj):
        self.children.append(obj)

    def increase_amount(self):
        self.amount = self.amount + 1




Main()
