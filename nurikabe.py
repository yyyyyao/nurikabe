import copy
import time
import sys

#get List of Walls.
def getWallList(_board):
    _wList = []
    for i in range(xSize * ySize):
        if _board[i][0] <= 0:
            _wList.append(i)
    return _wList

#check different Islands contiguous.
def checkIsland(_isl):
    islIndex = _isl[0]
    islNum = _isl[1]
    islId = _isl[2]
    checkedWList = []
    conAns = []
    checkQ = []
    checkQ.append(islIndex)
    conAns.append(islIndex)

    while checkQ:
        cIndex = checkQ.pop()
        if cIndex in checkedWList:
            continue
        checkedWList.append(cIndex)
        for i in adjMat[cIndex]:
            if board[i][0] > 0:
                if board[i][0] == islId:
                    if i not in conAns:
                        conAns.append(i)
                    if i not in checkedWList:
                        checkQ.append(i)
                else:
                    print "board[i][0]", board[i][0], ":", islIndex
                    print "different Island contiguous. isl:", _isl
                    return False
    if len(conAns) != islNum:
        return False 
    return True


#deprecated.
def checkIslands(_board):
    _islID = 0
    for isl in islList:
        _islID += 1
        islIndex = isl[0]
        islNum = isl[1]
        checkedWList = []
        conAns = []
        checkQ = []
        checkQ.append(islIndex)
        conAns.append(islIndex)

        while checkQ:
            cIndex = checkQ.pop()
            if cIndex in checkedWList:
                continue
            checkedWList.append(cIndex)
            for i in adjMat[cIndex]:
                if _board[i][0] > 0:
                    if _board[i][0] == _islID:
                        if i not in conAns:
                            conAns.append(i)
                        if i not in checkedWList:
                            checkQ.append(i)
                    else:
                        print "different Island contiguous."
                        return False
        #print "islIndex", islIndex, "conAns", conAns
        if len(conAns) != islNum:
            return False 
    return True

#check 2x2Wall present. If yes, return False.
def check2x2Wall():
    for i in range(xSize * (ySize - 1)):
        if i % xSize == xSize - 1:
            continue
        elif board[i][0] <= 0 and board[i + 1][0] <= 0 and\
                board[i + xSize][0] <= 0 and board[i + xSize + 1][0] <= 0: 
                    return False
    return True

#check all of walls are connected.
def checkConWall(_board):
    ans = getWallList(_board)
    checkedWList = []
    conAns = []
    checkQ = []
    checkQ.append(ans[0])
    conAns.append(ans[0])

    while checkQ:
        cIndex = checkQ.pop()
        if cIndex in checkedWList:
            continue
        checkedWList.append(cIndex)
        for i in adjMat[cIndex]:
            if _board[i][0] <= 0:
                if i not in conAns:
                    conAns.append(i)
                if i not in checkedWList:
                    checkQ.append(i)
    conAns.sort()
    if conAns == ans:
        return True
    else:
        return False

#check _board is answer.
def checkBoardState(_board):
    if not check2x2Wall():
        "Error 2x2"
        return False
    if not checkConWall(_board):
        "Error Wall connection"
        return False

    for isl in islList:
        if not checkIsland(isl):
            "Error Island Connection"
            return False
    return True

#check _index point can put _islId. This is similar checkIsland.
#but this is small and fast.
def checkConIsland(_index, _islId, _board):
    for i in adjMat[_index]:
        #print i
        #print "_board[i][0]", _board[i][0], "_islId", _islId
        if _board[i][0] > 0 and _board[i][0] != _islId:
            #print "ConIsLand", _board[i][0], ":", _islId
            return False
    return True

def checkConIslandNum(_cIndexes):
    checkedIslands = []
    checkQ = [_cIndexes[0]]

    while checkQ:
        cIndex = checkQ.pop()
        if cIndex in checkedIslands:
            continue
        checkedIslands.append(cIndex)
        for i in adjMat[cIndex]:
            if i in _cIndexes:
                checkQ.append(i)
    if len(_cIndexes) == len(checkedIslands):
        return True
    return False

#make adjacent matrix.
def makeAdjMat(x, y):
    Maxindex = x * y
    for i in range(Maxindex):
        if not i < x:
            adjMat[i].append(i - x)
        if not i >= x * (y - 1):
            adjMat[i].append(i + x)
        if not i % x == 0:
            adjMat[i].append(i - 1)
        if not i % x == x -1:
            adjMat[i].append(i + 1)

def printBoards(_board):
    print "--------------------"
    printBoard(_board)
    print "--------------------"
    printBoardId(_board)

#print Board State(num).
def printBoard(board):
    for i in range(ySize):
        for j in range(xSize):
            print "%2d" % board[j + i * xSize][1],
        print ""
    return 

#print Board State(ID).
def printBoardId(board):
    for i in range(ySize):
        for j in range(xSize):
            print "%2d" % board[j + i * xSize][0],
        print ""
    return 

#get all of possible position about isl(Index)
#_islIndexList is present position list.
def checkPath(isl, _islIndexList):
    islIndex = isl[0]
    islNum = isl[1]
    islId = isl[2]
    checkedWList = {}
    boardList = {}
    ans = []
    conAns = []
    checkQ = []
    checkQ.append(_islIndexList)
    conAns.append(islIndex)
    boardList[tuple(_islIndexList)] = board

    if islNum == 1:
        return ans

    while checkQ:
        cIndexes = checkQ.pop()
        __board = boardList[tuple(cIndexes)]
        cIndexes.sort()
        key = tuple(cIndexes)
        if key in checkedWList:
            continue
        checkedWList[key] = True

        for cIndex in cIndexes:
            for i in adjMat[cIndex]:
                if i in cIndexes:
                    continue
                if __board[i][0] == 0:
                    _cIndexes = copy.deepcopy(cIndexes)
                    _cIndexes.append(i)
                    _cIndexes.sort()
                    key = tuple(_cIndexes)
                    if key in checkedWList:
                        continue
                    _board = copy.deepcopy(__board)
                    _board[i][0] = islId
                    _board[i][1] = islNum

                    if checkConWall(_board) and checkConIsland(i, islId, _board):
                        if len(_cIndexes) == islNum:
                            #_cIndexes.remove(islIndex)
                            if _cIndexes not in ans and\
                                checkConIslandNum(_cIndexes):
                                    ans.append(_cIndexes)
                            continue

                        _cIndexes.sort()
                        checkQ.append(_cIndexes)
                        boardList[tuple(_cIndexes)] = _board
                    else:
                        """
                        if not checkConWall(_board):
                            print "ERR:checkConWall"
                        if not checkConIsland(i, islId, _board):
                            print "ERR:checkConIsland"
                        """
    return ans
    
#check 2x2 Walls. return if it finds puttable point.
def check2x2Island(_reachIdMat, _board):
    ansList = []
    for i in range(xSize * (ySize - 1)):
        if i % xSize == xSize - 1:
            continue
        elif _board[i][0] <= 0 and _board[i + 1][0] <= 0 and\
                _board[i + xSize][0] <= 0 and _board[i + xSize + 1][0] <= 0: 
                    reachNum = 0
                    index = 0
                    id = 0
                    temp_index = i
                    if _board[temp_index][0] == 0 and \
                            len(_reachIdMat[temp_index]) != 0:
                                if len(_reachIdMat[temp_index]) == 1:
                                    reachNum += 1
                                    index = temp_index 
                                    id = _reachIdMat[temp_index][0]
                                else:
                                    reachNum += 10

                    temp_index = i + 1
                    if _board[temp_index][0] == 0 and \
                            len(_reachIdMat[temp_index]) != 0:
                                if len(_reachIdMat[temp_index]) == 1:
                                    reachNum += 1
                                    index = temp_index 
                                    id = _reachIdMat[temp_index][0]
                                else:
                                    reachNum += 100

                    temp_index = i + xSize
                    if _board[temp_index][0] == 0 and \
                            len(_reachIdMat[temp_index]) != 0:
                                if len(_reachIdMat[temp_index]) == 1:
                                    reachNum += 1
                                    index = temp_index 
                                    id = _reachIdMat[temp_index][0]
                                else:
                                    reachNum += 1000

                    temp_index = i + xSize + 1
                    if _board[temp_index][0] == 0 and\
                            len(_reachIdMat[temp_index]) != 0:
                                if len(_reachIdMat[temp_index]) == 1:
                                    reachNum += 1
                                    index = temp_index 
                                    id = _reachIdMat[temp_index][0]
                                else:
                                    reachNum += 10000 

                    if reachNum == 1:
                        #print i
                        #print "canPUt index:", index, "id", id
                        ansList.append((index, id))
    return ansList

#_islIndexList is fixed.(satisfied answer)
#so, It can put adjacent point to wall.
def fixedIsland(_islIndexList, _board):
    wallList = []

    for i in _islIndexList:
        for j in adjMat[i]:
            if _board[j][0] == 0:
                if j not in wallList:
                    wallList.append(j)
    return wallList

def updateReachIdMat(ans, reachIdMat, islId):
    for i in ans:
        for j in i:
            if islId not in reachIdMat[j]:
                reachIdMat[j].append(islId)

def reducePosssibleAnsList(_possibleAnsLists, _islIndexList):
    newPossibleAnsLists = [[] for i in range(islID - 1)]
    _index = 0
    for possibleAnses in _possibleAnsLists:
        for possibleAns in possibleAnses:
            if set(possibleAns).issuperset(set(_islIndexList[_index])):
                newPossibleAnsLists[_index].append(possibleAns)
        _index += 1
    return newPossibleAnsLists

def getCanPutIndexes(_ans):
    _canPutIndexes = []
    if _ans:
        for i in _ans[0]:
            checker = True
            for index in _ans:
                if i not in index:
                    checker = False
                    break
            if checker:
                _canPutIndexes.append(i)
    return _canPutIndexes

def getPutNumFromID(_id, _islList):
    for isl in _islList:
        _islId = isl[2]
        if _islId == id:
            putNum = isl[1]
            return putNum
    return -1

def getUnreachableWallIndex(_reachIdMat, _board):
    _wallIndexes = []
    i = 0
    for reachIds in _reachIdMat:
        if _board[i][0] == 0 and not reachIds:
            _wallIndexes.append(i)
        i += 1
    return _wallIndexes
     
#main function.
if __name__ == '__main__':
    #pre processing
    argvs = sys.argv
    argc = len(argvs)
    strt = time.time()

    if (argc == 2):
        fileName = argvs[1]
    else:
        print "Usage: # python %s filename" % argvs[0]
        print "Use default filename:hoge.txt"
        fileName = "p3.txt"

    f = open(fileName, 'r')
    wList = []
    maxWordLen = 0

    xSize = int(f.readline())
    ySize = int(f.readline())
    adjMat = [[] for i in range(xSize * ySize)]
    board = [[] for i in range(xSize * ySize)]
    for i in range(xSize * ySize):
        board[i].append(0)
        board[i].append(0)

    makeAdjMat(xSize, ySize)
 
    line = f.readline().rsplit()
    islList = []
    islID = 1
    while line:
        index = int(line[0]) + int(line[1]) * xSize
        islList.append((index, int(line[2]), islID))
        board[index][0] = islID
        islID += 1
        board[index][1] = int(line[2])
        line = f.readline().rsplit()
    f.close()

    islIndexList = [[] for i in range(islID - 1)]

    for i in range(0, islID - 1):
        islIndexList[i].append(islList[i][0])

    printBoards(board)

    possibleAnsList = [[] for i in range(islID - 1)]

    oldBoard = []
    k = 0
    while True:
        #checkPath
        reachIdMat = [[] for i in range(xSize * ySize)]
        islList.sort(lambda x, y: x[1] - y[1]) 

        for isl in islList:
            islIndex = isl[0]
            islNum = isl[1]
            islId = isl[2]
            indx = islId - 1
            if len(islIndexList[indx]) == islNum:
                wallList = fixedIsland(islIndexList[indx], board)
                for i in wallList:
                    board[i][0] = -1
                indx += 1
                continue

            ans = checkPath(isl, islIndexList[indx])
            possibleAnsList[indx] = ans
            updateReachIdMat(ans, reachIdMat, islId)
            canPutIndexes = getCanPutIndexes(ans)
            for put in canPutIndexes:
                board[put][0] = islId
                board[put][1] = islNum
                if put not in islIndexList[indx]:
                    islIndexList[indx].append(put)
        #printBoards(board)

        #2x2Island
        #canPutter is (index, islId). 
        canPutter = check2x2Island(reachIdMat, board)
        for put in canPutter:
            index = put[0]
            id = put[1]
            putNum = getPutNumFromID(id, islList)
            board[index][0] = id
            board[index][1] = putNum
            islIndexList[id - 1].append(index)

        #put Walls.
        wallIndexes = getUnreachableWallIndex(reachIdMat, board)
        for i in wallIndexes:
            board[i][0] = -1

        #reduce Possible answer list.
        possibleAnsList = reducePosssibleAnsList(possibleAnsList, islIndexList)

        for isl in islList:
            islIndex = isl[0]
            islNum = isl[1]
            islId = isl[2]
            indx = islId - 1
            possibleAns = possibleAnsList[indx]
            if len(possibleAns) == 1:
                for i in possibleAns[0]:
                    if board[i][0] == 0:
                        board[i][0] = islId
                        board[i][1] = islNum
                        if i not in islIndexList[indx]:
                            islIndexList[indx].append(i)

        if oldBoard == board:
            print "end heuristic search"
            print "loop:", k
            break
        oldBoard = copy.deepcopy(board)
        k += 1
        #end try heulistic search 2loops.

    #try searching.
    #depthSearch(board, possibleAnsList, islList)

    """
    indx = 0
    for j in possibleAnsList:
        if len(j) == 1:
            print "unique answer id:", indx + 1, ":", j
        elif len(j) == 0:
            print "unique answer id:", indx + 1, ":", j
        else:
            print "not solved id:", indx + 1, " num:", len(j), " :", j
        indx += 1
    """
        
    if checkBoardState(board):
        print "This is Answer."
        printBoard(board)
