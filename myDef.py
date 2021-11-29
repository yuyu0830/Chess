def small_eq(a, b):
    return a if a <= b else b

def isin(target, start, end):
    if type(target) == type([]):
        for i in range(len(target)):
            if target[i] > start and target[i] < end:
                return False
        return True
    else:
        return True if target > start and target < end else False

def switch(target, lis1, lis2):
    return lis2[lis1.index(target)]

def position(pos):
    try:
        a = [ord(pos[0]) - 96, 9 - int(pos[1])]
        return a
    except:
        return

def un_position(pos):
    return [chr(pos[0] + 96), 9 - pos[1]]

def change_NtoP(num):
    return switch(num, [1, 2, 3, 4, 5, 6], ['King', 'Queen', 'Rook', 'Bishop', 'knight', 'Pawn'])
