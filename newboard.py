"""
unicode symbols for chess pieces, 
- yes that's a thing!
"""

import chess
from tableeval import *

B_TEXT = "\033[30m"
W_TEXT = "\033[30m"
RESET = "\033[0;0m"
W_BG = "\033[107;0;107m"

WK = W_TEXT + u'\u2654' #♚
WQ = W_TEXT + u'\u2655' #♛
WR = W_TEXT + u'\u2656' #♜
WB = W_TEXT + u'\u2657' #♝
WN = W_TEXT + u'\u2658' #♞
WP = W_TEXT + u'\u2659' #♟
BK = B_TEXT + u'\u265A' #♚
BQ = B_TEXT + u'\u265B' #♛
BR = B_TEXT + u'\u265C' #♜
BB = B_TEXT + u'\u265D' #♝
BN = B_TEXT + u'\u265E' #♞
BP = B_TEXT + u'\u265F' #♟
#Dict of letters to pieces
l2p = {'K':WK,'Q':WQ,'R':WR,'B':WB,'N':WN,'P':WP,'k':BK,'q':BQ,'r':BR,'b':BB,'n':BN,'p':BP," ":" "}

class Board:

    def __init__(self):
        self.board = []
        self.chessboard  = chess.Board()
        self.set_start_board_position()
        self.backplayer = ""
        self.whiteplayer = ""
        self.originboard=[]
        self.lastorigin = ""
        self.lastdestin = ""
        self.originboard = ["r","n","b","q","k","b","n","r","R","N","B","Q","K","B","N","R","p","p","p","p","p","p","p","p","P","P","P","P","P","P","P","P"]
    def set_start_board_position(self):
        self.board.extend(["r","n","b","q","k","b","n","r"])
        self.board.extend(list("p"*8))
        self.board.extend(list(" "*32))
        self.board.extend(list("P"*8))
        self.board.extend(["R","N","B","Q","K","B","N","R"])



    def set_players(self, white, black):
        self.whiteplayer = white
        self.backplayer = black


    def clear_board(self):
        self.board = list(" "*64)

    def highlight(self,tile):
        index = self.coord_to_index(tile)
        h = "\033[46;30;46m"
        k = "\033[0;0m"
        self.board[index] = h + self.board[index] + k

    def extract_material(self):
        captured_pieces = ["r","n","b","q","k","b","n","r","R","N","B","Q","K","B","N","R","p","p","p","p","p","p","p","p","P","P","P","P","P","P","P","P"]
        current_board = [x for x in self.board if x != " "]
        advantage = self.eval_material_advantage(current_board)
        for piece in current_board:
            try:
                captured_pieces.remove(piece)
            except Exception as e:
                print(e)
                print(piece)
                print(captured_pieces)
                print(current_board)

        white_captures = [x for x in captured_pieces if x.islower()]
        black_captures = [x for x in captured_pieces if x.isupper()]
        return [white_captures,black_captures,advantage]

    def eval_material_advantage(self, listMaterial):
        pieces_worth = {"Q":9, "R":4, "B":3, "N":3, "P":1, "K":0}
        white_cumul_worth = 0
        black_cumul_worth = 0
        for piece in listMaterial:
            worth = pieces_worth[piece.upper()]
            if piece.isupper():
                white_cumul_worth += worth
            else:
                black_cumul_worth += worth

        difference = abs(white_cumul_worth-black_cumul_worth)
        if white_cumul_worth > black_cumul_worth:
            return [difference,0]
        elif black_cumul_worth > white_cumul_worth:
            return [0, difference]
        else: 
            return [0,0]
    def alternate_tile(self, row, offset,piece):
        w = "\033[107;0;107m"
        k = "\033[42;0;42m"

        n = "\033[0;0m"
        head = ""
        tile = l2p[piece] 
        tail = " " + n
        if  (row + offset ) %2 == 0:
            head = w
        else: 
            head = k
        return head + tile + tail
        
    def pretty_print_captures(self, captures,advantage):
        toreturn = ""
        if len(captures) != 0:
            if captures[0].isupper():
                advantage= advantage[1]
            else:
                advantage = advantage[0]

            for piece in captures:
                toreturn += l2p[piece] + " "

            if advantage != 0:
                toreturn += f" +{advantage}"
        
        return toreturn
            
    

    def print_checker_pattern(self, row, l,perspective):
        if perspective == 0:
            row_nb = 8 - int(row)
        else:
            row_nb = int(row) +1
        to_print = f"{W_BG}{B_TEXT}{row_nb} {RESET}"
        for i in range(len(l)):
            to_print += self.alternate_tile(8-int(row), i, l[i])
        to_print += f"{W_BG}{B_TEXT} {row_nb}{RESET}"

        material = self.extract_material()
        white_captures = material[0]
        black_captures = material[1]
        
        advantage = material[2]
    
        white_cap_str = f"  {W_BG}{self.pretty_print_captures(white_captures,advantage)}{RESET}"
        black_cap_str = f"  {W_BG}{self.pretty_print_captures(black_captures,advantage)}{RESET}"
        if (int(row) == 0):
            if perspective == 0:
                to_print+= black_cap_str
            else:
                to_print+= white_cap_str

        if (int(row) == 7):
            if perspective == 0:
                to_print+= white_cap_str
            else:
                to_print+= black_cap_str
                 

        if (int(row) == 4):
            to_print += f"   EVAL: {self.evaluate_board()}"

        
        print(to_print)


    def make_move_san(self, move):
            self.chessboard.push_san(move)
            self.fen = self.chessboard.fen()
            self.update_board(self.fen)




    def update_board(self, fen):
        self.board = list(" "* 64)
        indexboard = 0
        indexstring = 0
        fenonly = fen.split(" ")[0]
        while(indexboard < 64 and indexstring < len(fenonly)):
            fenonly = fenonly.replace("/", "")
            if fenonly[indexstring].isdigit():
                indexboard += int(fenonly[indexstring])
            else:
                self.board[indexboard] = fenonly[indexstring]
                indexboard +=1
            indexstring += 1



    
    def coord_to_index(self, coord):
        d = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
        index = d[coord[0]] + (8 - int(coord[1])) *8
        return index


    def generate_fen(self):
        fen = ""
        nb_empty = 0
        for i in range(len(self.board)):
            if i > 0 and i % 8 == 0:
                if nb_empty != 0:
                    fen += str(nb_empty)
                    nb_empty = 0
                fen += "/"
            if self.board[i] != " ":
                if nb_empty != 0:
                    fen+=str(nb_empty)
                    nb_empty = 0
                fen += self.board[i]
            else:
                nb_empty +=1
        return fen

    def print_board(self,perspective):
        to_print = []
        w = "\033[107;0;107m"
        k = "\033[42;0;42m"

        board = self.board
        if perspective == 0:
            columntop = f"{w}{B_TEXT}  A B C D E F G H   {RESET}  Noir : "+self.backplayer
            columnbottom = f"{w}{B_TEXT}  A B C D E F G H   {RESET}  Blanc: "+self.whiteplayer

        else:
            board.reverse() 
            columntop = f"{w}{B_TEXT}  H G F E D C B A   {RESET}  Blanc: "+self.whiteplayer
            columnbottom = f"{w}{B_TEXT}  H G F E D C B A   {RESET} Noir : "+self.backplayer


        i =0
        print()
        print(columntop)
        while(i < 64):
            self.print_checker_pattern(i/8, board[i:i+8],perspective)
            i+=8
        print(columnbottom)

        print()
    



    def evaluate_board(self):
        board = self.chessboard
        if board.is_checkmate():
            if board.turn:
                return -9999
            else:
                return 9999
        if board.is_stalemate():
            return 0
        if board.is_insufficient_material():
            return 0
        
        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))
        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))
        
        material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)
        
        pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq= pawnsq + sum([-pawntable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq= sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq= bishopsq + sum([-bishopstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
        rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
        queensq = queensq + sum([-queenstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
        kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KING, chess.BLACK)])
        
        eval = material + pawnsq + knightsq + bishopsq+ rooksq+ queensq + kingsq
        if board.turn:
            return eval
        else:
            return -eval


