import socket
import sys
import time
import pygame
import threading
import random
import pickle

WINDOW_DIMENSIONS = (1100, 768)

ALL_PIECES_LIST = { 
'yellow': [{'id':0, 'x':0, 'y':0, 'bmp':5, 'bmps':5, 'jail':True, 'jail_pos':[555, 600]},
	      {'id':1, 'x':0, 'y':0, 'bmp':5, 'bmps':5, 'jail':True, 'jail_pos':[690, 600]},
	      {'id':2, 'x':0, 'y':0, 'bmp':5, 'bmps':5, 'jail':True, 'jail_pos':[560, 665]},
	      {'id':3, 'x':0, 'y':0, 'bmp':5, 'bmps':5, 'jail':True, 'jail_pos':[685, 665]}],
          
'red': [{'id':0, 'x':0, 'y':0, 'bmp':39, 'bmps':39, 'jail':True, 'jail_pos':[70, 90]},
	      {'id':1, 'x':0, 'y':0, 'bmp':39, 'bmps':39, 'jail':True, 'jail_pos':[185, 90]},
	      {'id':2, 'x':0, 'y':0, 'bmp':39, 'bmps':39, 'jail':True, 'jail_pos':[70, 150]},
	      {'id':3, 'x':0, 'y':0, 'bmp':39, 'bmps':39, 'jail':True, 'jail_pos':[185, 150]}],
          
'green': [{'id':0, 'x':0, 'y':0, 'bmp':56, 'bmps':56, 'jail':True, 'jail_pos':[70, 600]},
	      {'id':1, 'x':0, 'y':0, 'bmp':56, 'bmps':56, 'jail':True, 'jail_pos':[185, 600]},
	      {'id':2, 'x':0, 'y':0, 'bmp':56, 'bmps':56, 'jail':True, 'jail_pos':[70, 665]},
	      {'id':3, 'x':0, 'y':0, 'bmp':56, 'bmps':56, 'jail':True, 'jail_pos':[185, 665]}],
          
'blue': [{'id':0, 'x':0, 'y':0, 'bmp':22, 'bmps':22, 'jail':True, 'jail_pos':[565, 90]},
	      {'id':1, 'x':0, 'y':0, 'bmp':22, 'bmps':22, 'jail':True, 'jail_pos':[680, 90]},
	      {'id':2, 'x':0, 'y':0, 'bmp':22, 'bmps':22, 'jail':True, 'jail_pos':[565, 150]},
	      {'id':3, 'x':0, 'y':0, 'bmp':22, 'bmps':22, 'jail':True, 'jail_pos':[680, 150]}]
}

BOARD_MAP = [{'x':-1, 'y':-1, 'secure':False, 'entry':None, 'num_pie':-1, 'coord_inc':-1},
{'x':430, 'y':735, 'secure':False, 'num_pie':0, 'coord_inc':'x'},
{'x':430, 'y':695, 'secure':False, 'num_pie':0, 'coord_inc':'x'},
{'x':430, 'y':660, 'secure':False, 'num_pie':0, 'coord_inc':'x'},
{'x':430, 'y':625, 'secure':False, 'num_pie':0, 'coord_inc':'x'},
{'x':430, 'y':590, 'secure':True,  'num_pie':0, 'coord_inc':'x'},
{'x':430, 'y':555, 'secure':False, 'num_pie':0, 'coord_inc':'x'},
{'x':430, 'y':520, 'secure':False, 'num_pie':0, 'coord_inc':'x'},
{'x':430, 'y':485, 'secure':False, 'num_pie':0, 'coord_inc':'x'},
{'x':485, 'y':425, 'secure':False, 'num_pie':0, 'coord_inc':'y'},
{'x':520, 'y':427, 'secure':False, 'num_pie':0, 'coord_inc':'y'},
{'x':555, 'y':427, 'secure':False, 'num_pie':0, 'coord_inc':'y'},
{'x':590, 'y':427, 'secure':True,  'num_pie':0, 'coord_inc':'y'},
{'x':625, 'y':427, 'secure':False, 'num_pie':0, 'coord_inc':'y'},
{'x':670, 'y':427, 'secure':False, 'num_pie':0, 'coord_inc':'y'},
{'x':695, 'y':427, 'secure':False, 'num_pie':0, 'coord_inc':'y'},
{'x':735, 'y':427, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':735, 'y':345, 'secure':True,  'num_pie':0, 'coord_inc':'y'},
{'x':730, 'y':265, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':695, 'y':265, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':660, 'y':265, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':625, 'y':265, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':590, 'y':265, 'secure':True,  'num_pie':0, 'coord_inc':'y'},
{'x':555, 'y':265, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':520, 'y':265, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':485, 'y':280, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':430, 'y':260, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':430, 'y':225, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':430, 'y':190, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':430, 'y':155, 'secure':True,  'num_pie':0, 'coord_inc':'x'},
{'x':430, 'y':120, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':430, 'y':95, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':430, 'y':60, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':430, 'y':20, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':345, 'y':20, 'secure':True,  'num_pie':0, 'coord_inc':'x'},
{'x':265, 'y':20, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':265, 'y':55, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':265, 'y':90, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':265, 'y':125, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':265, 'y':160, 'secure':True,  'num_pie':0, 'coord_inc':'x'},
{'x':265, 'y':195, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':265, 'y':230, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':280, 'y':263, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':260, 'y':280, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':235, 'y':265, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':195, 'y':265, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':160, 'y':265, 'secure':True,  'num_pie':0, 'coord_inc':'y'},
{'x':125, 'y':265, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':90, 'y':265, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':55, 'y':265, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':20, 'y':265, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':20, 'y':345, 'secure':True,  'num_pie':0, 'coord_inc':'y'},
{'x':20, 'y':430, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':55, 'y':430, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':90, 'y':430, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':125, 'y':430, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':160, 'y':430, 'secure':True,  'num_pie':0, 'coord_inc':'y'},
{'x':195, 'y':430, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':230, 'y':430, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':265, 'y':430, 'secure':False,  'num_pie':0, 'coord_inc':'y'},
{'x':280, 'y':485, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':265, 'y':515, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':265, 'y':550, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':265, 'y':585, 'secure':True,  'num_pie':0, 'coord_inc':'x'},
{'x':265, 'y':620, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':265, 'y':655, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':265, 'y':690, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':265, 'y':725, 'secure':False,  'num_pie':0, 'coord_inc':'x'},
{'x':345, 'y':725, 'secure':True,  'num_pie':0, 'coord_inc':'x'}
]

class Player:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_switch = True
        self.username = ""
        self.data_received_server = ""
        self.color = ""
        self.username = ""
        self.have_shift = False
        self.firts_time_injail = True
        self.allplayers_pieces_list = {}
        self.board_map = []
        self.allplayers_piecesimg_list = {}

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
    
    def throw_dice(self, screen, cordx, cordy):
        
        diceimg1 = pygame.image.load("img/dado1.png").convert_alpha()
        diceimg2 = pygame.image.load("img/dado2.png").convert_alpha()
        diceimg3 = pygame.image.load("img/dado3.png").convert_alpha()
        diceimg4 = pygame.image.load("img/dado4.png").convert_alpha()
        diceimg5 = pygame.image.load("img/dado5.png").convert_alpha()
        diceimg6 = pygame.image.load("img/dado6.png").convert_alpha()
        
        pygame.display.flip()
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)
        unleashed_dice = True
        
        while unleashed_dice:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        unleashed_dice = False
                        for i in range (2):
                            screen.blit(diceimg1,(cordx, cordy))
                            screen.blit(diceimg5, (cordx+70, cordy))
                            time.sleep(0.1)
                            pygame.display.flip()
                            screen.blit(diceimg2,(cordx, cordy))
                            screen.blit(diceimg4, (cordx+70, cordy))
                            time.sleep(0.1)
                            pygame.display.flip()
                            screen.blit(diceimg3,(cordx, cordy))
                            screen.blit(diceimg1, (cordx+70, cordy))
                            time.sleep(0.1)
                            pygame.display.flip()
                            screen.blit(diceimg4,(cordx, cordy))
                            screen.blit(diceimg2, (cordx+70, cordy))
                            time.sleep(0.1)
                            pygame.display.flip()
                            screen.blit(diceimg5,(cordx, cordy))
                            screen.blit(diceimg6, (cordx+70, cordy))
                            time.sleep(0.1)
                            pygame.display.flip()
                            screen.blit(diceimg6,(cordx, cordy))
                            screen.blit(diceimg3, (cordx+70, cordy))
                            time.sleep(0.1)
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
        
        dice_value = []
        dice_value.append(dice1)
        dice_value.append(dice2)
        return dice_value
        
    def load_pieces_images(self):
        all_players_pieces_list = {}
        ficha_roja1 = pygame.image.load("img/ficha_roja.png").convert_alpha()
        ficha_roja2 = pygame.image.load("img/ficha_roja.png").convert_alpha()
        ficha_roja3 = pygame.image.load("img/ficha_roja.png").convert_alpha()
        ficha_roja4 = pygame.image.load("img/ficha_roja.png").convert_alpha()
        ficha_amarilla1 = pygame.image.load("img/ficha_amarilla.png").convert_alpha()
        ficha_amarilla2 = pygame.image.load("img/ficha_amarilla.png").convert_alpha()
        ficha_amarilla3 = pygame.image.load("img/ficha_amarilla.png").convert_alpha()
        ficha_amarilla4 = pygame.image.load("img/ficha_amarilla.png").convert_alpha()
        ficha_verde1 = pygame.image.load("img/ficha_verde.png").convert_alpha()
        ficha_verde2 = pygame.image.load("img/ficha_verde.png").convert_alpha()
        ficha_verde3 = pygame.image.load("img/ficha_verde.png").convert_alpha()
        ficha_verde4 = pygame.image.load("img/ficha_verde.png").convert_alpha()
        ficha_azul1 = pygame.image.load("img/ficha_azul.png").convert_alpha()
        ficha_azul2 = pygame.image.load("img/ficha_azul.png").convert_alpha()
        ficha_azul3 = pygame.image.load("img/ficha_azul.png").convert_alpha()
        ficha_azul4 = pygame.image.load("img/ficha_azul.png").convert_alpha()
        self.allplayers_piecesimg_list = { 
        "red":[ficha_roja1, ficha_roja2, ficha_roja3, ficha_roja4],
        "yellow":[ficha_amarilla1, ficha_amarilla2, ficha_amarilla3, ficha_amarilla4],
        "green":[ficha_verde1, ficha_verde2, ficha_verde3, ficha_verde4],
        "blue":[ficha_azul1, ficha_azul2, ficha_azul3, ficha_azul4]
        }
        
    def show_players_pieces(self, screen):
        for key, players_pieces_list in self.allplayers_pieces_list.iteritems():
            for piece in players_pieces_list:
                if piece['jail']:
                    screen.blit(self.allplayers_piecesimg_list[key][piece['id']], piece['jail_pos'])
                else:
                    screen.blit(self.allplayers_piecesimg_list[key][piece['id']], (piece['x'], piece['y']))
        pygame.display.flip()
        
    def out_jail(self, screen, color):
        pieces_list = self.allplayers_pieces_list[color]
        for piece in pieces_list:
            piece['x'] = self.board_map[piece['bmps']]['x']
            piece['y'] = self.board_map[piece['bmps']]['y']
            piece['bmp'] = piece['bmps']
            piece[self.board_map[piece['bmps']]['coord_inc']] += self.board_map[piece['bmps']]['num_pie']*25
            self.board_map[piece['bmps']]['num_pie'] += 1
            screen.blit(self.allplayers_piecesimg_list[self.color][piece['id']], (piece['x'], piece['y']))
        pygame.display.flip()

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

    time.sleep(1)
    pygame.quit()
    return color_list[pointer]
        
def main():
    player = Player()
    player_conexion_thread = threading.Thread(target = player.connect, args = (str(sys.argv[2]), int(sys.argv[3])))
    player_conexion_thread.start()
    
    actual_message = ""
    turn_owner = ""
    init_game = False
    
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
                player.username = username
                player.data_received_server = []

            elif player.data_received_server[0] == 'repeated_username':
                print "REPEATED USERNAME MESSAGE"
                username = raw_input("CLIENT: Choose another username: ")
                player.sock.sendall(username)
                player.username = username
                player.data_received_server = []
                
            elif player.data_received_server[0] == 'get_color':
                print "GET COLOR MESSAGE"
                selected_color = select_color()
                player.sock.sendall(selected_color)
                player.color = selected_color
                player.data_received_server = []
                
            elif player.data_received_server[0] == 'repeated_color':
                print "REPEATED COLOR MESSAGE"
                selected_color = select_color()
                player.sock.sendall(selected_color)
                player.color = selected_color
                player.data_received_server = []
                
            elif player.data_received_server[0] == 'throw_dice_ft':
                print "THROW DICE FT MESSAGE"
                screen = pygame.display.set_mode((415, 200))
                pygame.display.set_caption("Throw dice")
                pygame.init()
                dice_ft = []
                dice_ft = player.throw_dice(screen, 130, 70)
                time.sleep(1)
                pygame.quit()
                player.sock.sendall(str(dice_ft[0]+dice_ft[1]))
                player.data_received_server = []
                
            elif player.data_received_server[0] == 'init':
                print "INIT GAME MESSAGE"
                pygame.init()
                init_game = True
                screen = pygame.display.set_mode((1100, 768))
                pygame.display.set_caption("PARCHEESI")
                screen.blit(pygame.image.load("img/parchis.png"), (0, 0))
                pygame.display.flip()
                player.load_pieces_images()
                player.allplayers_pieces_list = ALL_PIECES_LIST
                player.board_map = BOARD_MAP
                player.show_players_pieces(screen)
                player.data_received_server = []
                player.sock.sendall("ack")
                
            elif player.data_received_server[0] == 'your_turn':
                player.have_shift = True
                #~ jugador.posee_turno = ""
                #~ poseedor_act = ""
                print "CLIENT: I own the turn"
                player.sock.sendall("ack")
                player.data_received_server = []
                
            elif player.data_received_server[0] == 'player_jailout':
                player.out_jail(screen, player.data_received_server[1])
                player.sock.sendall("ack")
                player.data_received_server = []
                
                
        if init_game:
            if player.have_shift:
                if player.firts_time_injail: 
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            game_switch = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                for i in range(3):
                                    
                                    dices = player.throw_dice(screen, 800, 35)
                                    
                                    if dices[0] == dices[1]:
                                        player.out_jail(screen, player.color)
                                        player.firts_time_injail = False 
                                        player.soc.sendall("jail_out" + player.color)
                                        player.have_shift = False
                                    
                                print "FINE"
                
        
if __name__ == '__main__':
    main()
