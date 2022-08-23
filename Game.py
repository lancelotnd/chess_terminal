from newboard import Board
import random
class Game:
    def __init__(self, uuid, playerID1, playerName1):
        self.tomove = 0
        self.player_id1 = playerID1
        self.player_id2 = ""
        self.players= {}
        self.order = ""
        self.board = Board()
        self.uuid = uuid
        self.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        self.player1name = playerName1
        self.player2name = ""
        self.whiteplayerid = ""
        self.movenumber = 0
        self.blackplayerid = ""
        self.ply = 0
        self.lastwhitemove = ""
        self.lastblackmove = ""


    def get_move_header(self):
        if self.tomove == 0:
            self.movenumber = self.board.chessboard.fullmove_number
            toreturn = f"{self.movenumber-1}. {self.lastwhitemove} {self.lastblackmove}"
        else:
            toreturn = f"{self.movenumber}. {self.lastwhitemove} ..."
        
        return toreturn


    def get_fen(self):
        return self.fen + " " + str(self.tomove) + " " + self.order

    def start_game(self, playerID2, playerName2):
        self.player_id2 = playerID2
        self.player2name = playerName2

        if random.randrange(2) == 0:
            self.players[self.player_id1] = 0
            self.order =  f":{self.player1name}:{self.player2name}:"
            self.players[self.player_id2] = 1
        else:
            self.players[self.player_id2] = 0
            self.order =  f":{self.player2name}:{self.player1name}:"
            self.players[self.player_id1] = 1


    def play_move(self, idplayer, move):
        if self.tomove == self.players[idplayer]:
                if self.tomove == 0:
                    self.lastwhitemove = move
                else:
                    self.lastblackmove = move

                self.board.make_move_san(move)
                self.fen = self.board.generate_fen()
                self.ply += 1
                self.tomove = self.ply % 2
        
        