import socket
import sys
import time
import pygame
import threading
import random

class Player:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_switch = True
        self.username = ""
        self.data_received_server = ""

    def connect(self, host, port):
        print "CONNECTING TO {0} {1}".format(host, port)
        try:
            self.sock.connect((host, port))
        except socket.error as e:
            print(str(e))

        while self.game_switch:
            self.data_received_server  = self.sock.recv(1000).split(' ')
            print "DATA RECEIVED: \n------\n", self.data_received_server , "\n------\n"
            try:
                if self.data_received_server[0] == "kill_game":
                    self.game_switch = False
                    break
            except:
                print "AN ERROR HAS OCURRED"
        self.sock.close()
    
    def Throw_dice(screen, cordx, cordy):

        diceimg1 = pygame.image.load("img/dado1.png").convert_alpha()
        diceimg2 = pygame.image.load("img/dado2.png").convert_alpha()
        diceimg3 = pygame.image.load("img/dado3.png").convert_alpha()
        diceimg4 = pygame.image.load("img/dado4.png").convert_alpha()
        diceimg5 = pygame.image.load("img/dado5.png").convert_alpha()
        diceimg6 = pygame.image.load("img/dado6.png").convert_alpha()

        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)
    
        for i in range (2):
            screen.blit(diceimg1,(cordx, cordy))
            screen.blit(diceimg5, (cordx+70, cordy))
            time.sleep(0.2)
            pygame.display.flip()
            screen.blit(diceimg2,(cordx, cordy))
            screen.blit(diceimg4, (cordx+70, cordy))
            time.sleep(0.2)
            pygame.display.flip()
            screen.blit(diceimg3,(cordx, cordy))
            screen.blit(diceimg1, (cordx+70, cordy))
            time.sleep(0.2)
            pygame.display.flip()
            screen.blit(diceimg4,(cordx, cordy))
            screen.blit(diceimg2, (cordx+70, cordy))
            time.sleep(0.2)
            pygame.display.flip()
            screen.blit(diceimg5,(cordx, cordy))
            screen.blit(diceimg6, (cordx+70, cordy))
            time.sleep(0.2)
            pygame.display.flip()
            screen.blit(diceimg6,(cordx, cordy))
            screen.blit(diceimg3, (cordx+70, cordy))
            time.sleep(0.2)
            pygame.display.flip()

        if (dice1==1):
            screen.blit(diceimg1, (cordx, cordy))
        if (dice1==2):
            screen.blit(diceimg2, (cordx, cordy))
        if (dice1==3):
            screen.blit(diceimg3, (cordx, cordy))
        if (dice1==4):
            screen.blit(diceimg4, (cordx, cordy))
        if (dice1==5):
            screen.blit(diceimg5, (cordx, cordy))
        if (dice1==6):
            screen.blit(diceimg6, (cordx, cordy))

        if (dice2==1):
            screen.blit(diceimg1, (cordx+70, cordy))
        if (dice2==2):
            screen.blit(diceimg2, (cordx+70, cordy))
        if (dice2==3):
            screen.blit(diceimg3, (cordx+70, cordy))
        if (dice2==4):
            screen.blit(diceimg4, (cordx+70, cordy))
        if (dice2==5):
            screen.blit(diceimg5, (cordx+70, cordy))
        if (dice2==6):
            screen.blit(diceimg6, (cordx+70, cordy))
            
        pygame.display.flip()

        dice_value[0]=dice1
        dice_value[1]=dice2
        
        return fichas_dados

def load_color_images(screen):
    red = pygame.image.load("img/rojo.png").convert()
    green = pygame.image.load("img/verde.png").convert()
    yellow = pygame.image.load("img/amarillo.png").convert()
    blue = pygame.image.load("img/azul.png").convert()
    screen.blit(red,(90,70))
    screen.blit(green,(140,70))
    screen.blit(yellow,(190,70))
    screen.blit(blue,(240,70))
    pygame.display.flip()

def move_color_pointer(screen, pointer, direction = ""):
    pointer_image = pygame.image.load("img/puntero.png").convert()
    if direction == 'right':
        pointer += 1
        if pointer > 3:
            pointer = 0
    elif direction == 'left':
        pointer -= 1
        if pointer < 0:
            pointer = 3
    position = (90+pointer*50, 48)
    screen.blit(pointer_image, position)
    pygame.display.flip()
    return pointer

def clean_color_screen(screen):
    screen.fill((0,0,0))
    load_color_images(screen)

def select_color():
    screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Select Color")
    color_not_selected = True
    color_list =["red", "green", "yellow", "blue"]
    pointer = 0
    pygame.init()
    load_color_images(screen)
    while color_not_selected:
        pointer = move_color_pointer(screen, pointer, "")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    clean_color_screen(screen)
                    pointer = move_color_pointer(screen, pointer, "left")
                if event.key == pygame.K_RIGHT:
                    clean_color_screen(screen)
                    pointer = move_color_pointer(screen, pointer, "right")
                if event.key == pygame.K_TAB:
                    color_not_selected = False

    time.sleep(2)
    pygame.quit()
    return color_list[pointer]
        
def main():
    player = Player()
    player_conexion_thread = threading.Thread(target = player.connect, args = (str(sys.argv[2]), int(sys.argv[3])))
    player_conexion_thread.start()
    
    actual_message = ""
    turn_owner = ""
    
    while player.game_switch:
        
        if actual_message != player.data_received_server:
            print "CLIENT: Checking Recieved data: ", player.data_received_server
            actual_message = player.data_received_server

        if type(player.data_received_server) == type([]) and len(player.data_received_server) > 0:
            
            if player.data_received_server[0] == 'get_time':
                print "GET TIME MESSAGE"
                gap = time.time() - float(player.data_received_server[1])
                player.sock.sendall(str(gap))
                time.sleep(0.01)
                player.data_received_server = []
            
            elif player.data_received_server[0] == 'post_time':
                print "POST TIME MESSAGE"
                local_time = float(player.data_received_server[1])
                print "CLIENT: New time: {0}".format(local_time)
                time.sleep(0.01)
                player.data_received_server = []
                
            elif player.data_received_server[0] == '':
                break
                
            elif player.data_received_server[0] == 'get_username':
                print "GET NAME MESSAGE"
                try:
                    username = str(sys.argv[1])
                except:
                    username = raw_input("CLIENT: Enter your name: ")
                player.sock.sendall(username)
                player.data_received_server = []

            elif player.data_received_server[0] == 'repeated_username':
                print "REPEATED USERNAME MESSAGE"
                username = raw_input("CLIENT: Choose another username: ")
                player.sock.sendall(username)
                player.data_received_server = []
                
            elif player.data_received_server[0] == 'get_color':
                print "GET COLOR MESSAGE"
                try:
                    selected_color = select_color()
                except:
                    print "ERROR SELCTING COLOR"
                player.sock.sendall(selected_color)
                player.data_received_server = []
                
            elif player.data_received_server[0] == 'repeated_color':
                print "REPEATED COLOR MESSAGE"
                selected_color = select_color()
                player.sock.sendall(selected_color)
                player.data_received_server = []
                
           elif player.data_received_server[0] == 'throw_dice_ft':
                print "THROW DICE FT MESSAGE"
                try:
                    screen = pygame.display.set_mode((415, 200))
                    pygame.display.set_caption("Throw dice")
                    pygame.init()
                    dice_ft = Throw_dice(screen, 130, 70)
                    pygame.quit()
                except:
                    print "ERROR SELCTING COLOR"
                player.sock.sendall(dice_ft)
                player.data_received_server = []
                
        
    
        
if __name__ == '__main__':
    main()
