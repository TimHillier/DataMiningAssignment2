#import FileIO
import sys, os.path



#Main Runner of the code
def Main():
    arguments = GetArguments()
    File = readFile(arguments[1])


#get and manipulate arguemnts
def GetArguments():
    print("arguments: " + str(sys.argv))
    return sys.argv

#Reads files into the code
def readFile(fileName):

    if(os.path.isfile(fileName)):
        file = open(fileName,"r")
        print(file.read())
        return file
    else:
        print("Not a file Path")


Main()
