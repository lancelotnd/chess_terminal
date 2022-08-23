from datetime import datetime
from json import loads, dumps
from pprint import pprint
import socket
from threading import Thread
from Game import Game
import uuid
games = {}
game_queue = []

class ThreadedServer(Thread):
    def __init__(self, host, port, timeout=60, callback=None, debug=False):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.callback = callback
        self.debug = debug
        Thread.__init__(self)

    # run by the Thread object
    def run(self):
        if self.debug:
            print(datetime.now())
            print('SERVER Starting...', '\n')

        self.listen()

    def listen(self):
        # create an instance of socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to its host and port
        self.sock.bind((self.host, self.port))
        if self.debug:
            print(datetime.now())
            print('SERVER Socket Bound', self.host, self.port, '\n')

        # start listening for a client
        self.sock.listen(5)
        if self.debug:
            print(datetime.now())
            print('SERVER Listening...', '\n')
        while True:
            # get the client object and address
            client, address = self.sock.accept()

            # set a timeout
            client.settimeout(self.timeout)

            if self.debug:
                print(datetime.now())
                print('CLIENT Connected:', client, '\n')

            # start a thread to listen to the client
            Thread(
                target=self.listenToClient,
                args=(client, address, self.callback)
            ).start()

            # send the client a connection message
            # res = {
            #     'cmd': 'connected',
            # }
            # response = dumps(res)
            # client.send(response.encode('utf-8'))

    def listenToClient(self, client, address, callback):
        # set a buffer size ( could be 2048 or 4096 / power of 2 )
        size = 1024
        while True:
            try:
                # try to receive data from the client
                data = client.recv(size).decode('utf-8')
                if data:
                    data = loads(data.rstrip('\0'))
                    if self.debug:
                        print(datetime.now())
                        print('CLIENT Data Received', client)
                        cmd = data["cmd"]
                        content = data["data"]
                        if cmd == "JOIN":
                            if len(game_queue) == 0:
                                gameuuid = str(uuid.uuid1())
                                game_queue.append(gameuuid)
                                playerid1 = str(uuid.uuid1())
                                playerName1 = content[0]
                                games[str(gameuuid)] = Game(gameuuid, playerid1,playerName1 ) 
                                response = {"cmd":"SESSIONINFO", "data": [gameuuid, playerid1]}
                            else:
                                gameuuid = game_queue.pop(0)
                                playerid2 = str(uuid.uuid1())
                                playerName2 = content[0]
                                response = {"cmd":"SESSIONINFO", "data": [gameuuid, playerid2]}
                                games[gameuuid].start_game(playerid2, playerName2)

                        if cmd == "FEN":
                            if content[0] in game_queue:
                                 response = {"cmd":"WAITING", "data": []}
                            else:
                                 gameuuid = content[0]
                                 playerid = content[1]
                                 response = {"cmd": "FEN", "data": [games[gameuuid].get_fen(), games[gameuuid].players[playerid],games[gameuuid].board.chessboard.fen(), games[gameuuid].get_move_header()]}
                        if cmd == "MAKEMOVE":
                            gameid = content[0]
                            playerid = content[1]
                            move = content[2]
                            games[gameid].play_move(playerid, move)
                            reponse = {"cmd":"OK", "data": []}
                        print(data["cmd"])
                        print(data["data"])
                        pprint(data, width=1)
                        print('\n')

                    if callback is not None:
                        callback(client, address, response)

                else:
                    raise error('Client disconnected')

            except Exception as e:
                print(e)
                if self.debug:
                    print(datetime.now())
                    print('CLIENT Disconnected:', client, '\n')
                client.close()
                return False


def some_callback(client, address, data):
    print('data sent', data)
    # send a response back to the client

    res = {
        'cmd': data['cmd'],
        'data': data['data']
    }
    response = dumps(res)
    client.send(response.encode('utf-8'))


if __name__ == "__main__":
    ThreadedServer('127.0.0.1', 8008, timeout=86400, callback=some_callback, debug=True).start()