import pygame as pg

SIZE = [1200, 1000]
WIDTH = 800
HEIGHT = 800
TITLE = "Chess"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
DARKGRAY = (100, 100, 100)

def mouse(pos):
    return [pos[0] // 100, pos[1] // 100]

def isin(v, a, b):
    if v > a and v < b: return True
    return False

def inmap(lis):
    return [lis[0] - 2, lis[1] - 1]

class game:
    def __init__(self):
        #Pygame Setting
        pg.init()
        self.screen = pg.display.set_mode(SIZE)
        self.title = pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("arial", 48, True, False)
        self.s_font = pg.font.SysFont("arial", 20, True, False)
        self.pieces = [[], []] #White, Black, King, Queen, Rook, Bishop, Knight, Pawn
        for idx, color in enumerate(["WHITE_", "BLACK_"]):
            for piece in ["KING", "QUEEN", "ROOK", "BISHOP", "KNIGHT", "PAWN"]:
                self.pieces[idx].append(pg.transform.scale(pg.image.load('piece/' + color + piece + '.png'), [100, 100]))
        
        #Chess Setting
        self.selected = [False, 0, 0]
        self.running = True
        self.mouse_pos = [0, 0]
        self.pressed = False
        self.board = [[[0, 0]]*8 for _ in range (8)] #color, pieces, x, y
        self.turn = 1 #1 = White, 2 = Black
        self.movable = []
        self.attackable = []
        self.dead_piece = [[], []]
        self.promotion = [0, -1]
        for idx, v in enumerate([2, 4, 3, 1, 0, 3, 4, 2]):
            self.board[idx][0] = [2, v] #minor piece
            self.board[idx][7] = [1, v]
            self.board[idx][1] = [2, 5] #pawn
            self.board[idx][6] = [1, 5]
        self.board[2][2] = [1, 5]
        self.board[5][5] = [2, 5]
    def run(self):
        #Mouse
        self.mouse_pos = pg.mouse.get_pos()
        self.pos = mouse(self.mouse_pos)
        self.mouse_pressed = pg.mouse.get_pressed()

        #Selected Board 
        if pg.mouse.get_pressed()[0] == True:
            if self.pressed == False:
                self.pressed = True
                if self.promotion[1] != -1: #promotion on
                    if self.promotion[1] == 0: a, b, c = 1, 5, 1
                    else: a, b, c = 3, 7, 2
                    if self.pos[0] - 2 == self.promotion[0] and self.pos[1] - 1 in range(a, b):
                        self.board[self.promotion[0]][self.promotion[1]] = [c, self.pos[1] - a]
                        self.promotion[1] = -1
                        self.turn = 2 if self.turn == 1 else 1
                else:
                    if self.selected[0]: #if selected
                        if inmap(self.pos) in self.movable or inmap(self.pos) in self.attackable: #move
                            self.move(inmap(self.selected[1:3]), inmap(self.pos))
                            self.reset_select()
                        else: #reset select
                            self.reset_select()
                    elif isin(self.pos[0], 1, 10) and isin(self.pos[1], 0, 9):
                        if self.board[self.pos[0] - 2][self.pos[1] - 1][0] == self.turn:
                            self.selected = [True, self.pos[0], self.pos[1]]
                            self.move_calculation()
        else:
            self.pressed = False

        self.draw()
        pg.display.update()

    def draw(self):
        #Draw Board
        self.screen.fill(WHITE)
        for i in range(2, 10):
            for j in range(1, 9):
                if i%2 == (j + 1)%2:
                    pg.draw.rect(self.screen, GRAY, [i*100, j*100, 100, 100])
        pg.draw.rect(self.screen, BLACK, [200, 0, 1000, 100])
        pg.draw.rect(self.screen, BLACK, [0, 0, 200, 902.5])
        pg.draw.rect(self.screen, BLACK, [200, 100, 800, 800], 5)
        pg.draw.rect(self.screen, RED, [0, 900 if self.turn == 1 else 0, 1200, 100])

        #Draw Piece
        for x in range(8):
            for y in range(8):
                temp = self.board[x][y]
                if temp[0] != 0:
                    self.screen.blit(self.pieces[temp[0] - 1][temp[1]], [(x + 2)*100, (y + 1)*100])
            
        #Draw Dead Piece
        for pieces in self.dead_piece:
            for idx, v in enumerate(pieces):
                self.screen.blit(self.pieces[v[0] - 1][v[1]], [0 if v[0] == 2 else 1000, 100 + (idx * 100)])

        #Draw Mouse Location
        if isin(self.pos[0], 1, 10) and isin(self.pos[1], 0, 9):
            pg.draw.rect(self.screen, BLACK, [self.pos[0]*100, self.pos[1]*100, 100, 100], 4)

        #Draw Movable Board
        for x, y in self.movable:
            pg.draw.circle(self.screen, DARKGRAY, [(x + 2)*100 + 50, (y + 1)*100 + 50], 20)
        for x, y in self.attackable:
            pg.draw.rect(self.screen, RED, [(x + 2)*100, (y + 1)*100, 100, 100], 5)
            
        #Draw Selected Board
        if self.selected[0] == True:
            pg.draw.rect(self.screen, GREEN, [self.selected[1]*100, self.selected[2]*100, 100, 100], 5)

        #Draw Promotion Select Box
        if self.promotion[1] != -1:
            if self.promotion[1] == 0:
                pg.draw.rect(self.screen, WHITE, [(self.promotion[0] + 2)*100, (self.promotion[1] + 2)*100, 100, 400])
                pg.draw.rect(self.screen, BLACK, [(self.promotion[0] + 2)*100, (self.promotion[1] + 2)*100, 100, 400], 5)
                for i in range(1, 5):
                    self.screen.blit(self.pieces[0][i], [(self.promotion[0] + 2)*100, (i + 1)*100])
            else:
                pg.draw.rect(self.screen, WHITE, [(self.promotion[0] + 2)*100, (self.promotion[1] - 3)*100, 100, 400])
                pg.draw.rect(self.screen, BLACK, [(self.promotion[0] + 2)*100, (self.promotion[1] - 3)*100, 100, 400], 5)
                for i in range(1, 5):
                    self.screen.blit(self.pieces[1][i], [(self.promotion[0] + 2)*100, (i + 3)*100])
        

    def move_calculation(self):
        pos = [self.selected[1] - 2, self.selected[2] - 1]
        piece = self.board[pos[0]][pos[1]][1]
        enemy = 2 if self.turn == 1 else 1
        if piece == 0: #king
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if isin(pos[0] + i, -1, 8) and isin(pos[1] + j, -1, 8):
                        if self.board[pos[0] + i][pos[1] + j][0] == 0: #Normal move
                            self.movable.append([pos[0] + i, pos[1] + j])
                        elif self.board[pos[0] + i][pos[1] + j][0] == enemy: #Attackable
                            self.attackable.append([pos[0] + i, pos[1] + j])

        elif piece == 4: #Knight
            for i, j in [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, 2], [1, 2], [-1, -2], [1, -2]]:
                if isin(pos[0] + i, -1, 8) and isin(pos[1] + j, -1, 8):
                    if self.board[pos[0] + i][pos[1] + j][0] == 0: #Normal move
                        self.movable.append([pos[0] + i, pos[1] + j])
                    elif self.board[pos[0] + i][pos[1] + j][0] == enemy: #Attackable
                        self.attackable.append([pos[0] + i, pos[1] + j])

        elif piece == 5: #Pawn
            direction = -1 if self.turn == 1 else 1
            first = 6 if self.turn == 1 else 1
            if self.board[pos[0]][pos[1] + direction][0] == 0: #Normal move
                self.movable.append([pos[0], pos[1] + direction])
                if pos[1] == first and self.board[pos[0]][pos[1] + (direction * 2)][0] == 0: #First move
                    self.movable.append([pos[0], pos[1] + (direction * 2)])
            for i in [-1, 1]: #Attackable
                if isin(pos[0] + i, -1, 8):
                    if self.board[pos[0] + i][pos[1] + direction][0] == enemy:
                        self.attackable.append([pos[0] + i, pos[1] + direction])
            

        else:
            if piece != 3: #Queen, Rook Straight
                for x, y in [[1, 0], [0, 1]]:
                    for direction in [-1, 1]:
                        temp = [pos[0] + (direction * x), pos[1] + (direction * y)]
                        while isin(temp[y], -1, 8):
                            if self.board[temp[0]][temp[1]][0] == 0:
                                self.movable.append([temp[0], temp[1]])
                                temp[0] += (direction * x)
                                temp[1] += (direction * y)
                            elif self.board[temp[0]][temp[1]][0] == enemy:
                                self.attackable.append([temp[0], temp[1]])
                                break
                            else:
                                break

            if piece != 2: #Queen, Bishop Diagonal
                for x, y in [[1, 1], [-1, 1], [1, -1], [-1, -1]]:
                    temp = [pos[0] + x, pos[1] + y]
                    while isin(temp[0], -1, 8) and isin(temp[1], -1, 8):
                        if self.board[temp[0]][temp[1]][0] == 0:
                            self.movable.append([temp[0], temp[1]])
                            temp[0] += x
                            temp[1] += y
                        elif self.board[temp[0]][temp[1]][0] == enemy:
                            self.attackable.append([temp[0], temp[1]])
                            break
                        else:
                            break
    
    def move(self, org, des):
        enemy = 2 if self.turn == 1 else 1
        if self.board[des[0]][des[1]][0] == enemy:
            self.dead_piece[self.board[des[0]][des[1]][0] - 1].append(self.board[des[0]][des[1]])
        self.board[des[0]][des[1]] = self.board[org[0]][org[1]]
        self.board[org[0]][org[1]] = [0, 0]

        piece = self.board[des[0]][des[1]] #Pawn promotion
        if (piece[0] == 1 and piece[1] == 5 and des[1] == 0) or (piece[0] == 2 and piece[1] == 5 and des[1] == 7):
            self.promotion = des
            print(self.promotion)
        else:
            self.turn = 2 if self.turn == 1 else 1


    def reset_select(self):
        self.selected[0] = False
        self.movable = []
        self.attackable = []

g = game()
while g.running:
    g.clock.tick(20)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            g.running = False
    g.run()