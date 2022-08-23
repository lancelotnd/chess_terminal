from newboard import Board
import chess
board = Board()
board.clear_board()
board.update_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
board.print_board(0)
board.make_move(0, "Rh2")

while(True):
   
    try:
        txt = input("Black to move: ")
        if txt == "exit":
            break
        board.make_move_san(txt)
        board.print_board(0)
    except Exception as e:
        print(e)
        print( "Ce move n'est pas légal veuillez recommencer.")

    

    
