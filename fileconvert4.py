#########
#	This version add try/except error handling for the files
#######

import sys
############# Globals ###############
simList = []    #define the simlist
attackList = []  # list to hold all of the attacks
attackType = []  #define a list to hold the attack types for each system
theCount = 0

########## Constant Definitions ###########
Csou = 3
Cdes = 4
Cmeth = 2
Cexe = 5
CisB = 7
CType = 12
CPhase = 13
CDate = 14

########### create a list that we will sort later removing the unnecessary fields
def createAttackList(theSource, theDest, theMethod, theParams, theBlock, theType, thePhase, theDate):
	theAttack = []

#### method has to be first to make sort work correctly when we print it out we will fix that
#### print order should be 
	theAttack.append(theMethod)   # item 0 print 3
	theAttack.append(theSource)   # item 1 print 0
	theAttack.append(theDest)     # print 1
	
	theAttack.append(theBlock)
	theAttack.append(theType)
	theAttack.append(theDate)
	theAttack.append(theParams)
	attackList.append(theAttack)
	
def appendTosimList(theSim, isBlocked):
#	print "appending to simList"
	if isBlocked == "Yes":
		myList = [theSim, 1, 0]
	else:
		myList = [theSim, 0, 1]
		
	simList.append(myList)
#	print simList

########### if the simulator is already in the list we just want to update isBlocked totals
def updatesimList(theSim, isBlocked):
	index = 0
#	print "updating sim list for "+theSim
	i = 0
	flag = 0
	while ( i < len(simList)):
#		print simList
#		print simList[i][0]
#       print simList[i][1]
#		print simList[i][2]
#		print "i = "+str(i)
		if (theSim in simList[i]):
#			print "theSim "+str(theSim)+" in simList "+str(simList[i])
			index = i
			flag = 1
#		else:
#			print "theSim "+str(theSim)+" not in simList "+str(simList[i])
		i = i + 1
	#	print "Index is "+str(index)
	if (isBlocked == "Yes"):
		simList[index][1] = simList[index][1] + 1
	else:
#			print "else"
		simList[index][2] = simList[index][2] + 1
#			print "index is "+str(index)
#	print ""  # just adds a newline for readability
		
############## returns true if the simulator is already in the list ############
def isInList(theSim):
#	print "checking to see if "+theSim+" is in the list"
	i = 0
	flag = 0
	while (i < len(simList)):
#		print simList[i]
		if theSim in simList[i]:
			flag = 1
		i = i + 1
	if (flag > 0):
		return 1
	else:
		return 0

	
	
def handleParts(theSim, isBlocked):
#	print "Handling the parts "+theSim+" "+isBlocked
	if (isInList(theSim)==1):
		updatesimList(theSim, isBlocked)
	else:
		appendTosimList(theSim, isBlocked)


	
	
def processLine(theLine):		###### process each line starting witht the second one
#	print theLine
	theParts = theLine.split("\",\"")
#	print theParts[4]+theParts[7]
	
	if (len(simList) == 0):
		appendTosimList(theParts[4], theParts[7])
	else:
		handleParts(theParts[4], theParts[7])
	createAttackList(theParts[3], theParts[4], theParts[2], theParts[5], theParts[7], theParts[12], theParts[13], theParts[14])
	
def writeOutput(theName):
#	print simList
	print theName
	i = 0
	while (i < len(simList)):
		print str(simList[i][0])+"\tBlocked = "+str(simList[i][1])+" Not Blocked = "+str(simList[i][2])
		i = i + 1
	fileName = "output_"+theName
	print fileName
	try:
		f = open(fileName, "w")
	except:
		print "unable to open the output file, probably because it's already open in excel stupid"
	f.write("\"Simulator\",\"Blocked\",\"Not Blocked\"\r")
	i = 0
	while ( i < len(simList)):
	#	theStr = "\""+str(simList[i][0])+"\"",\""+str(simList[i][1]+"\"",\"+str(simList[i][2]+"\"
		theStr = "\""+str(simList[i][0])+"\","+"\""+str(simList[i][1])+"\","+"\""+str(simList[i][2])+"\"\r"
	#	print theStr
		f.write(theStr)
		i = i + 1
	i = 0		## reset our index back to zero
######## write column headings ###########
	theStr = "\"Method\",\"Source\",\"Destination\",\"IsBlocked\",\"AttackType\",\"Date\",\"Parameters\"\r" 
	f.write(theStr)

	while (i < len(attackList)):
		theStr = "\""+str(attackList[i][0])+"\",\""+str(attackList[i][1])+"\",\""+str(attackList[i][2])+"\",\""+str(attackList[i][3])+"\",\""+str(attackList[i][4])+"\",\""+str(attackList[i][5])+"\",\""+str(attackList[i][6])+"\"\r"
		i = i + 1
		print theStr
		f.write(theStr)
	f.close
	
def sortAttackList(): 					## lets sort by simulator Name
	i = 0
#	while (i < len(attackList)):
#		print attackList[i][0]
#		i = i + 1
	attackList.sort()
	print "##################"
#	while (i < len(attackList)):
##		i = i + 1
#	print attackList

def writeAttackFile():
	print "writing the Attack File"
	
################### main routine ####################

#print "This is the name of the script: ", sys.argv[0]
#print "Number of arguments: ", len(sys.argv)
#print "The arguments are: ", str(sys.argv)
#print "Argument 2 is: ", sys.argv[1]

try:
	f = open(sys.argv[1], "r")
except IOError:
	print "Unable to open the input file"
	
lines = f.readlines()
#print lines

i=0
while i < len(lines):
#	print lines[i]
#	print "i = "+str(i)
	if (i > 0):				#### skip the header line
		processLine(lines[i])
	i = i + 1
f.close()
print str(i)+" lines processed"
sortAttackList()
writeOutput(sys.argv[1])

#print attackList

writeAttackFile()
