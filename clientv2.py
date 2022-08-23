import json
import socket
import time
from newboard import Board


def send(cmd, data,sock):
    data = {
	    'cmd': cmd,
	    'data': data
    }
    msg = json.dumps(data)
    sock.sendall(msg.encode('utf-8'))
    

FORMAT = "utf-8"
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


username = input("Entrez votre username:")

# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 8008)
sock.connect(server_address)

# Create the data and load it into json
data = {
	'cmd': 'JOIN',
	'data': [username],
}
msg = json.dumps(data)

# Send the message
sock.sendall(msg.encode('utf-8'))

# Receive the message back
res = sock.recv(1024).decode('utf-8')
response = json.loads(res)

gameid = response["data"][0]
playerId = response["data"][1]

# Create the data and load it into json
data = {
	'cmd': 'FEN',
	'data': [gameid, playerId]
}
msg = json.dumps(data)
sock.sendall(msg.encode('utf-8'))

# Receive the message back
res = sock.recv(1024).decode('utf-8')
response = json.loads(res)
while(response["cmd"] == "WAITING"):
    time.sleep(1)
    print("nous attendons un autre joueur")
    sock.sendall(msg.encode('utf-8'))
    res = sock.recv(1024).decode('utf-8')
    response = json.loads(res)


fen = response["data"][0]
officialfen = response["data"][2]
move_header = response["data"][3]

color = 0
color =  response["data"][1]
whiteusername = fen.split(":")[1]
blackusername = fen.split(":")[2]

colorname = ["white", "black"]


print(f"Vous jouez les  {colorname[color]}")

board = Board()
board.update_board(fen)
board.chessboard.set_fen(officialfen)
board.set_players(whiteusername, blackusername)
print(move_header)
board.print_board(color)


playing = True
while(playing):
    tomove = int(fen.split(" ")[1])
    if(color == tomove):
        board.update_board(fen)
        board.chessboard.set_fen(officialfen)
        print(move_header)
        board.print_board(color)
        while(True):
            try:
                move = input(f"{colorname[color]} to move: ")
                board.make_move_san(move)
                send('MAKEMOVE',[gameid,playerId,move],sock)
                break
            except Exception as e:
                print(e)
                print("Ce move n'est pas légal, vous devez utiliser la notion algébrique abrégée ou étendue.\nVeuillez recommencer.")
           
        response = sock.recv(1024).decode(FORMAT)
        data = {
	        'cmd': 'FEN',
	        'data': [gameid,playerId]
        }
        sock.sendall(msg.encode('utf-8'))
        res = sock.recv(1024).decode('utf-8')
        response = json.loads(res)

        fen = response["data"][0]
        color = response["data"][1]
        official_fen = response["data"][2]
        move_header = response["data"][3]
        board.update_board(fen)
        board.chessboard.set_fen(official_fen)
        print(move_header)
        board.print_board(color)

    else:
        data = {
	        'cmd': 'FEN',
	        'data': [gameid]
        }
        sock.sendall(msg.encode('utf-8'))
        res = sock.recv(1024).decode('utf-8')
        response = json.loads(res)
        fen = response["data"][0]
        officialfen = response["data"][2]
        move_header = response["data"][3]
        board.chessboard.set_fen(officialfen)
        time.sleep(1)

