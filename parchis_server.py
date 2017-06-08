import socket
import time
import pygame
import sys
import threading
import random

class TimeServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_time = time.time()
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_sock.bind((host, port))
        except socket.error as e:
            print(str(e))
            sys.exit()
        self.server_sock.listen(5)
        self.maximun_players = 1
        self.players_pieces_list = []
        self.connection_list = []
        self.players_list = {}
        self.players_color_list = {}
        self.players_first_turn = {}
        self.active_game = True
        self.player_active_turn = ""
        self.shift_list = []
        
    def init_server(self):
        print "SERVER: Wating players {0} {1}".format(self.host, self.port)
        try:
            while True:
                self.accept_connection()
        except socket.error as e:
            print "Error ", # coding=utf-8
        finally:
            self.server_sock.close()
            
    def accept_connection(self):
        try:
            new_sock, addr = self.server_sock.accept()
        except:
            self.server_sock.close()
            
        if len(self.connection_list) < self.maximun_players:
            print "SERVER: Connection received {0}".format(addr)
            self.connection_list.append(new_sock) 
            self.synchronize()
        else:
            print "SERVER: No more connections allowed"
            new_sock.send("")

    def synchronize(self):
        accumulated_time = 0
        local_time = time.time()
        
        for sock in self.connection_list:
            if sock != self.server_sock:
                init_time = time.time()
                sock.send("get_time " + str(time.time()))
                client_gap = float(sock.recv(4094))
                end_time = time.time()
                client_gap += ((end_time - init_time) / 2)
                accumulated_time += local_time + client_gap
                
        print "SERVER: New time {0}".format(accumulated_time)
        avg = (accumulated_time + local_time) / (len(self.connection_list))
        for sock in self.connection_list:
            if sock != self.server_sock:
                sock.send("post_time " + str(avg))
                
        if len(self.connection_list) == self.maximun_players:
            self.boot_match()

    def boot_match(self):
        
        threads = []
        #NOMBRE DE USUARIO
        for sock in self.connection_list:
            if sock != self.server_sock:
                sock.send("get_username ")
                player_username = sock.recv(1024)
                while player_username in self.players_list:
                    sock.send("repeated_username ")
                    player_username = sock.recv(1024)
                self.players_list.update({player_username:sock})
                
        print "SERVER: Players list: "
        for player in self.players_list:
            print "\t* ", player
            
        #COLOR DE USUARIO
        for username, player_sock in self.players_list.iteritems():
            if player_sock != self.server_sock:
                player_sock.send("get_color ")
                player_color = player_sock.recv(1024)
                while player_color in self.players_color_list:
                    player_sock.send("repeated_color ")
                    player_color = player_sock.recv(1024)
                self.players_color_list.update({username:player_color})
                
        print "SERVER: Players color list: "
        for username, player_color in self.players_color_list.iteritems():
            print "\t* ", player_color
        
        #PRIMERA TIRADA DE DADOS PARA DETERMINAR EL PRIMER TURNO
        for username, player_sock in self.players_list.iteritems():
            if player_sock != self.server_sock:
                player_sock.send("throw_dice_ft ")
                dice_ft = int(player_sock.recv(1024))
                self.players_first_turn.update({username:dice_ft})
                
        
        self.player_active_turn = max(self.players_first_turn.keys())
        
        print "SERVER: Firts turn"
        print "\t* ", self.player_active_turn
            
        #INICIALIZAR CADA JUGADOR
        for username, player_sock in self.players_list.iteritems():
            ack = ""
            if player_sock != self.server_sock:
                while not(ack == "ack"):
                    print "SERVER: player ", username, " has not yet stated"
                    player_sock.send("init ")
                    ack = player_sock.recv(1024)
                print "SERVER: player ", username, " has started"
            player = threading.Thread(target = self.game, args = (username, ))
            threads.append(player)

        for thread in threads:
            thread.start()

    def game(self, username):
        sock = self.players_list[username]
        while self.active_game:
            if username == self.player_active_turn:
                time.sleep(2)
                move = ""
                while not(move != "ack" and move != ''):
                    sock.send("your_turn ")
                    move = sock.recv(1024)
                move = jugada.split(" ")
                
                print "SERVER: Player ", username, " want to make the move: ", move
                
                if move[0] == "move":
                    print "FINE"

if __name__ == '__main__':
    server = TimeServer(str(sys.argv[1]), int(sys.argv[2]))
    server.init_server()
		 

        
    
