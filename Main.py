import sys, os.path
from anytree import Node,RenderTree

minSupport = -1
numberOfLines = -1
Root = Node("Root")
lastNode = Root
listOfNodes = []
allowedItems = []
frequentItemSets = []
#dictionary to store the amount:
CountDictionary = {}
#make the header table a dictionary?
HeaderTable = {}




#Main Runner of the code
def Main():
    global minSupport,allowedItems
    arguments = GetArguments()
    currentFile = readFile(arguments[1])
    minSupport = int((numberOfLines) * ((int) (arguments[2]) / 100))
    print("Minsup:", minSupport)
    # Trim()
    CreateHeaderTable()
    print(CountDictionary)

    allowedItems = SortDictionary()
    print("Allowed: ", allowedItems)
    FPGrowth(arguments[1])
    print(RenderTree(Root))
    # print(HeaderTable)
    for a in HeaderTable.keys():
        getParents(HeaderTable.get(a))



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
#not sure if this is actually needed based on how FP-growth works
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

#create empty Header Table
def CreateHeaderTable():
    for x in CountDictionary:
        HeaderTable[x] = []




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
    # print("Current Transaction: ", approved, "\n current: ",current)
    addNodes(approved,current)

def findLowest(approvedNodes,currntNode):
    # print("approved: ",approvedNodes)
    lowestNode = currntNode
    if approvedNodes == []:
        # print("X")
        return lowestNode
    if currntNode.children == []:
        # print("Y")
        return lowestNode
    # print(currntNode.name," Children:", currntNode.children)
    for i in range(0,len(currntNode.children)):
        if(currntNode.children[i].name == approvedNodes[0]):
            del approvedNodes[0]
            currntNode.children[i].amount +=1
            currntNode=currntNode.children[i]
            lowestNode = findLowest(approvedNodes,currntNode)
            break
    return lowestNode

#add node to the tree if it doesnt exist otherwise increase amount
def addNodes(approvedNodes, currntNode):
    if approvedNodes == []:
        return
    elif currntNode.name == approvedNodes[0]:
        currntNode.amount += 1
        del approvedNodes[0]
        addNodes(approvedNodes,currntNode)
    else:
        newNode = Node(approvedNodes[0], parent=currntNode, amount=1)
        addToHeaderTable(newNode)
        del approvedNodes[0]
        listOfNodes.append(newNode)
        addNodes(approvedNodes,newNode)


#add node to header table
def addToHeaderTable(NodeToAdd):
    if(NodeToAdd.name in HeaderTable):
        x = HeaderTable[NodeToAdd.name]
        x.append(NodeToAdd)
        HeaderTable.update({NodeToAdd.name:x})

def printParents(Child):
    print(Child.name," Parents:")
    print(Child.parent)

#accepts the array of nodes of specific child
def getParents(childFromDictionary):
    for i in range(0,len(childFromDictionary)):
        printParents(childFromDictionary[i])
        print(childFromDictionary[i].amount)


#sort transactions according to number of occurances
def SortTransactions(Transaction):
    newTransaction = []
    for x in allowedItems:
        if x in Transaction:
            newTransaction.append(x)
    # print("Old Transaction: ", Transaction)
    # print("New Transaction: ",newTransaction)
    return newTransaction

#create the fpGrowth tree
def FPGrowth(fileName):
    readIntoTree(fileName)
    findFrequentItemSets()

#this might be wrong?
def findFrequentItemSets():
    global allowedItems
    reversedAllowedItems = allowedItems[::-1]
    #find lowest value node
    print("rev: ", reversedAllowedItems)
    find(reversedAllowedItems)

def find(itemset):
    if(itemset == []):
        return
    print(itemset)
    if(CountDictionary[itemset[0]] < minSupport):
        print("Deleting:",itemset[0])
        del itemset[0]
        find(itemset)
    else:
        print("k")
#read the file into the count dictionary
def readIntoDictionary(fileName):
    global numberOfLines
    file = open(fileName, "r")
    numberOfLines = int(file.readline())
    for i in range (0,numberOfLines):
        a = file.readline().split()
        a = a[2:]
        CheckDictionary(a)
    file.close()

#read the file into the tree structure
def readIntoTree(fileName):
    file = open(fileName,"r")
    for i in range(0,int(file.readline())):
        a = file.readline().split()
        a = a[2:]
        a = SortTransactions(a)
        CreateTree(a)







Main()
