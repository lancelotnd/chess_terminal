"""
unicode symbols for chess pieces, 
- yes that's a thing!
"""

import chess

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
        self.set_start_board_position()
        self.backplayer = ""
        self.whiteplayer = ""
        self.lastorigin = ""
        self.lastdestin = ""
        
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
              

    def print_checker_pattern(self, row, l,perspective):
        if perspective == 0:
            row_nb = 8 - int(row)
        else:
            row_nb = int(row) +1
        to_print = f"{W_BG}{B_TEXT}{row_nb} {RESET}"
        for i in range(len(l)):
            to_print += self.alternate_tile(8-int(row), i, l[i])
        to_print += f"{W_BG}{B_TEXT} {row_nb}{RESET}"

        
        print(to_print)


    def make_move_san(self, move):
        if len(move) == 2:
            self.pawn_move(color,move)
        if len(move) == 3:
            if(move.lower()[0] == 'r'):
                self.rook_move(color, move[1:])
            if(move.lower()[0]== 'b'):
                self.bishop_move(color, move[1:])
            if(move.lower()[0]== 'q'):
                self.queen_move(color, move[1:])
            if(move.lower()[0]== 'n'):
                    self.knight_move(color, move[1:])

    

    def make_move(self, color, move):
        if len(move) == 2:
            self.pawn_move(color,move)
        if len(move) == 3:
            if(move.lower()[0] == 'r'):
                self.rook_move(color, move[1:])
            if(move.lower()[0]== 'b'):
                self.bishop_move(color, move[1:])
            if(move.lower()[0]== 'q'):
                self.queen_move(color, move[1:])
            if(move.lower()[0]== 'n'):
                    self.knight_move(color, move[1:])


    def bishop_move(self,color,move):
        if color == 0:
                piece = "B"
        else: 
            piece = "b"
        originindex = -1
        index = self.coord_to_index(move)
        indexes = self.get_diag_indexes(move)
        for i in range(len(indexes)):
            if self.board[indexes[i]] == piece:
                originindex = indexes[i]
                break
        if self.move_is_legal(originindex, index):
            self.move(originindex, index)


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


    def rook_move(self,color,move):
        if color == 0:
            piece = "R"
        else: 
            piece = "r"
        originindex = -1
        index = self.coord_to_index(move)
        indexes = self.get_hv_indexes(move)
        for i in range(len(indexes)):
            if self.board[indexes[i]] == piece:
                originindex = indexes[i]
                break
        if self.move_is_legal(originindex, index):
            self.move(originindex, index)
            

    def move(self, origin_index, destination_index):
        if origin_index != -1:
            self.lastorigin = origin_index
            self.lastdestin = destination_index
            piece = self.board[origin_index]
            self.board[origin_index] = " "
            self.board[destination_index] = piece


    def move_is_legal(self, origin_index, dest_index):
        move_is_possible = origin_index != -1
        suicidal = self.suicidal(origin_index, dest_index)
        jumping = self.check_if_jumping(self.board[origin_index], origin_index, dest_index)
        return move_is_possible and (not suicidal) and (not jumping)
    """
    Check if this move is suicidal, that is, if a player
    would be capturing its own pieces. 
    """
    def suicidal(self, origin_index, dest_index):
        is_suicidal = False
        destination_occupied = self.board[dest_index] !=  " "
        if destination_occupied:
            is_suicidal = self.board[origin_index].isupper() == self.board[dest_index].isupper()
        return is_suicidal

    def tile_is_occupied(self, index):
        return self.board[index] != " "

    def queen_move(self,color,move):
        if color ==0:
            piece = "Q"
        else:
            piece = "q"
        originindex = -1
        dest_index = self.coord_to_index(move)
        indexes = self.get_hv_indexes(move)
        indexes.extend(self.get_diag_indexes(move))
        for i in range(len(indexes)):
            if self.board[indexes[i]] == piece:
                originindex = indexes[i]
                break
        if self.move_is_legal(origin_index, dest_index):
            self.move(originindex, dest_index)

    """
    Will test if a piece can move to a given location jumping
    over other pieces.

    it will iterate through all the tiles where this piece should 
    traverse to arrive at its destination index and if a piece is 
    in the middle of it this piece will be considered jumping.

    Since the knight can jump, it will not be taken into account
    """

    def check_if_jumping(self, piece, origin_index, dest_index):
        is_jumping = False
        increment = 0
        direction = -1
        if origin_index < dest_index:
            direction = 1
        genericpiece = piece.lower()
        
        #QUEEN REDUCTION  (the move of the queen can be reduced to that of a rook or bishop)
        if genericpiece == "q":
            move_is_vertical = origin_index % 8  == dest_index % 8
            move_is_horizontal = origin_index - (origin_index % 8) == dest_index - (dest_index %8)
            if move_is_vertical or move_is_horizontal:
                genericpiece = "r" #Reduce the queen to a rook. 
            else: 
                genericpiece = "b" #Reduce the queen to a bishop
        # ROOK INCREMENT
        if genericpiece == "r":
            if abs(origin_index - dest_index) > 7:
                increment = 8 * direction
            else: 
                increment = 1 * direction
        # BISHOP INCREMENT
        if genericpiece == "b":
            if origin_index % 8 < dest_index % 8:
                increment = 8 * direction
            else:
                increment = 7 * direction
        # PAWN INCREMENT 
        if genericpiece == "p": 
                increment = 8 * direction

        current_index = origin_index + increment
        while(current_index != dest_index):
            is_jumping = self.board[current_index] != " "
            if is_jumping:
                break
            current_index += increment

        return is_jumping

    def get_origin_index_of_piece(self, piece, indexes):
        originindex = -1
        for i in range(len(indexes)):
            if self.board[indexes[i]] == piece:
                originindex = indexes[i]
                break
        return originindex
        

    def knight_move(self,color,move):
        if color ==0:
            piece = "N"
        else:
            piece = "n"
        dest_index = self.coord_to_index(move)
        indexes = self.get_knight_possible_indexes(move)
        origin_index = self.get_origin_index_of_piece(piece, indexes)
        suicidal = self.suicidal(origin_index, dest_index)
        if not suicidal:
            self.move(origin_index, dest_index)
        



    def return_knight_move(self, coord, letter_offset, number_offset):
        allowed_letters= ['a','b','c','d','e','f','g','h']
        letter = chr(ord(coord[0]))
        number = int(coord[1])
        let_pos = chr(ord(letter)+letter_offset)
        num_pos = number + number_offset
        allowed_letter =  let_pos in allowed_letters
        allowed_number = num_pos >= 1 and num_pos <= 8
        if allowed_letter and allowed_number:
            new_coord = str(let_pos) + str(num_pos)
            to_return = self.coord_to_index(new_coord)
        else:
            to_return = -1
        return to_return


    def get_knight_possible_indexes(self,coord):
        indexes = []        
        indexes.append(self.return_knight_move(coord, 1, 2))
        indexes.append(self.return_knight_move(coord, 2, 1))
        indexes.append(self.return_knight_move(coord, 2, -1))
        indexes.append(self.return_knight_move(coord, 1, -2))
        indexes.append(self.return_knight_move(coord, -1, -2))
        indexes.append(self.return_knight_move(coord, -2, -1))
        indexes.append(self.return_knight_move(coord, -2, 1))
        indexes.append(self.return_knight_move(coord, -1, 2))

        return [index for index in indexes if index != -1]

    def get_last_or_dest(self):
        return [self.lastorigin, self.lastdestin]

    def pawn_move(self,color, move):
        index = self.coord_to_index(move)
        if color == 0:
            if self.board[index+8] == "P":
                self.board[index+8] = " "
                self.board[index] = "P"
            else:
                self.board[index+16] = " "
                self.board[index] = "P"
        else:
            if self.board[index-8] == "p":
                self.board[index-8] = " "
                self.board[index] = "p"
            else:
                self.board[index-16] = " "
                self.board[index] = "p"

    def place_piece(self,piece, coord):
        index = self.coord_to_index(coord)
        self.board[index] = piece
    

    
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
        print(self.generate_fen())
    
    def get_diag_indexes(self, coord):
        indexes = []
        index = self.coord_to_index(coord)
        south_east = index
        south_west = index
        north_east = index
        north_west = index
        indexes.append(index)

        if index % 7 != 0:
            while south_east < 63:
                south_east += 9
                if south_east < 63:
                    indexes.append(south_east)
            while north_east >= 0:
                north_east -= 7
                if north_east >= 0:
                    indexes.append(north_east)

        if index % 8 != 0:
            while south_west < 63:
                south_west += 7
                if(south_west < 63):
                    indexes.append(south_west)


            while north_west >= 0:
                north_west -= 9
                if north_west >= 0:
                    indexes.append(north_west)


        return indexes

    def get_hv_indexes(self, coord):
        list_indexes = []
        
        for i in range(8):
            list_indexes.append(self.coord_to_index(coord[0]+str(i+1)))
            nc = self.coord_to_index(str(chr(ord("a")+i)+coord[1]))
            list_indexes.append(nc)
        return list_indexes


  
