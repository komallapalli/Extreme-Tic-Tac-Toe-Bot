from __future__ import print_function
import random
import copy
import datetime

class Team60:

    def __init__(self):
        self.weight_factor = [2,3,3,2,3,4,4,3,3,4,4,3,2,3,3,2]
        self.begin = 1e10
        self.termVal = 1e10
        self.trans = {}
        self.dict = {'x':1,'o':-1,'-':0,'d':0}
        self.marker = 'x'
        self.limit = 10
        self.limitReach = 0
        self.timeLimit = datetime.timedelta(seconds = 14.7)
    def getMarker(self, flag):
        if flag == 'x':
            return 'o'
        else:
            return 'x'
    def evaluate(self,board,blx,bly,tmpBlock):

        BL_X = 4*blx
        BL_Y = 4*bly
        colCnt = [3,3,3,3]
        rowCnt = [3,3,3,3]
        val = 0
        INFINITY = 1e10
        for i in range(4):
            t = 4*i
            for j in range(4):
                mark = board.board_status[BL_X+i][BL_Y+j]
                dictVal = self.dict[mark]
                if(dictVal!=0):
                    val = val + dictVal*self.weight_factor[t+j]
                    if (colCnt[j] == 3):
                        colCnt[j] = dictVal * 5
                    elif(dictVal * colCnt[j] < 0):
                        colCnt[j] = 0
                    if (rowCnt[i] == 3):
                        rowCnt[i] = dictVal * 5
                    elif(dictVal * rowCnt[i] < 0):
                        rowCnt[i] = 0
                    rowCnt[i]=rowCnt[i]*16
                    colCnt[j]=colCnt[j]*16

        diam1,diam2,diam3,diam4 = 3,3,3,3
        for i in range(4):
            if i==0:
    			x = 0
    			y = 1
            elif i==1:
    			x = 1
    			y = 0
            elif i==2:
    			x = 2
    			y = 1
            else:
    			x = 1
    			y = 2
            mark = board.board_status[BL_X+x][BL_Y+y]
            dictVal = self.dict[mark]
            if(dictVal!=0):
                if(diam1==3):
                    diam1 = dictVal*5
                elif(dictVal*diam1<0):
                    diam1 = 0
                diam1=diam1*16
            mark = board.board_status[BL_X+x][BL_Y+y+1]
            dictVal = self.dict[mark]
            if(dictVal!=0):
                if(diam2==3):
                    diam2 = dictVal*5
                elif(dictVal*diam2<0):
                    diam2 = 0
                diam2=diam2*16
            mark = board.board_status[BL_X+x+1][BL_Y+y]
            dictVal = self.dict[mark]
            if(dictVal!=0):
                if(diam3==3):
                    diam3 = dictVal*5
                elif(dictVal*diam3<0):
                    diam3 = 0
                diam3=diam3*16
            mark = board.board_status[BL_X+x+1][BL_Y+y+1]
            dictVal = self.dict[mark]
            if(dictVal!=0):
                if(diam4==3):
                    diam4 = dictVal*5
                elif(dictVal*diam4<0):
                    diam4 = 0
                diam4=diam4*16
        draw = 12
        for i in xrange(4):
            if(rowCnt[i]==0):
                draw-=1
            if(colCnt[i]==0):
                draw-=1
        if(diam1==0):
            draw=draw-1
        if(diam2==0):
            draw= draw-1
        if(diam3==0):
            draw= draw -1
        if(diam4==0):
            draw = draw-1

        if(draw==0):
            tmpBlock[blx][bly] = 'd'
            return 0
        for i in range(4):
            if(colCnt[i]!=3):
                val = val + colCnt[i]
            if(rowCnt[i]!=3):
                val = val + rowCnt[i]

        if(diam1!=3):
            val = val + diam1
        if(diam2!=3):
            val = val + diam2
        if(diam3!=3):
            val = val +diam3
        if(diam4!=3):
            val = val +diam4

        return val

    def blockEval(self,board,tmpBlock):
        rowCnt = [3,3,3,3]
        val = 0
        colCnt = [3,3,3,3]
        INFINITY = 1e10
        for i in range(4):
            t = 4*i
            for j in range(4):
                mark = tmpBlock[i][j]
                dictVal = self.dict[tmpBlock[i][j]]
                if(mark!='-'):
                    val = val + dictVal*self.weight_factor[t+j]
                    if (colCnt[j]==3):
                        colCnt[j] = dictVal*5
                    elif(dictVal*colCnt[j]<=0):
                        colCnt[j] = 0
                    if (rowCnt[i]==3):
                        rowCnt[i] = dictVal*5
                    elif(dictVal*rowCnt[i]<=0):
                        rowCnt[i] = 0
                    colCnt[j]=colCnt[j]*16
                    rowCnt[i]=rowCnt[i]*16

        diam1,diam2,diam3,diam4 = 3,3,3,3
        for i in xrange(4):
                if i==0:
    				x = 0
    				y = 1
                elif i==1:
    				x = 1
    				y = 0
                elif i==2:
    				x = 2
    				y = 1
                else:
    				x = 1
    				y = 2
                mark = tmpBlock[x][y]
                if(mark!='-'):
                    dictVal = self.dict[mark]
                    if(diam1==3):
                        diam1 = dictVal*5
                    elif(dictVal*diam1<=0):
                        diam1 = 0
                    diam1=diam1*16
                    diam1 = diam1 *dictVal*dictVal
                mark = tmpBlock[x][y+1]
                if(mark!='-'):
                    dictVal = self.dict[mark]
                    if(diam2==3):
                        diam2 = dictVal*5
                    elif(dictVal*diam2<=0):
                        diam2 = 0
                    diam2=diam2*16
                    diam2 = diam2*dictVal*dictVal
                mark = tmpBlock[x+1][y]
                if(mark!='-'):
                    dictVal = self.dict[mark]
                    if(diam3==3):
                        diam3 = dictVal*5
                    elif(dictVal*diam3<=0):
                        diam3 = 0
                    diam3=diam3*16
                    diam3 = diam3*dictVal*dictVal
                mark = tmpBlock[x+1][y+1]
                if(mark!='-'):
                    dictVal = self.dict[mark]
                    if(diam4==3):
                        diam4 = dictVal*5
                    elif(dictVal*diam4<=0):
                        diam4 = 0
                    diam4=diam4*16
                    diam4 = diam4*dictVal*dictVal

        for i in xrange(4):
            if(colCnt[i]!=3):
                val = val +colCnt[i]
            if(rowCnt[i]!=3):
                val = val +rowCnt[i]

        if(diam1!=3):
            val= val +diam1
        if(diam2!=3):
            val= val +diam2
        if(diam3!=3):
            val= val +diam3
        if(diam4!=3):
            val= val +diam4

        return val

    def heuristic(self, board):
        final = 0
        tmpBlock = copy.deepcopy(board.block_status)
        for i in range(4):
            for j in range(4):
                eval_ans = self.evaluate(board,i,j,tmpBlock)
                final = final + eval_ans
        final = final + self.blockEval(board,tmpBlock)*144
        del(tmpBlock)
        return final

    def alphaBeta(self, board, old_move, flag, depth, alpha, beta):

        hashval = hash(str(board.board_status))
        temp = 1
        INFINITY = 1e10
        if(self.trans.has_key(hashval)):
            bounds = self.trans[hashval]
            if(bounds[1] <= alpha):
                return bounds[1],old_move
            if(bounds[0] >= beta):
                return bounds[0],old_move
            if alpha < bounds[0]:
                alpha = bounds[0]
            if beta > bounds[1]:
                beta = bounds[1]

        cells = board.find_valid_move_cells(old_move)
        random.shuffle(cells)
        if (flag == 'x'):
            tmp = copy.deepcopy(board.block_status)
            a = alpha
            new = 'o'
            nodeVal = -INFINITY, cells[0]

            for chosen in cells :
                te = 0
                if datetime.datetime.utcnow() - self.begin >= self.timeLimit :
                    self.limitReach = 1
                    break
                te = 1
                board.update(old_move, chosen, flag)
                if (board.find_terminal_state()[0] == 'x'):
                    nodeVal = self.termVal,chosen
                    board.block_status = copy.deepcopy(tmp)
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    break
                if (board.find_terminal_state()[0] == 'o'):
                    board.block_status = copy.deepcopy(tmp)
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    continue
                if(board.find_terminal_state()[0] == 'NONE'):
                    x,d,o,tmp1 = 0,0,0,0
                    for i2 in xrange(4):
                        for j2 in xrange(4):
                            if(board.block_status[i2][j2] == 'x'):
                                x = x +1
                            elif(board.block_status[i2][j2] == 'o'):
                                o = o +1
                            elif(board.block_status[i2][j2] == 'd'):
                                d = d +1
                    if(x==o):
                        tmp1 = 0
                    elif(x < 0):
                        tmp1 = -INFINITY/2 - 10*(o-x)
                    elif (x > o):
                        tmp1 = INFINITY/2 + 10*(x-o)
                elif( depth >= self.limit):
                    tmp1 = self.heuristic(board)
                else:
                    tmp1 = self.alphaBeta(board, chosen, new, depth+1, a, beta)[0]


                if(nodeVal[0] < tmp1):
                    nodeVal = tmp1,chosen
                board.block_status = copy.deepcopy(tmp)
                board.board_status[chosen[0]][chosen[1]] = '-'
                if a < tmp1:
                    a = tmp1
                if beta <= nodeVal[0] :
                    break
            del(tmp)

        if (flag == 'o'):
            tmp = copy.deepcopy(board.block_status)
            b = beta
            new = 'x'
            nodeVal = INFINITY, cells[0]

            for chosen in cells :
                te = 0
                if datetime.datetime.utcnow() - self.begin >= self.timeLimit :
                    self.limitReach = 1
                    break
                te = 1
                board.update(old_move, chosen, flag)
                if(board.find_terminal_state()[0] == 'o'):
                    nodeVal = -1*self.termVal,chosen
                    board.block_status = copy.deepcopy(tmp)
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    break
                if(board.find_terminal_state()[0] == 'x'):
                    board.block_status = copy.deepcopy(tmp)
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    continue
                if(board.find_terminal_state()[0] == 'NONE'):
                    x,d,o,tmp1 = 0,0,0,0
                    for i2 in range(4):
                        for j2 in range(4):
                            if board.block_status[i2][j2] == 'x':
                                x = x + 1
                            elif board.block_status[i2][j2] == 'o':
                                o = o + 1
                            elif board.block_status[i2][j2] == 'd':
                                d = d + 1
                    if(x == o):
                        tmp1 = 0
                    elif(x < o):
                        tmp1 = -INFINITY/2 - 10 * (o-x)
                    elif (x > o):
                        tmp1 = INFINITY/2 + 10 * (x-o)
                elif(depth >= self.limit):
                    tmp1 = self.heuristic(board)
                else:
                    tmp1 = self.alphaBeta(board, chosen, new, depth+1, alpha, b)[0]
                if(nodeVal[0] > tmp1):
                    nodeVal = tmp1,chosen
                board.block_status = copy.deepcopy(tmp)
                board.board_status[chosen[0]][chosen[1]] = '-'
                if b > tmp1:
                    b = tmp1
                if alpha >= nodeVal[0] :
                    break
            del(tmp)

        if(nodeVal[0] < beta and nodeVal[0] > alpha):
            self.trans[hashval] = [nodeVal[0],nodeVal[0]]
            return nodeVal
        if(nodeVal[0] >= beta):
            self.trans[hashval] = [nodeVal[0],INFINITY]
            return nodeVal
        if(nodeVal[0] <= alpha):
            self.trans[hashval] = [-INFINITY,nodeVal[0]]
            return nodeVal

    def mtd(self,board,old_move,flag,depth,f):
        INFINITY = 1e10
        lowerbound = -INFINITY
        upperbound = INFINITY
        g = f
        while(lowerbound<upperbound):
            if g <= (lowerbound + 1):
                b = lowerbound + 1
            else:
                b = g

            tmp = self.alphaBeta(board,old_move,flag,depth,b-1,b)
            g = tmp[0]
            if datetime.datetime.utcnow() - self.begin >= self.timeLimit :
                self.limitReach = 1
                break
            if(tmp[0] >= b ):
                lowerbound = g
            elif(tmp[0] < b):
                upperbound = g
        return tmp

    def move(self, board, old_move, flag):
    	self.begin = datetime.datetime.utcnow()
        self.limitReach = 0
        INFINITY = 1e10
        flag1 = 1
        flag2 = 0
        self.marker = flag
        own = self.marker
        opp = self.getMarker(own)
        self.trans.clear()
        toret1 = board.find_valid_move_cells(old_move)[0]
        global toret
        toret = []
        toret.append(0)
        toret.append(0)
        temp_row = [['-'] * 4 for i in range(4)]
        temp_col = [['-'] * 4 for i in range(4)]
        temp_dia = [['-'] * 4 for i in range(4)]
        b_x = old_move[0]%4
        b_y = old_move[1]%4
        temp_block = copy.deepcopy(board.block_status)
        for i in xrange(4):
            for j in xrange(4):
                temp_row[i][j] = board.board_status[4*b_x + i][4*b_y + j]
        for i in xrange(4):
            for j in xrange(4):
                temp_col[i][j] = board.board_status[4*b_x + j][4*b_y + i]
        for i in xrange(4):
            if i==0:
                x = 0
                y = 1
            elif i==1:
                x = 0
                y = 2
            elif i==2:
                x = 1
                y = 1
            else:
                x = 1
                y = 2
            for j in xrange(4):
                if j==0:
    				x1 = 0
    				y1 = 0
                elif j==1:
    				x1 = 1
    				y1 = -1
                elif j==2:
    				x1 = 2
    				y1 = 0
                else:
    				x1 = 1
    				y1 = 1
                temp_dia[i][j] = board.board_status[4*b_x + x+x1][4*b_y + y+y1]
        nb_x = 4*b_x
        nb_y = 4*b_y
        if temp_block[old_move[0]/4][old_move[1]/4] == '-':
            if [own,'-',own,own] in temp_row:
	            ind = temp_row.index([own,'-',own,own])
	            toret[0] = nb_x + ind
	            toret[1] = nb_y + 1
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif [own,own,'-',own] in temp_row :
	            ind = temp_row.index([own,own,'-',own])
	            toret[0] = nb_x + ind
	            toret[1] = nb_y + 2
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif [own,own,own,'-'] in temp_row :
	            ind = temp_row.index([own,own,own,'-'])
	            toret[0] = nb_x + ind
	            toret[1] = nb_y + 3
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif ['-',own,own,own] in temp_row :
	            ind = temp_row.index(['-',own,own,own])
	            toret[0] = nb_x + ind
	            toret[1] = nb_y
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif [own,'-',own,own] in temp_col :
	            ind = temp_col.index([own,'-',own,own])
	            toret[0] = nb_x + 1
	            toret[1] = nb_y + ind
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif [own,own,'-',own] in temp_col :
	            ind = temp_col.index([own,own,'-',own])
	            toret[0] = nb_x + 2
	            toret[1] = nb_y + ind
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif [own,own,own,'-'] in temp_col :
	            ind = temp_col.index([own,own,own,'-'])
	            toret[0] = nb_x + 3
	            toret[1] = nb_y + ind
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif ['-',own,own,own] in temp_col :
	            ind = temp_col.index(['-',own,own,own])
	            toret[0] = nb_x
	            toret[1] = nb_y+ ind
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif [own,'-',own,own] in temp_dia :
                ind = temp_dia.index([own,'-',own,own])
                t = ind % 2
                if ind < 2:
                    toret[0] = nb_x + 1
                    toret[1] = nb_y + ind + 1 - 1
                else :
                    toret[0] = nb_x + 1 + 1
                    toret[1] = nb_y + t + 1 - 1
                if(temp_block[toret[0]/4][toret[1]/4] == '-'):
                    flag2 = 1
            elif [own,own,'-',own] in temp_dia:
                ind = temp_dia.index([own,own,'-',own])
                t=ind%2
                if ind < 2:
                    toret[0] = nb_x + 2
                    toret[1] = nb_y + ind + 1
                else :
                     toret[0] = nb_x + 2 + 1
                     toret[1] = nb_y + t + 1
                if(temp_block[toret[0]/4][toret[1]/4] == '-'):
                    flag2 = 1
            elif [own,own,own,'-'] in temp_dia:
                ind = temp_dia.index([own,own,own,'-'])
                t = ind % 2
                if ind < 2 :
                    toret[0] = nb_x + 1
                    toret[1] = nb_y + ind + 2
                else :
                    toret[0] = nb_x + 2
                    toret[1] = nb_y + t + 2
                if(temp_block[toret[0]/4][toret[1]/4] == '-'):
                    flag2 = 1
            elif ['-',own,own,own] in temp_dia:
                ind = temp_dia.index(['-',own,own,own])
                t = ind % 2
                if ind < 2:
                    toret[0] = nb_x
                    toret[1] = nb_y + ind + 1
                else :
                     toret[0] = nb_x + 1
                     toret[1] = nb_y + t + 1
                if(temp_block[toret[0]/4][toret[1]/4] == '-'):
                    flag2 = 1
            elif [opp,'-',opp,opp] in temp_row :
	            ind = temp_row.index([opp,'-',opp,opp])
	            toret[0] = nb_x + ind
	            toret[1] = nb_y + 1
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif [opp,opp,'-',opp] in temp_row :
	            ind = temp_row.index([opp,opp,'-',opp])
	            toret[0] = nb_x + ind
	            toret[1] = nb_y + 2
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif [opp,opp,opp,'-'] in temp_row :
	            ind = temp_row.index([opp,opp,opp,'-'])
	            toret[0] = nb_x + ind
	            toret[1] = nb_y + 3
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif ['-',opp,opp,opp] in temp_row :
	            ind = temp_row.index(['-',opp,opp,opp])
	            toret[0] = nb_x + ind
	            toret[1] = nb_y
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif [opp,'-',opp,opp] in temp_col :
	            ind = temp_col.index([opp,'-',opp,opp])
	            toret[0] = nb_x + 1
	            toret[1] = nb_y + ind
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif [opp,opp,'-',opp] in temp_col :
	            ind = temp_col.index([opp,opp,'-',opp])
	            toret[0] = nb_x + 2
	            toret[1] = nb_y + ind
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif [opp,opp,opp,'-'] in temp_col :
	            ind = temp_col.index([opp,opp,opp,'-'])
	            toret[0] = nb_x + 3
	            toret[1] = nb_y + ind
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif ['-',opp,opp,opp] in temp_col :
	            ind = temp_col.index(['-',opp,opp,opp])
	            toret[0] = nb_x
	            toret[1] = nb_y+ ind
	            if(temp_block[toret[0]/4][toret[1]/4] == '-'):
	                flag2 = 1
            elif [opp,'-',opp,opp] in temp_dia :
                ind = temp_dia.index([opp,'-',opp,opp])
                t = ind % 2
                if ind < 2:
                    toret[0] = nb_x + 1
                    toret[1] = nb_y + ind + 1 - 1
                else :
                    toret[0] = nb_x + 1 + 1
                    toret[1] = nb_y + t + 1 - 1
                if(temp_block[toret[0]/4][toret[1]/4] == '-'):
                    flag2 = 1
            elif [opp,opp,'-',opp] in temp_dia:
                ind = temp_dia.index([opp,opp,'-',opp])
                t=ind%2
                if ind < 2:
                    toret[0] = nb_x + 2
                    toret[1] = nb_y + ind + 1
                else :
                     toret[0] = nb_x + 2 + 1
                     toret[1] = nb_y + t + 1
                if(temp_block[toret[0]/4][toret[1]/4] == '-'):
                    flag2 = 1
            elif [opp,opp,opp,'-'] in temp_dia:
                ind = temp_dia.index([opp,opp,opp,'-'])
                t = ind % 2
                if ind < 2 :
                    toret[0] = nb_x + 1
                    toret[1] = nb_y + ind + 2
                else :
                    toret[0] = nb_x + 2
                    toret[1] = nb_y + t + 2
                if(temp_block[toret[0]/4][toret[1]/4] == '-'):
                    flag2 = 1
            elif ['-',opp,opp,opp] in temp_dia:
                ind = temp_dia.index(['-',opp,opp,opp])
                t = ind % 2
                if ind < 2:
                    toret[0] = nb_x
                    toret[1] = nb_y + ind + 1
                else :
                     toret[0] = nb_x + 1
                     toret[1] = nb_y + t + 1
                if(temp_block[toret[0]/4][toret[1]/4] == '-'):
                    flag2 = 1
            else:
                flag1 = 0
                for i in xrange(3,100):
                    self.limit = i
                    self.trans.clear()
                    prune_ans = self.alphaBeta(board, old_move, flag, 1, -INFINITY, INFINITY)
                    getval = prune_ans[1]
                    if(self.limitReach != 0):
                        break
                    elif(self.limitReach == 0):
                        toret1 = getval
        else:
            flag1 = 0
            for i in xrange(3,100):
                self.limit = i
                self.trans.clear()
                prune_ans = self.alphaBeta(board, old_move, flag, 1, -INFINITY, INFINITY)
                getval = prune_ans[1]
                if(self.limitReach != 0):
                    break
                elif(self.limitReach == 0):
                    toret1 = getval
        if flag1 == 1 and flag2 == 0:
            flag1 = 0
            for i in xrange(3,100):
                self.limit = i
                self.trans.clear()
                prune_ans = self.alphaBeta(board, old_move, flag, 1, -INFINITY, INFINITY)
                getval = prune_ans[1]
                if(self.limitReach != 0):
                    break
                elif(self.limitReach == 0):
                    toret1 = getval

        if flag1 == 0 and flag2 == 0:
            return toret1[0], toret1[1]
        elif flag1 == 1 and flag2 == 1:
            return toret[0],toret[1]
