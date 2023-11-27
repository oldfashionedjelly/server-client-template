import pygame
import toolbox
import random
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep


running = True


class MyGameClient(ConnectionListener):
    def __init__(self, host, port):
        """
        Client constructor function. This is the code that runs once
        when a new client is made.
        """
        ConnectionListener.__init__(self)
        
        # Start the game
        pygame.init()
        pygame.mixer.pre_init(buffer=1024)
        game_width = 1000
        game_height = 650
        self.screen = pygame.display.set_mode((game_width, game_height))
        self.clock = pygame.time.Clock()

        self.stuffToDraw = []
        self.stuffToDrawNext = []
        
        self.background = pygame.image.load("../assets/bg_lab.png")
        self.avatar_image = pygame.image.load("../assets/Monkey/Monkey_idle_1.png")

        self.small_font = pygame.font.SysFont("default", 30)
        self.ready_text = self.small_font.render("Ready!", True, (0, 255, 0))
        self.not_ready_text = self.small_font.render("Not Ready", True, (0, 0, 255))

        self.medium_font = pygame.font.SysFont("default", 45)

        self.connected = False

        self.Connect((host, port))


    def update(self):
        """
        Client update function. This is the function that runs over and
        over again, once every frame of the game.
        """
        connection.Pump()
        self.Pump()
        #connection.Send({"action": "hi"})

        # Set running to False if the player clicks the X or presses esc
        global running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        connection.Send({"action": "keys", "keys": pygame.key.get_pressed()})

        for item in self.stuffToDraw:
            self.screen.blit(item[0], item[1])
            
        # Tell pygame to update the screen
        pygame.display.flip()
        self.clock.tick(30)
        pygame.display.set_caption("GET CONNECTED! fps: " + str(self.clock.get_fps()))


    def ShutDown(self):
        """
        Client ShutDown function. Disconnects and closes the game.
        """
        self.connected = False
        connection.Close()
        pygame.quit()
        exit()
        
                
    #####################################
    ### Client-side Network functions ###
    #####################################
    """
    Each one of these "Network_" functions defines a command
    that the server will tell you (the client) to do.
    """
    def Network_flip(self, data):
        self.stuffToDraw.clear()
        for item in self.stuffToDrawNext:
            self.stuffToDraw.append(item)
        self.stuffToDrawNext.clear()

    def Network_draw_background(self, data):
        self.stuffToDrawNext.append([self.background, (0, 0)])

    def Network_draw_avatar(self, data):
        avatar_rect = self.avatar_image.get_rect(center=data["coords"])
        self.stuffToDrawNext.append([self.avatar_image, avatar_rect])

        if data["ready"]:
            text_to_draw = self.ready_text
        else:
            text_to_draw = self.not_ready_text
        text_rect = text_to_draw.get_rect(midtop = avatar_rect.midbottom)
        self.stuffToDrawNext.append([text_to_draw, text_rect])

        number_text = self.medium_font.render(str(data["number"]), True, data["color"])    
        text_rect = number_text.get_rect(midbottom = avatar_rect.midtop)
        self.stuffToDrawNext.append([number_text, text_rect])
        
    def Network_connected(self, data):
        """
        Network_connected runs when you successfully connect to the server
        """
        self.connected = True
        print("Connection succesful!")
    
    def Network_error(self, data):
        """
        Network_error runs when there is a server error
        """
        print('error:', data['error'][1])
        self.ShutDown()
    
    def Network_disconnected(self, data):
        """
        Network_disconnected runs when you disconnect from the server
        """
        print('Server disconnected')
        self.ShutDown()


ip = "192.168.1.39" #input("Please enter the host's IP address: ")
port = 5555
thisClient = MyGameClient(ip, port)

"""This is the loop that keeps going until the game is closed"""
while running:
    thisClient.update()
    
thisClient.ShutDown()
