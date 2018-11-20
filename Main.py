import sys, os.path,itertools,timeit,threading,time
from anytree import Node,RenderTree
from progress.bar import Bar
from progress.spinner import Spinner
import pyfpgrowth
minSupport = -1
numberOfLines = -1
Root = Node("Root")
lastNode = Root
listOfNodes = []
allowedItems = []
frequentItemSets = []
answer = {}
frequentDictionary = {}
#dictionary to store the amount:
CountDictionary = {}
#make the header table a dictionary?
HeaderTable = {}
testSet = []
state = False




#Main Runner of the code
def Main():
    # spinner = Spinner('Working')

    start = timeit.timeit()
    global minSupport,allowedItems,state
    arguments = GetArguments()
    currentFile = readFile(arguments[1])
    minSupport = int((numberOfLines) * ((int) (arguments[2]) / 100))
    addToAnswer()
    print("Min Support: ",minSupport)
    Trim() #what do you do here?
    print("Trimmed")
    CreateHeaderTable()
    print("Created Header table:",HeaderTable)
    allowedItems = SortDictionary()
    print("Allowed Items:",allowedItems)
    FPGrowth(arguments[1])
    print("FP Growthed")
    print(RenderTree(Root))
    end = timeit.timeit()
    print("Answer", answer)
    OutPutToFile(answer,"MiningResult")
    state = True
    print("Time Ellapsed:", end-start)

#add singletons to answer
def addToAnswer():
    for x in CountDictionary:
        if CountDictionary.get(x) >= minSupport:
            print(CountDictionary.get(x),"is greater than",minSupport)
            a = tuple(x)
            answer[a]=(CountDictionary.get(x))
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

#sort transactions according to number of occurances
def SortTransactions(Transaction):
    newTransaction = []
    for x in allowedItems:
        if x in Transaction:
            newTransaction.append(x)
    return newTransaction

#create the fpGrowth tree
def FPGrowth(fileName):
    print("Reading Into Tree")
    readIntoTree(fileName)
    print("Read Into Tree, Generating Frequent Itemsets")
    # print(RenderTree(Root))
    findFrequentItemSets()
    print("Found Frequent Itemsets")

#this might be wrong?
def findFrequentItemSets():
    global allowedItems
    reversedAllowedItems = allowedItems[::-1]
    #find lowest value node
    while reversedAllowedItems != []:
        createSubTree(reversedAllowedItems[0])
        GenerateFreq(reversedAllowedItems[0])
        del reversedAllowedItems[0]
    # print("Freq",frequentDictionary)

#Genereate frequent itemsets from the frequent dictionary
def GenerateFreq(_node):
    list = []
    for x in HeaderTable.get(_node):
        list.append(addPathToList(x,[]))
    CalcFrequent(list,[],_node)

#calculates the frequent patterns
def CalcFrequent(List,frequents,name):
    toLookFor = getPermutations(List)
    toLookFor = clean(toLookFor,name)
    for y in toLookFor:
        counter = 0
        for x in List:
            if DoesItAppear(y,x):
                counter +=1

        fromDictionary = frequentDictionary.get(y[0])
        for k in range(0,len(fromDictionary)):
            if set(list(y)) == set(fromDictionary[k][0]) and fromDictionary[k][1] > 1:
                # print("Adding",fromDictionary[k][1], "To",counter)
                counter += fromDictionary[k][1]
                # print("new count: ",counter)
        if counter >= minSupport:
            if type(y) != 'tuple':
                y = tuple(y)
            answer[y]=counter


def clean(TheSet,name):
    L = list(TheSet)
    remove = []
    if(len(L) >0):
        for i in range(0,len(L)):
            if name not in L[i]:
                remove.append(i)
    remove.reverse()
    for x in remove:
        del L[x]
    return L



#returns a set of permutations to search for
def getPermutations(l):
    if len(l) == 1:
        return l
    perms = []
    for x in l:
        for b in range(1,len(x)+1):
            a =list(itertools.combinations(x,b))
            perms.append(a)
    temp = [item for sublist in perms for item in sublist]
    perms = set(temp)
    return perms

def working():
    # spinner = Spinner('Mining ')
    bar = Bar('Mining',max = 100)
    for i in range(100):
        time.sleep(1)
        if i == 99 and not state:
            i -=1
        bar.next()
    bar.finish()
    # while state != True:
        # time.sleep(1)
        # spinner.next


#returns true if tofind is a subset of tolook
def DoesItAppear(tofind,tolook):
    return set(tofind).issubset(tolook)


def addPathToList(node,list):
    if node.name == "Root":
        return list
    else:
        list.append(node.name)
        addPathToList(node.parent,list)
    return list


def createSubTree(StartNode):
    heads = HeaderTable.get(StartNode)
    currentList = []
    for x in heads:
        b = thing(x,[])
        currentList.append(b)
        frequentItemSets.append(b)
        if x.name not in frequentDictionary:
            frequentDictionary[x.name] = []
        currentamount = x.amount
        pathName = []
        for a in x.path:
            if(a.name == "Root"):# or a.name == x.name):
                pass
            else:
                pathName.append(a.name)
        currentPath = frequentDictionary.get(x.name)
        currentPath.append([pathName,currentamount])
        frequentDictionary[x.name]=(currentPath)

#this does something idk
def thing(remainingNodes,CurrentPass):
    if remainingNodes.name == "Root":
        return CurrentPass #return the current path
    else:
        temp = remainingNodes
        if temp.amount >= minSupport:
            CurrentPass.append(temp.name)
        thing(remainingNodes.parent,CurrentPass)
    return CurrentPass


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

#create output files for the tests
def OutPutToFile(fileToOut,FileName):
    file = open(FileName+".txt","w+")
    file.write("|FPs|=%d\n" % len(fileToOut))
    for fp,amt in fileToOut.items():
        file.write(str(fp)+":"+str(amt)+"\n")
    # write to file
    file.close()

# try:
#
#     threading.Thread(target=working()).start()
#     threading.Thread(target=Main()).start()
# except:
#     print("Error: unable to start")
# while 1:
#     pass
Main()
