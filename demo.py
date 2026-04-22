from pyscript import web
from pyscript import when
import time


class Chessboard():
    class Board():
        def __init__(self, content=[]):
            self.content = content
            if content == []: self.reset()
        
        def reset(self):
            self.content = [
                ["B-ROOK", "B-KNIGHT", "B-BISHOP", "B-QUEEN", "B-KING", "B-BISHOP", "B-KNIGHT", "B-ROOK"],
                ["B-PAWN", "B-PAWN", "B-PAWN", "B-PAWN","B-PAWN", "B-PAWN", "B-PAWN", "B-PAWN"],
                ["EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY"],
                ["EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY"],
                ["EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY"],
                ["EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY"],
                ["W-PAWN", "W-PAWN", "W-PAWN", "W-PAWN","W-PAWN", "W-PAWN", "W-PAWN", "W-PAWN"],
                ["W-ROOK", "W-KNIGHT", "W-BISHOP", "W-QUEEN", "W-KING", "W-BISHOP", "W-KNIGHT", "W-ROOK"]
            ]
        
        def set_tile(self, array_coord, peice):
            self.reverse()
            self.content[array_coord[1]][array_coord[0]] = peice
            self.reverse()


        def get_pieces(self, color):
            pieces = []
            for x in range(0, 8):
                for y in  range(0,8):
                    if color+"-" in self.get_tile((x, y)): 
                        pieces.append((self.get_tile((x, y)).replace("W-", "").replace("B-", ""), (x, y)))

            return pieces
        

        def get_tile(self, array_coord):
            self.reverse()
            ret = self.content[array_coord[1]][array_coord[0]]
            self.reverse()
            return ret
        

        def switch(self, start, end):
            z = self.get_tile(start)
            self.set_tile(start, "EMPTY")
            self.set_tile(end, z)


        def inside(self, array_coord):
            if array_coord[1] < 8 and array_coord[1] > -1:
                if array_coord[0] < 8 and array_coord[0] > -1:
                    return True
            return False
        

        def copy(self):
            copy = []
            for row in range(0, 8): copy.append(self.content[row].copy())
            return copy
        

        def reverse(self): self.content.reverse()
        

    def __init__(self):
        self.board = self.Board()
        self.game_turn = "W"
        self.game_history = []



    def reset_game(self):
        self.board.reset()
        self.game_turn = "W"
        self.game_history = []



    # works
    def king_move_legal(self, board, array_coord):
        possible_spaces = []
        king_moves = ((-1, -1), (0, -1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (0, 1))

        """
        if board.get_tile((5, 0)) == "EMPTY" and board.get_tile((6, 0)) == "EMPTY":
            if self.game_turn == "W":
                for i in self.game_history:
                    if i[0] == (7, 0) or i[0] == (4, 0): 
                        possible_spaces.remove("O-O") # have the ring or rook moved
            else:
                for i in self.game_history:
                    if i[0] == (7, 7) or i[0] == (4, 7): 
                        possible_spaces.remove("O-O") # have the ring or rook moved
            
            for i in ((4, 0), (5, 0), (6, 0)):
                if self.under_check(i): 
                    possible_spaces.remove("O-O") # is under check

        
        if move_input == "O-O-O":
            if board.get_tile((1, 0)) == "EMPTY" and board.get_tile((2, 0)) == "EMPTY" and board.get_tile((3, 0)) == "EMPTY":
                if  self.game_turn == "W":
                    for i in self.game_history:
                        if i[0:2] == (0, 7) or i[0:2] == (4, 7): 
                            possible_spaces.remove("O-O-O") # have the ring or rook moved
                else:
                     for i in self.game_history:
                        if i[0:2] == (0, 7) or i[0:2] == (4, 0): 
                            possible_spaces.remove("O-O-O") # have the ring or rook moved

                for i in ((1, 0), (2, 0), (3, 0), (4, 0)):
                    if self.under_check(i): 
                        possible_spaces.remove("O-O-O") # is under check
        """               
        for i in range(0, 8):
            if board.inside((king_moves[i][0]+array_coord[0], king_moves[i][1]+array_coord[1])):
                if board.get_tile((king_moves[i][0]+array_coord[0], king_moves[i][1]+array_coord[1])) == "EMPTY":
                    possible_spaces.append((king_moves[i][0]+array_coord[0], king_moves[i][1]+array_coord[1]))
        
        for i in possible_spaces:  
            if self.game_turn+"-" in board.get_tile((i[0], i[1])) or self.under_check((i[0], i[1])):
                possible_spaces.remove(i)

        return possible_spaces 

    
    # works
    def queen_move_legal(self, board, array_coord):
        possible_spaces = []

        possible_spaces.extend(self.rook_move_legal(board, array_coord))
        possible_spaces.extend(self.bishop_move_legal(board, array_coord))

        return possible_spaces 


    # works
    def rook_move_legal(self, board, array_coord):
        possible_spaces = []
        rook_moves = (
                      ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)),
                      ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)),
                      ((0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)),
                      ((-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0))
                     )
        
        for i in range(0, 4):
            for j in range(0, 7):
                if board.inside((rook_moves[i][j][0]+array_coord[0], rook_moves[i][j][1]+array_coord[1])):
                    if board.get_tile((rook_moves[i][j][0]+array_coord[0], rook_moves[i][j][1]+array_coord[1])) != "EMPTY":   
                        if self.game_turn+"-" in board.get_tile((rook_moves[i][j][0]+array_coord[0], rook_moves[i][j][1]+array_coord[1])):
                            break
                        else:
                            possible_spaces.append((rook_moves[i][j][0]+array_coord[0], rook_moves[i][j][1]+array_coord[1]))
                            break
                    else:
                        possible_spaces.append((rook_moves[i][j][0]+array_coord[0], rook_moves[i][j][1]+array_coord[1]))
        
        return possible_spaces 



    # works
    def pawn_move_legal(self, board, array_coord):
        possible_spaces = []
        if array_coord[1] != 7:
            if board.get_tile((array_coord[0], array_coord[1]+1)) == "EMPTY":
                if array_coord[1] == 1: 
                    if board.get_tile((array_coord[0], array_coord[1]+2)) == "EMPTY":
                        possible_spaces.append((array_coord[0], array_coord[1]+2))# double move
            
                if board.inside((array_coord[0], array_coord[1]+1)):
                    possible_spaces.append((array_coord[0], array_coord[1]+1))# single move 
            
                    
            if board.inside((array_coord[0]-1, array_coord[1]+1)):
                if self.game_turn+"-" not in board.get_tile((array_coord[0]-1, array_coord[1]+1)):
                    if board.get_tile((array_coord[0]-1, array_coord[1]+1)) != "EMPTY":
                        possible_spaces.append((array_coord[0]-1, array_coord[1]+1))# left capture 
            
                    
            if board.inside((array_coord[0]+1, array_coord[1]+1)):
                if self.game_turn+"-" not in board.get_tile((array_coord[0]+1, array_coord[1]+1)):
                    if board.get_tile((array_coord[0]+1, array_coord[1]+1)) != "EMPTY":
                        possible_spaces.append((array_coord[0]+1, array_coord[1]+1))# right capture
        
        else: possible_spaces.append(array_coord)

        return possible_spaces



    # works
    def knight_move_legal(self, board, array_coord):
        possible_spaces = []
        knight_moves = ((-1, -2), (1, -2), (-2, -1), (2, -1), (-2, 1), (2, 1), (-1, 2), (1, 2))

        for i in range(0, 8):
            if board.inside((knight_moves[i][0]+array_coord[0], knight_moves[i][1]+array_coord[1])):
                possible_spaces.append((knight_moves[i][0]+array_coord[0], knight_moves[i][1]+array_coord[1]))
                
        for i in possible_spaces:  
            if self.game_turn+"-" in board.get_tile((i[0], i[1])):
                possible_spaces.remove(i)
                
        return possible_spaces



    # works
    def bishop_move_legal(self, board, array_coord):
        possible_spaces = []
        bishop_moves = (
                        ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)),
                        ((-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)),
                        ((1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)),
                        ((-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7))
                        )
        
        for i in range(0, 4):
            for j in range(0, 7):
                if board.inside((bishop_moves[i][j][0]+array_coord[0], bishop_moves[i][j][1]+array_coord[1])):
                    if board.get_tile((bishop_moves[i][j][0]+array_coord[0], bishop_moves[i][j][1]+array_coord[1])) != "EMPTY":
                        if self.game_turn+"-" in board.get_tile((bishop_moves[i][j][0]+array_coord[0], bishop_moves[i][j][1]+array_coord[1])):
                            break
                        else:
                            possible_spaces.append((bishop_moves[i][j][0]+array_coord[0], bishop_moves[i][j][1]+array_coord[1]))
                            break
                    else:
                        possible_spaces.append((bishop_moves[i][j][0]+array_coord[0], bishop_moves[i][j][1]+array_coord[1]))

         

        return possible_spaces 


    def get_move(self, board, array_coord):
        piece_moves = {
            "ROOK": self.rook_move_legal,
            "KING": self.king_move_legal,
            "KNIGHT": self.knight_move_legal,
            "QUEEN": self.queen_move_legal, 
            "PAWN": self.pawn_move_legal,
            "BISHOP": self.bishop_move_legal
        }
        #if board.get_tile(array_coord) != "EMPTY":
        return piece_moves[board.get_tile(array_coord).replace("W-", "").replace("B-", "")](board, array_coord)
        #else: return []
        
    


    def next_turn(self):
        if self.game_turn == "W": self.game_turn = "B"
        else: self.game_turn = "W"
        self.board.reverse()



    def under_check(self, array_coord):
        if self.game_turn == "W": opposite = "B"
        else: opposite = "W"

        bishop_moves = (
                        ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)),
                        ((-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)),
                        ((1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)),
                        ((-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7))
                        )

        rook_moves = (
                      ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)),
                      ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)),
                      ((0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)),
                      ((-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0))
                     )

        knight_moves = ((-1, -2), (1, -2), (-2, -1), (2, -1), (-2, 1), (2, 1), (-1, 2), (1, 2))

        king_moves = ((-1, -1), (0, -1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (0, 1))

        for i in range(0, 8):
            if self.board.inside((king_moves[i][0]+array_coord[0], king_moves[i][1]+array_coord[1])):
                if opposite+"KING" in self.board.get_tile((king_moves[i][0]+array_coord[0], king_moves[i][1]+array_coord[1])) == "EMPTY":
                    print("no")
                    return True

        for i in range(0, 8):
            if self.board.inside((knight_moves[i][0]+array_coord[0], knight_moves[i][1]+array_coord[1])):
                if opposite+"KNIGHT" in self.board.get_tile((knight_moves[i][0]+array_coord[0], knight_moves[i][1]+array_coord[1])):
                    print("no")
                    return True
                
        for i in range(0, 4):
            for j in range(0, 7):
                if self.board.inside((bishop_moves[i][j][0]+array_coord[0], bishop_moves[i][j][1]+array_coord[1])):
                    if self.game_turn in self.board.get_tile((bishop_moves[i][j][0]+array_coord[0], bishop_moves[i][j][1]+array_coord[1])): break
                    for p in [opposite+"-QUEEN", opposite+"-BISHOP"]:# checks if it is a bishop or queen
                        if p in self.board.get_tile((bishop_moves[i][j][0]+array_coord[0], bishop_moves[i][j][1]+array_coord[1])):
                            return True
        
        for i in range(0, 4):
            for j in range(0, 7):
                if self.board.inside((rook_moves[i][j][0]+array_coord[0], rook_moves[i][j][1]+array_coord[1])):
                    if self.game_turn in self.board.get_tile((rook_moves[i][j][0]+array_coord[0], rook_moves[i][j][1]+array_coord[1])): break
                    for p in [opposite+"-QUEEN", opposite+"-ROOK"]:
                        if p in self.board.get_tile((rook_moves[i][j][0]+array_coord[0], rook_moves[i][j][1]+array_coord[1])):
                            return True
        
        return False



    def move_piece(self, board, move_input, next_turn, promotion=""):
        start = move_input[0]
        end = move_input[1]
        
        if self.game_turn+"-" in board.get_tile(start):
            if "KING" in board.get_tile(start):
                if end in self.king_move_legal(board, start):
                    if self.game_turn == "W": self.white_king_position = end
                    else: self.black_king_position_king_position = end
                    
                    if "O-O" in self.king_move_legal(board, start):
                        board.switch((4, 0), (6, 0))
                        board.switch((7, 0), (5, 0))
                        
                    elif "O-O-O" in self.king_move_legal(board, start):
                        board.switch((4, 0), (6, 0))
                        board.switch((7, 0), (5, 0))
                    else:    
                        board.switch(start, end)
                    if next_turn: self.next_turn()
                     
                    self.game_history.append(move_input)
                    
            elif "ROOK" in board.get_tile(start):
                if end in self.rook_move_legal(board, start): 
                    board.switch(start, end)
                    if next_turn: self.next_turn()
                    self.game_history.append(move_input)
            
            elif "QUEEN" in board.get_tile(start):
                if end in self.queen_move_legal(board, start): 
                    board.switch(start, end)
                    if next_turn: self.next_turn()
                    self.game_history.append(move_input)
                
            elif "BISHOP" in board.get_tile(start):
                if end in self.bishop_move_legal(board, start):
                    board.switch(start, end)
                    if next_turn: self.next_turn()
                    self.game_history.append(move_input)

            elif "KNIGHT" in board.get_tile(start):
                if end in self.knight_move_legal(board, start): 
                    board.switch(start, end)
                    if next_turn: self.next_turn()
                    self.game_history.append(move_input)

            elif "PAWN" in board.get_tile(start):
                if end in self.pawn_move_legal(board, start): 
                    if start != end:
                        board.switch(start, end)
                        if next_turn: self.next_turn()
                        self.game_history.append(move_input)
                    else:
                        board.set_tile(start, promotion)
                        if next_turn: self.next_turn()
                        self.game_history.append(move_input)
        
        return board


class Bot(Chessboard):
    def __init__(self):
        super().__init__()

        self.piece_values = {
            "ROOK": 5,
            "BISHOP": 3,
            "PAWN": 1,
            "KING": 10**30,
            "QUEEN": 9,
            "KNIGHT": 3
        } 

        self.heatmaps = {
        "PAWN": self.Board([
            [0,  0,  0,  0,  0,  0,  0,  0],
			[50, 50, 50, 50, 50, 50, 50, 50],
			[10, 10, 20, 30, 30, 20, 10, 10],
			[5,  5, 10, 25, 25, 10,  5,  5],
			[0,  0,  0, 20, 20,  0,  0,  0],
			[5, -5,-10,  0,  0,-10, -5,  5],
			[5, 10, 10,-20,-20, 10, 10,  5],
			[0,  0,  0,  0,  0,  0,  0,  0]
        ]),
        
        "KNIGHT": self.Board([
			[-50,-40,-30,-30,-30,-30,-40,-50],
			[-40,-20,  0,  0,  0,  0,-20,-40],
			[-30,  0, 10, 15, 15, 10,  0,-30],
			[-30,  5, 15, 20, 20, 15,  5,-30],
			[-30,  0, 15, 20, 20, 15,  0,-30],
			[-30,  5, 10, 15, 15, 10,  5,-30],
			[-40,-20,  0,  5,  5,  0,-20,-40],
			[-50,-40,-30,-30,-30,-30,-40,-50]
        ]),

        "BISHOP": self.Board([
			[-20,-10,-10,-10,-10,-10,-10,-20],
			[-10,  0,  0,  0,  0,  0,  0,-10],
			[-10,  0,  5, 10, 10,  5,  0,-10],
			[-10,  5,  5, 10, 10,  5,  5,-10],
			[-10,  0, 10, 10, 10, 10,  0,-10],
			[-10, 10, 10, 10, 10, 10, 10,-10],
			[-10,  5,  0,  0,  0,  0,  5,-10],
			[-20,-10,-10,-10,-10,-10,-10,-20]
        ]),

        "ROOK": self.Board([
			[0,  0,  0,  0,  0,  0,  0,  0],
			[5, 10, 10, 10, 10, 10, 10,  5],
			[-5,  0,  0,  0,  0,  0,  0, -5],
			[-5,  0,  0,  0,  0,  0,  0, -5],
			[-5,  0,  0,  0,  0,  0,  0, -5],
			[-5,  0,  0,  0,  0,  0,  0, -5],
			[-5,  0,  0,  0,  0,  0,  0, -5],
			[0,  0,  0,  5,  5,  0,  0,  0]
        ]),

        "QUEEN": self.Board([
			[-20,-10,-10, -5, -5,-10,-10,-20],
			[-10,  0,  0,  0,  0,  0,  0,-10],
			[-10,  0,  5,  5,  5,  5,  0,-10],
			[-5,  0,  5,  5,  5,  5,  0, -5],
			[0,  0,  5,  5,  5,  5,  0, -5],
			[-10,  5,  5,  5,  5,  5,  0,-10],
			[-10,  0,  5,  0,  0,  0,  0,-10],
			[-20,-10,-10, -5, -5,-10,-10,-20]
		]),

        "KING-START": self.Board([
            [-30,-40,-40,-50,-50,-40,-40,-30],
			[-30,-40,-40,-50,-50,-40,-40,-30],
			[-30,-40,-40,-50,-50,-40,-40,-30],
			[-30,-40,-40,-50,-50,-40,-40,-30],
			[-20,-30,-30,-40,-40,-30,-30,-20],
			[-10,-20,-20,-20,-20,-20,-20,-10],
			[20, 20,  0,  0,  0,  0, 20, 20],
			[20, 30, 10,  0,  0, 10, 30, 20]
		]),

        "KING-END": self.Board([
			[-50,-40,-30,-20,-20,-30,-40,-50],
			[-30,-20,-10,  0,  0,-10,-20,-30],
			[-30,-10, 20, 30, 30, 20,-10,-30],
			[-30,-10, 30, 40, 40, 30,-10,-30],
			[-30,-10, 30, 40, 40, 30,-10,-30],
			[-30,-10, 20, 30, 30, 20,-10,-30],
			[-30,-30,  0,  0,  0,  0,-30,-30],
			[-50,-30,-30,-30,-30,-30,-30,-50]
		])
        }

    def mobility(self, board, color):
        mobility_score = 0
        for piece in board.get_pieces(color):
            mobility_score += len(self.get_move(board, piece[1]))

        return mobility_score
    
    
    
    def position(self, board, color):
        position_score = 0
        for piece in board.get_pieces(color):
            if piece[0] == "KING": position_score += 0
            else: position_score += self.heatmaps[piece[0]].get_tile(piece[1])
        
        return position_score
            
        
    
    def material(self, board, color):    
        material_score = 0
        for piece in board.get_pieces("W"):
            material_score += self.piece_values[piece[0]]
                
        for piece in board.get_pieces("B"):
            material_score -= self.piece_values[piece[0]]

        if color == "W": return material_score
        else: return -material_score

    
    def evaluate(self, board, color):
        move_rating = self.mobility(board, color)
        move_rating = self.material(board, color)*13
        move_rating += self.position(board, color)
        return move_rating

    
    
    def bot_move(self, board, color, move=False, depth=3):
        ogboard = self.Board(board.copy())

        
        original = self.evaluate(ogboard, color)
        moves, move_ratings = [], [] 
        promotions = []
        
        for piece in ogboard.get_pieces(color):
            for move in self.get_move(ogboard, piece[1]):
                if piece[1] == move: #all promotion options
                    for promotion in [color+"-"+"QUEEN", color+"-"+"ROOK", color+"-"+"BISHOP", color+"-"+"KNIGHT"]:
                        new_board = self.Board(ogboard.copy())
                        self.move_piece(new_board, (piece[1], move), False, promotion) 
                        moves.append(((piece[1], move), promotion))
                        move_ratings.append(self.evaluate(new_board, color)-original)
                        
                else: #normal
                    new_board = self.Board(ogboard.copy())
                    self.move_piece(new_board, (piece[1], move), False) 
                    moves.append(((piece[1], move), ""))
                    move_ratings.append(self.evaluate(new_board, color)-original)
        
        #self.board = self.Board()
        best_move = moves[move_ratings.index(max(move_ratings))] 
        if move: self.move_piece(self.board, best_move[0], True, best_move[1])
        else: return best_move

        
#-/mobitlity
#-/pieces
#-/heatmaps
#space in enemy territory
#king check surround
#defence
#attack
#check squares

web.page["load"].textContent = "This site has succesfully loaded"

bot = Bot()
start, end = "", ""

def set_tile_color(id, color):
    web.page[id.replace("b", "t")].classes.clear()
    web.page[id.replace("b", "t")].classes.add(color)    


def reset_tile_colors():
    for id in range(1, 65):
        web.page["t"+str(id)].classes.clear() 
        if web.page["t"+str(id-8)].classes == {"light"}:
            set_tile_color("t"+str(id), "dark")
        else: set_tile_color("t"+str(id), "light")
        

def draw_moves(start_tile):    
    start_piece = bot.board.get_tile(((int(start_tile.replace("b", ""))-1)%8, 7-((int(start_tile.replace("b", ""))-1)//8))).replace("W-", "").replace("B-", "")
    start_pos = (((int(start_tile.replace("b", ""))-1)%8), 7-(int(start_tile.replace("b", ""))-1)//8)
    web.page[bot.game_turn+"PP"].classes.clear()
    web.page[bot.game_turn+"PP"].classes.add("hide")
    web.page[bot.game_turn+"PP"].x = "0"
    web.page[bot.game_turn+"PP"].y = "0"

    for i in bot.get_move(bot.board, start_pos):
        if start_pos == i:
            web.page[bot.game_turn+"PP"].classes.clear()
            web.page[bot.game_turn+"PP"].classes.add("show")
            web.page[bot.game_turn+"PP"].classes.add("Div")
            web.page[bot.game_turn+"PP"].x = str(start_pos[0])
            web.page[bot.game_turn+"PP"].y = str(start_pos[1])
        else: 
            set_tile_color("t"+str((7-i[1])*8+(i[0]+1)), "can_move")    
    
    set_tile_color(start_tile, "selected")
    update(bot.board)

@when("mouseenter", "#KNIGHT")
@when("mouseenter", "#QUEEN")
@when("mouseenter", "#BISHOP")
@when("mouseenter", "#ROOK")
def set_image_background(event): 
    web.page["KNIGHT"].classes.clear()
    web.page["BISHOP"].classes.clear()
    web.page["QUEEN"].classes.clear()
    web.page["ROOK"].classes.clear()
    web.page[event.target.id].classes.add("selected")

@when("mouseleave", "#WPP")
@when("mouseleave", "#BPP")
def remove_image_background():
    web.page["KNIGHT"].classes.clear()
    web.page["BISHOP"].classes.clear()
    web.page["QUEEN"].classes.clear()
    web.page["ROOK"].classes.clear()

@when("click", "#KNIGHT")
@when("click", "#QUEEN")
@when("click", "#BISHOP")
@when("click", "#ROOK")
def promote_piece(event):
    x = int(web.page[bot.game_turn+"PP"].x)
    y = int(web.page[bot.game_turn+"PP"].y)
    bot.move_piece(bot.board, ((x, y), (x, y)), True, bot.game_turn+"-"+event.target.id)
    bot.bot_move(bot.board, bot.game_turn, True)
    web.page[bot.game_turn+"PP"].classes.clear()
    web.page[bot.game_turn+"PP"].classes.add("hide")
    web.page[bot.game_turn+"PP"].classes.add("Div")
    reset_tile_colors()
    update(bot.board)



@when("click", ".dark")
@when("click", ".light")
def click(event):
    global start, end
    
    if start == "": 
        if bot.game_turn+"-" in web.page[event.target.id.replace("t", "b")].src:
            start = event.target.id.replace("t", "b")
            draw_moves(start)

    elif end == "": 
        if web.page[event.target.id.replace("b", "t")].classes == {"can_move"}: 
            end = event.target.id.replace("t", "b")
            start_pos = (((int(start.replace("b", ""))-1)%8), 7-(int(start.replace("b", ""))-1)//8)
            end_pos = (((int(end.replace("b", ""))-1)%8), 7-(int(end.replace("b", ""))-1)//8)
            bot.move_piece(bot.board, (start_pos, end_pos), True)
            update(bot.board)
            reset_tile_colors()

            bot.bot_move(bot.board, bot.game_turn, True)
            update(bot.board)
            
        elif bot.game_turn+"-" in web.page[event.target.id.replace("t", "b")].src:
            start = event.target.id.replace("t", "b")
            reset_tile_colors()
            draw_moves(start)    
        else:
            start = ""
            reset_tile_colors()
            
    else:
        if bot.game_turn+"-" in web.page[event.target.id.replace("t", "b")].src:
            start = event.target.id.replace("t", "b")
            draw_moves(start)
            end = ""
            
def update(update_board):
    piece_image = {
    "W-ROOK": "./Images/W-ROOK.webp",
    "W-BISHOP": "./Images/W-BISHOP.webp",
    "W-PAWN": "./Images/W-PAWN.webp",
    "W-KING": "./Images/W-KING.webp",
    "W-QUEEN": "./Images/W-QUEEN.webp",
    "W-KNIGHT": "./Images/W-KNIGHT.webp",
    "EMPTY": "./Images/EMPTY.png",
    "B-ROOK": "./Images/B-ROOK.webp",
    "B-BISHOP": "./Images/B-BISHOP.webp",
    "B-PAWN": "./Images/B-PAWN.webp",
    "B-KING": "./Images/B-KING.webp",
    "B-QUEEN": "./Images/B-QUEEN.webp",
    "B-KNIGHT": "./Images/B-KNIGHT.webp"
    }

    for i in range(0, 8):
        for j in range(0, 8):
            web.page["b"+str(i*8+j+1)].src = piece_image[update_board.content[i][j]]

update(bot.board)