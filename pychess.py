from myDef import *

#add En passant
#add Checkmate check
#menu to see record
#turn color to 0, 1

class game:
    def __init__(self):
        temp = []
        self.board = [] #[x, abcd...][y, 1234...]
        for i in range(10):     #[0] simbol [1] pieces color [2] pieces class
            for j in range(10): #[3] serial number [4] movable squares
                temp.append([' ']) #class 1. King 2. Queen 3. Rook 4. Bishop 5. knight 6. Pawn
            self.board.append(temp)
            temp = []
        self.sub_board = [['  ']*10 for _ in range (10)] #sub output
        self.turn_color = 1
        self.death_pieces = [[], []]
        self.movable_squares = [[], []]
        self.record = []
        self.record_player = []
        self.main_cursor_point = []
        self.sub_cursor_point = []
        self.king_position = [[5, 8], [5, 1]] #white, black
        self.temp = []
        self.castling = [1, 1, 1, 1]
        self.simbols = [['♚ ', '♔ '], ['♛ ', '♕ '], ['♜ ', '♖ '], ['♝ ', '♗ '], ['♞ ', '♘ '], ['♟', '♙ ']]
        self.squares = ['■', '□']
        self.cursor = ['▼', '▽']
        setting = [3, 5, 4, 2, 1, 4, 5, 3, 3, 7, 5, 2, 1, 6, 8, 4]
        
        for i in range(1, 9): #board setting
            self.board[i][8] = [self.simbols[setting[i - 1] - 1][0], 1, setting[i - 1], setting[i + 7], []] #minor pieces
            self.board[i][1] = [self.simbols[setting[i - 1] - 1][1], 2, setting[i - 1], setting[i + 7], []]
            self.board[i][7] = [self.simbols[5][0], 1, 6, i + 8, []] #pawn
            self.board[i][2] = [self.simbols[5][1], 2, 6, i + 8, []]
            for j in [0, 9]: 
                self.board[i][j] = [chr(96 + i) + ' ']
                self.board[j][i] = [9 - i]
                self.sub_board[j][i] = ' '

            for j in range(1, 9): #board square setting
                if self.board[i][j][0] == ' ':
                    if (i % 2 != 0 and j % 2 != 0) or (i % 2 == 0 and j % 2 == 0):
                        self.board[i][j] = [self.squares[0], 0]
                    else:
                        self.board[i][j] = [self.squares[1], 0]
                        
        del setting
        del temp
        
    def running(self):
        while True:
            self.movable()
            while True:
                temp = self.turn()
                if type(temp) != type(None):
                    break
            self.turn_color = 1 if self.turn_color == 2 else 2
            self.record.append([temp[0], temp[1]])
            self.record_player.append([un_position(temp[0]), un_position(temp[1])])
            check = self.check()
            if type(check) == type(int()):
                return check, self.record_player
            temp = ''

    def turn(self):
        col = 'White' if self.turn_color == 1 else 'Black'
        while True:
            if self.main_cursor_point != []:
                self.clean_mark()
            self.draw()
            print('{}. {} turn.'.format(len(self.record) + 1, col))
            pos, sel = self.select()
            self.draw()
            piece_class = change_NtoP(self.board[pos[0]][pos[1]][2])
            print("{} {} selected.".format(sel, piece_class))
            pos2, nex_mov = self.choose(pos)
            if type(pos2) == type(0):
                continue
        
            while True: #last check part
                self.draw()
                last_check = input("{} {} move to {}?\n(y/n) : ".format(sel, piece_class, nex_mov))
                if last_check == 'y' or last_check == 'Y':
                    self.move(pos, pos2)
                    return pos, pos2
                elif last_check == 'n' or last_check == 'N':
                    last_check = ''
                    break
                else:
                    print("Error : Please input y or n")


########################################
############## check part ##############
    def check(self):
        for i in self.king_position:
            if self.board[i[0]][i[1]][2] != 1:
                return self.board[i[0]][i[1]][1]
        
                    
#######################################
############## draw part ##############
    def draw(self):
        print('\n')
        for i in range(len(self.board)):
            for j in range(len(self.sub_board[i])):
                print(self.sub_board[j][i], end=' ')
            print('')
            for j in range(len(self.board[i])):
                print(self.board[j][i][0], end=' ')
            print('')
        print('')


#########################################
############## select part ##############
    def select(self):
        while True:
            sel = input("Select : ")
            if len(sel) == 2:
                pos = position(sel)
                if pos != None:
                    if isin([pos[0], pos[1]], 0, 9):
                        print("Input Error : Please input in a - h, 1 - 8")
                        continue
                    elif self.board[pos[0]][pos[1]][1] != self.turn_color:
                        print("Error : Please select own piece")
                        continue
                    elif len(self.board[pos[0]][pos[1]][4]) == 0:
                        print("Error : This piece can't move!")
                        continue
                    else:
                        self.set_curser(pos)
                        return pos, sel
                else:
                    print("Input Error : Please input in a - h, 1 - 8")
            else:
                print("Input Error : Please input in a - h, 1 - 8")

    def choose(self, pos):
        while True: #choose move square part
            nex_mov = input("Move(no input to cancle select) : ")
            if nex_mov == '':
                print("Cancle select")
                return 0, 0
            elif len(nex_mov) == 2:
                pos2 = position(nex_mov)
                if pos2 != None:
                    if pos2 in self.board[pos[0]][pos[1]][4]:
                        return pos2, nex_mov
                    else:
                        print("Error : There is not movable square.")
                else:
                    print("Input Error : Please input in a - h, 1 - 8")
            else:
                print("Error : There is not movable square.")
                
    def promotion(self):
        print("Choose class of piece to upgrade your Pawn!")
        while True:
            select = input("\n1. Queen\n2. Rook\n3. Bishop\n4. Knight\nChoose : ")
            if select in ['1', '2', '3', '4']:
                return int(select)
            print("Wrong input. Please input again.")
            
#######################################################
############## Calculate movable squares ##############
    def movable(self):
        temp = []
        temp2 = []
        for i in range(1, 9):
            for j in range(1, 9):
                if self.board[i][j][0] not in self.squares: #Is it piece?
                    if self.board[i][j][2] in [2, 3, 4]:
                        temp = self.move_cal_straight([i, j], self.board[i][j][2])
                    else:
                        temp = self.move_cal_other([i, j], self.board[i][j][2])
                    
                    self.board[i][j][4] = temp
                    temp2.append(temp)
                    temp = []
                    
    def move_cal_straight(self, pos, cla):
        temp = []
        xmym = [small_eq(pos[0], pos[1]), 1]
        xpym = [small_eq(9 - pos[0], pos[1]), 2]
        xmyp = [small_eq(pos[0], 9 - pos[1]), 3]
        xpyp = [small_eq(9 - pos[0], 9 - pos[1]), 4]
        xm = [pos[0], 5]
        xp = [9 - pos[0], 6]
        ym = [pos[1], 7]
        yp = [9 - pos[1], 8]

        len_list = switch(cla, [2, 3, 4], [[xmym, xpym, xmyp, xpyp, xm, xp, ym, yp], [xm, xp, ym, yp], [xmym, xpym, xmyp, xpyp]])
            
        for length in len_list:
            for i in range(1, length[0]): 
                j = switch(length[1], [1, 2, 3, 4, 5, 6, 7, 8], [-i, i, -i, i, -i, i, 0, 0])
                k = switch(length[1], [1, 2, 3, 4, 5, 6, 7, 8], [-i, -i, i, i, 0, 0, -i, i])
                    
                if self.board[pos[0] + j][pos[1] + k][1] == 0:
                    temp.append([pos[0] + j, pos[1] + k])
                elif self.board[pos[0] + j][pos[1] + k][1] == self.board[pos[0]][pos[1]][1]:
                    break
                elif self.board[pos[0] + j][pos[1] + k][1] != self.board[pos[0]][pos[1]][1]:
                    temp.append([pos[0] + j, pos[1] + k])
                    break

        if cla == 3: #castling
            temp_bool = True
            if pos in [[1, 1], [1, 8], [8, 1], [8, 8]]: 
                temp_num = switch(pos, [[1, 1], [1, 8], [8, 1], [8, 8]], [0, 1, 2, 3])
                if self.castling[temp_num] == 1:
                    if temp_num < 2: #left side Rook
                        t1, t2, t3 = 2, 5, 1 #2, 3, 4
                    else: #Right side Rook
                        t1, t2, t3 = 7, 5, -1 #7, 6
                    for i in range(t1, t2, t3):
                        if self.board[i][pos[1]][1] != 0:
                            temp_bool = False
                if temp_bool == True:
                    num = 0 if temp_num % 2 != 0 else 1
                    temp.append(self.king_position[num])
        return temp

    def move_cal_other(self, pos, cla):
        temp = []
        if cla == 1: #King
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if isin(pos[0] + i, 0, 9) and isin(pos[1] + j, 0, 9) and self.board[pos[0] + i][pos[1] + j][1] != self.turn_color:
                        temp.append([pos[0] + i, pos[1] + j])

        elif cla == 5: #Knight
            for i, j in [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, 2], [1, 2], [-1, -2], [1, -2]]:
                if isin(pos[0] + i, 0, 9) and isin(pos[1] + j, 0, 9) and self.board[pos[0] + i][pos[1] + j][1] != self.turn_color:
                    temp.append([pos[0] + i, pos[1] + j])

        elif cla == 6: #Pawn
            enemy = 1 if self.turn_color == 2 else 2
            direction = -1 if self.turn_color == 1 else 1
            if (self.turn_color == 1 and pos[1] == 7) or (self.turn_color == 2 and pos[1] == 2): #first move
                if self.board[pos[0]][pos[1] + direction][1] == 0:
                    temp.append([pos[0], pos[1] + direction])
                    if self.board[pos[0]][pos[1] + (direction * 2)][1] == 0:
                        temp.append([pos[0], pos[1] + (direction * 2)])

            else: #normal move
                if self.board[pos[0]][pos[1] + direction][1] == 0:
                    temp.append([pos[0], pos[1] + direction])

            for i in [-1, 1]: #attack
                if isin(pos[0] + i, 0, 9):
                    if self.board[pos[0] + i][pos[1] + direction][1] == enemy:
                        temp.append([pos[0] + i, pos[1] + direction])

        return temp

#######################################
############## move part ##############

    def move(self, pos1, pos2): # move part, 1 piece, 2 place
        if self.board[pos1[0]][pos1[1]][2] == 1: #king's position change
            self.king_position[self.turn_color - 1] = pos2
            num = [0, 2] if self.turn_color == 0 else [1, 3] #Can't Castling when after king move
            for i in num:
                if self.castling[i] == 1:
                    self.castling[i] = 0
        if self.board[pos1[0]][pos1[1]][2] == 3 and pos1 in [[1, 1], [1, 8], [8, 1], [8, 8]]:
            temp_num = switch(pos1, [[1, 1], [1, 8], [8, 1], [8, 8]], [0, 1, 2, 3])
            if self.castling[temp_num] == 1: #Castling
                self.castling[temp_num] = 0
                if self.board[pos2[0]][pos2[1]][2] == 1 and self.board[pos1[0]][pos1[1]][1] == self.board[pos2[0]][pos2[1]][1]:
                    if pos1[0] == 1: #Left side
                        self.board[pos2[0] - 2][pos2[1]] = self.board[pos2[0]][pos2[1]]
                        self.board[pos2[0] - 1][pos2[1]] = self.board[pos1[0]][pos1[1]]
                        self.king_position[self.turn_color - 1] = [pos2[0] - 2, pos2[1]]
                    else: #Right side
                        self.board[pos2[0] + 2][pos2[1]] = self.board[pos2[0]][pos2[1]]
                        self.board[pos2[0] + 1][pos2[1]] = self.board[pos1[0]][pos1[1]]
                        self.king_position[self.turn_color - 1] = [pos2[0] + 2, pos2[1]]
                    self.board[pos2[0]][pos2[1]] = [self.squares[0] if (pos1[0] % 2 != 0 and pos1[1] % 2 != 0) or (pos1[0] % 2 == 0 and pos1[1] % 2 == 0) else self.squares[1], 0]
                    self.board[pos1[0]][pos1[1]] = [self.squares[0] if (pos1[0] % 2 != 0 and pos1[1] % 2 != 0) or (pos1[0] % 2 == 0 and pos1[1] % 2 == 0) else self.squares[1], 0]
                    return
        if self.board[pos1[0]][pos1[1]][2] == 6: # Pawn promotion
            if (pos2[1] == 1 and self.turn_color == 1) or (pos2[1] == 8 and self.turn_color == 2): #Pawn color and position??
                temp = self.promotion()
                temp1 = self.board[pos1[0]][pos1[1]][3]
                self.board[pos1[0]][pos1[1]] = [self.simbols[temp][self.turn_color - 1], self.turn_color, temp + 1, temp1, []]
            
        
        if self.board[pos2[0]][pos2[1]][0] in self.squares:
            self.board[pos2[0]][pos2[1]] = self.board[pos1[0]][pos1[1]]

        else:
            self.death_pieces[self.turn_color - 1].append(self.board[pos2[0]][pos2[1]][0])
            self.board[pos2[0]][pos2[1]] = self.board[pos1[0]][pos1[1]]

        self.board[pos1[0]][pos1[1]] = [self.squares[0] if (pos1[0] % 2 != 0 and pos1[1] % 2 != 0) or (pos1[0] % 2 == 0 and pos1[1] % 2 == 0) else self.squares[1], 0]


############################################
############## curser setting ##############
    def clean_mark(self):
        self.sub_board[self.main_cursor_point[0]][self.main_cursor_point[1]] = '  '
        for i in range(len(self.sub_cursor_point)):
            self.sub_board[self.sub_cursor_point[i][0]][self.sub_cursor_point[i][1]] = '  '
        self.main_cursor_point = []
        self.sub_cursor_point = []
        
    def set_curser(self, pos):
        self.sub_board[pos[0]][pos[1]] = self.cursor[0]
        self.main_cursor_point = pos
        for i in range(len(self.board[pos[0]][pos[1]][4])):
            self.sub_cursor_point.append(self.board[pos[0]][pos[1]][4][i])
            self.sub_board[self.sub_cursor_point[i][0]][self.sub_cursor_point[i][1]] = self.cursor[1]
            
g = game()

chess = g.running()
print("{} player Win!".format(chess[0]))
print(chess[1])
print(g.king_position)
a = input()
