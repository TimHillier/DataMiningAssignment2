import sys, os.path
from anytree import Node,RenderTree

minSupport = -1
numberOfLines = -1
Root = Node("Root")
lastNode = Root
listOfNodes = []
allowedItems = []
#dictionary to store the amount:
CountDictionary = {}




#Main Runner of the code
def Main():
    global minSupport,allowedItems
    arguments = GetArguments()
    currentFile = readFile(arguments[1])
    minSupport = (int) (numberOfLines) * ((int) (arguments[2]) / 100)
    print("Minsup:", minSupport)
    Trim()
    print(CountDictionary)
    allowedItems = SortDictionary()
    print("Allowed: ", allowedItems)
    FPGrowth(arguments[1])
    print(RenderTree(Root))

#get and manipulate arguemnts
def GetArguments():
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
    global Root,listOfNodes,allowedItems,lastNode
    approved = []
    for i in range(0,len(Transaction)):
        if Transaction[i] in allowedItems:
            approved.append(Transaction[i])

   #Get to the lowest possible Node
    current = findLowest(approved,Root)
    #add nodes to the tree
    addNodes(approved,current)

def findLowest(approvedNodes,currntNode):
    lowestNode = currntNode
    if approvedNodes == []:
        return lowestNode
    if currntNode.children == []:
        return lowestNode
    for i in range(0,len(currntNode.children)):
        if(currntNode.children[i].name == approvedNodes[0]):
            del approvedNodes[0]
            currntNode.children[i].amount +=1
            currntNode=currntNode.children[i]
            lowestNode = findLowest(approvedNodes,currntNode)
        break
    return lowestNode


def addNodes(approvedNodes, currntNode):
    print("current Node",currntNode)
    if approvedNodes == []:
        return
    elif currntNode.name == approvedNodes[0]:
        currntNode.amount += 1
        del approvedNodes[0]
        addNodes(approvedNodes,currntNode)
    else:
        newNode = Node(approvedNodes[0],parent=currntNode,amount=1)
        del approvedNodes[0]
        listOfNodes.append(newNode)
        addNodes(approvedNodes,newNode)



def SortTransactions(Transaction):
    newTransaction = []
    for x in allowedItems:
        if x in Transaction:
            newTransaction.append(x)
    # print("Old Transaction: ", Transaction)
    # print("New Transaction: ",newTransaction)
    return newTransaction

def FPGrowth(fileName):
    readIntoTree(fileName)
    findFrequentItemSets()

def findFrequentItemSets():
    global allowedItems
    reversedAllowedItems = allowedItems[::-1]
    #find lowest value node



    print("rev: ", reversedAllowedItems)
    # lastNode = findBottom(NameOfNode)

def findBottom(NameOfNode):
    print("Bottom")
    return NameOfNode
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
        a = SortTransactions(a)
        CreateTree(a)







Main()
