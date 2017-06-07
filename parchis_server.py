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
        self.pieces_list = []
        self.connection_list = []
        self.players_list = {}
        self.players_color_list = {}
        self.players_first_turn = {}
        
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
            
        for username, player_sock in self.players_list.iteritems():
            if player_sock != self.server_sock:
                player_sock.send("throw_dice_ft ")
                dice_ft = player_sock.recv(1024)
                self.players_first_turn.update({username:dice_ft})
                
        print "SERVER: Players color list: "
        for username, player_dice_ft in self.players_first_turn.iteritems():
            print "\t* ", player_dice_ft

        
        #~ ack = ""
        #~ threads = []
        #~ for player_sock in self.connection_list:
            #~ if player_sock != self.server_sock:
                #~ gamer = threading.Thread(target = self., args = ())
                #~ threads.append(jugador)
                #~ print "SUCCES GAME"

        #~ for thread in threads:
            #~ thread.start()

    def game(self):
        pass

if __name__ == '__main__':
    server = TimeServer(str(sys.argv[1]), int(sys.argv[2]))
    server.init_server()
		 

        
    
