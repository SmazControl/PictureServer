"""
PICTURE SERVER 2 .py
20 May 2019 
Supot Sawangpiriyakij
Bunnavit Sawangpiriyakij EENG

Base on Python 3.7

UPTO
30 Categories
30 Pictures per Category
 9 Clients

Client use WebView App on Android
Setting URL http://ip-address:8080/index(number)
number = Client Number
"""
import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import socket
import socketserver
from shutil import copyfile

PORT = 8080
timeout= 0.5
        
Handler = http.server.SimpleHTTPRequestHandler

Handler.extensions_map={
        '.manifest': 'text/cache-manifest',
	'.html': 'text/html',
        '.png': 'image/png',
	'.jpg': 'image/jpg',
	'.svg':	'image/svg+xml',
	'.css':	'text/css',
	'.js':	'application/x-javascript',
	'': 'application/octet-stream', # Default
    }

# Import a library of functions called 'pygame'
import pygame
import os
import sys
from pygame import mouse
import threading 

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

PI = 3.141592653


# for Python 3
def xrange(x,y):
    return iter(range(x,y))

class MIMEServerThread(threading.Thread):
    def __init__(self):
        self.busy = False        
        threading.Thread.__init__(self)
    
    def run(self):
        self.busy = True
        # HTTP Server Section
        try:
            httpd = WebHTTPServer(("", PORT), Handler)
            print("serving at port", PORT)
        except:
            pass    
        try:
            httpd.handle_request()
        except:
            pass
        self.busy = False        

# Cria uma classe para armazenar os atributos do nosso heroi
class Picture(object):
    # Deixei alguns valores por padrao apenas por comodidade
    def __init__(self, image_path = "C:/Users/Admin/Desktop/Picture/chew.png", scale = (100,160), pos = [100, 200], opos = [100, 200]):
        # Caminho para a imagem que ira representar o heroi
        self.image_path = image_path
        # Posicao inicial do heroi na tela
        self.position = pos
        # Escala fixa do heroi
        self.scale = scale
        # Variavel utilizada para saber se o heroi esta selecionado ou nao
        self.held = False
        self.hide = False
        self.num = -1
        self.opos = opos
        self.opos_x = opos[0] # Big bug in Pygame Array diff.
        self.opos_y = opos[1]
        
        # Carrega a imagem do heroi
        self.image = pygame.image.load(self.image_path).convert_alpha()
        # Redimensiona a imagem para a escala definida
        self.image = pygame.transform.scale(self.image, self.scale)

class Client(object):
    def __init__(self, image_path = "C:/Users/Admin/Desktop/Picture/chew.png", scale = (100,160), pos = [100, 200], opos = [100, 200]):
        self.image_path = image_path
        self.position = pos
        self.scale = scale
        self.held = False
        self.hide = False
        self.num = -1
        self.opos = opos
        self.opos_x = opos[0]
        self.opos_y = opos[1]

        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scale)

class Rect(object):
    def __init__(self, x=0, y=0, w=20, d=20, txt=""):
        self.rect = pygame.Rect([x+2,y+2,w-4,d-4])
        self.table = [x,y,w,d]
        self.text = txt
        self.on_click = False

class Button(object):
    def __init__(self, x=20, y=20, w=100, d=20, textcolor=BLACK, text="", boo=True, bgcolor=WHITE, df=False, group=1, mode=0):
        self.rect = pygame.Rect([x,y,w,d])
        self.default = df
        self.x = x
        self.y = y
        self.w = w
        self.d = d
        self.textcolor = textcolor
        self.text = text
        self.boo = boo
        self.bgcolor = bgcolor
        self.group = group
        self.mode = mode
                
# Classe principal responsavel pela logica do jogo
class UI(object):

    def __init__(self):
        self.webPath = "C:/Users/Admin/Desktop/Picture"
        self.message = ""
        self.sub = True
        self.category = []
        self.category_number = 0
        self.category_rects = []
        # Initialize the game engine
        pygame.init()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.size = self.screen.get_size()
        x,y = self.size
        os.chdir(self.webPath)
        dirlist = os.listdir()
        y_add = 0
        for xdir in dirlist:
           if xdir.find(".",0)==(-1):
              self.category.append(xdir)
              self.category_rects.append(Rect(x-490, 20+y_add, 370, 25,"Category: "+xdir))
              print("load "+xdir)
              y_add+=25
        
        # Utiliza uma lista para armazenar os herois do jogo
        self.mode = 0 # mode 0 = Picks : mode 1 = All
        self.lotImg = []
        self.pictures = []
        self.clients = []
        self.buttons = []
        self.picture_held_number = -1
        self.picture_held_image_path = ""
        self.client_held_number = -1
        self.client_held_image_path = ""        
        self.rects = []
        self.mouse_mode = False
        self.mouse_mode_position = [0,0]
        self.client_number = 6

        # Utilizado para controlar a velocidade de quadros (de atualizacoes da tela)
        self.clock = pygame.time.Clock()

    def init_picture(self):
        os.chdir(self.webPath+"/"+ui.category[ui.category_number])
        dirlist = os.listdir()
        os.chdir(self.webPath)
        self.lotImg = []
        for xdir in dirlist:
            if xdir[xdir.find(".",0):]==".jpg":
                self.lotImg.append(xdir) 
        sx = 0
        sy = 0
        self.pictures = []
        for xImg in self.lotImg:
            os.chdir(self.webPath+"/"+ui.category[ui.category_number])        
            self.pictures.append(Picture(xImg, (75, 100), [x-(590-sx), 70+sy], [x-(590-sx), 70+sy]))
            os.chdir(self.webPath)
            sx+=85
            if sx>490:
                sx = 0
                sy+= 110
                
    def init_client(self):
        sx = 150
        sy = 150
        self.clients = []
        for cn in xrange(0,self.client_number):
            self.clients.append(Client(self.webPath+"/blank.jpg", (75, 100), [sx, sy], [sx, sy]))    
            sx+=150
            if sx>450:
                sx = 150
                sy+= 200        

    def button(self, x=20, y=20, w=99, d=26, textcolor=BLACK, txt="", boo=True, bgcolor=WHITE, default=False, group=1, mode=0):
        self.buttons.append(Button(x,y,w,d,textcolor,txt,boo,bgcolor,default,group,mode))
            
    def draw_button(self):
        for i in range(len(self.buttons)):
           if self.buttons[i].default:
              pygame.draw.rect(self.screen, self.buttons[i].textcolor, [self.buttons[i].x, self.buttons[i].y, self.buttons[i].w-1, self.buttons[i].d+1])
              text = font.render(self.buttons[i].text, self.buttons[i].boo, self.buttons[i].bgcolor)
           else:
              pygame.draw.rect(self.screen, self.buttons[i].textcolor, [self.buttons[i].x, self.buttons[i].y, self.buttons[i].w, self.buttons[i].d], 2)
              text = font.render(self.buttons[i].text, self.buttons[i].boo, self.buttons[i].textcolor)
           self.screen.blit(text, [self.buttons[i].x+2, self.buttons[i].y+2])    
        

    def is_mouse_same_position(self):
        mouse_pos = mouse.get_pos()
        if mouse_pos == self.mouse_mode_position:
           return True
        else:
           return False

    # Funcao utilizada para verificar se a posicao do mouse esta em cima
    # de um heroi (passado por parametro)
    def is_over(self, mouse_pos, picture):
        # Verifica a posicao no eixo X
        if mouse_pos[0] > picture.position[0] and mouse_pos[0] < picture.position[0] + picture.scale[0]:
            # Verifica a posicao no eixo Y
            if mouse_pos[1] > picture.position[1] and mouse_pos[1] < picture.position[1] + picture.scale[1]:
                return True
        return False

    def reset_button(self):
        for j in xrange(0, len(self.clients)):
            self.clients[j].position = [self.clients[j].opos_x, self.clients[j].opos_y]
            self.clients[j].image_path = self.webPath+"/blank.jpg"
            self.clients[j].image = pygame.image.load(self.clients[j].image_path).convert_alpha()
            self.clients[j].image = pygame.transform.scale(self.clients[j].image, self.clients[j].scale)
            self.clients[j].num = -1
            self.clients[j].hide = False                         
            self.clients[j].held = False
        for j in xrange(0, len(self.pictures)):
            self.pictures[j].num = -1
            self.pictures[j].position = [self.pictures[j].opos_x, self.pictures[j].opos_y]
            self.pictures[j].hide = False
            self.pictures[j].held = False
        

    # Funcao chamada quando o usuario clica com o mouse
    def mouse_button_down(self):
        # Obtem a posicao atual do mouse
        mouse_pos = mouse.get_pos()

        # normal state
        if self.mouse_mode == False:
           # check over button
           for i in xrange(0, len(self.buttons)): 
               if self.buttons[i].rect.collidepoint(mouse_pos):
                  if self.buttons[i].mode != -1:
                     self.mode = self.buttons[i].mode
                     if self.buttons[i].default:
                        self.buttons[i].default = False
                        gp = self.buttons[i].group
                        for j in xrange(0, len(self.buttons)):
                            if gp == self.buttons[j].group and i!=j:
                               self.buttons[j].default = True
                     else:
                        self.buttons[i].default = True
                        gp = self.buttons[i].group
                        for j in xrange(0, len(self.buttons)):
                            if gp == self.buttons[j].group and i!=j:
                               self.buttons[j].default = False                     
                  elif self.buttons[i].group == 2: # Reset button
                     self.reset_button()
                  elif self.buttons[i].group == 3: # (+) button
                     if self.client_number<9:
                        self.client_number+=1
                        self.init_client()
                        self.reset_button()
                  elif self.buttons[i].group == 4: # (-) button
                     if self.client_number>1:
                        self.client_number-=1
                        self.init_client()
                        self.reset_button()
                  elif self.buttons[i].group == 5: # SUB button
                     if self.sub:
                        self.sub = False
                     else:
                        self.sub = True
                  self.draw_button()
               
           # Mouse over Pictures
           for i in xrange(0, len(self.pictures)):
               # Mode Picks
               if self.mode == 0:
                  # Somente "ativa" a imagem_selecionada se o usuario clicou em cima da imagem
                  if self.is_over(mouse_pos, self.pictures[i]):
                     self.pictures[i].held = True
                     self.picture_held_number = i
                     self.picture_held_image_path = self.pictures[i].image_path
                     self.mouse_mode = True
                     self.mouse_mode_position = mouse_pos
               # Mode ALL
               elif self.mode == 1:
                  if self.is_over(mouse_pos, self.pictures[i]):
                     for cn in xrange(0,self.client_number):
                         if self.clients[cn].num >= 0:
                             self.pictures[self.clients[cn].num].position = [self.pictures[self.clients[cn].num].opos_x, self.pictures[self.clients[cn].num].opos_y]
                             self.pictures[self.clients[cn].num].hide = False
                         self.clients[cn].image_path = self.pictures[i].image_path
                         self.clients[cn].num = i
                         self.clients[cn].image = pygame.image.load(self.webPath+"/"+self.category[self.category_number]+"/"+self.clients[cn].image_path).convert_alpha()
                         self.clients[cn].image = pygame.transform.scale(self.clients[cn].image, self.clients[cn].scale)
                         copyfile(self.webPath+"/"+self.category[self.category_number]+"/"+self.clients[cn].image_path,self.webPath+"/image"+str(cn+1)+".jpg")
                         self.pictures[i].hide = True

           # Mouse over Clients
           for i in xrange(0, len(self.clients)):
               if self.is_over(mouse_pos, self.clients[i]):
                  self.clients[i].held = True
                  self.client_held_number = i
                  self.client_held_image_path = self.clients[i].image_path
                  self.mouse_mode = True
                  self.mouse_mode_position = mouse_pos


           #if rect.collidepoint(mouse_pos)):
           for i in xrange(0, len(self.rects)):
               if self.rects[i].on_click:
                  for j in xrange(0, len(self.category_rects)):
                      if self.category_rects[j].rect.collidepoint(mouse_pos):
                          self.rects[i].on_click = False
                          self.rects[i].text = "Category: "+self.category[j]
                          self.category_number = j
                          self.init_picture()
                          # hide pictures that already Pick
                          for k in xrange(0, len(self.pictures)):
                              for l in xrange(0, len(self.clients)):
                                  if self.clients[l].image_path == self.pictures[k].image_path:
                                      self.pictures[k].hide = True
               else:
                  if self.rects[i].rect.collidepoint(mouse_pos):
                      self.rects[i].on_click = True                      
        else: # after Pick state
           if self.is_mouse_same_position()==False:
              if self.picture_held_number >= 0:
                 for cn in xrange(0,self.client_number):
                     if self.is_over(mouse_pos, self.clients[cn]):
                        if self.clients[cn].num >= 0:
                           self.pictures[self.clients[cn].num].position = [self.pictures[self.clients[cn].num].opos_x, self.pictures[self.clients[cn].num].opos_y]
                           self.pictures[self.clients[cn].num].hide = False
                        self.clients[cn].image_path = self.picture_held_image_path
                        self.clients[cn].num = self.picture_held_number
                        self.clients[cn].image = pygame.image.load(self.webPath+"/"+self.category[self.category_number]+"/"+self.clients[cn].image_path).convert_alpha()
                        self.clients[cn].image = pygame.transform.scale(self.clients[cn].image, self.clients[cn].scale)
                        copyfile(self.webPath+"/"+self.category[self.category_number]+"/"+self.clients[cn].image_path,self.webPath+"/image"+str(cn+1)+".jpg")
                        self.pictures[self.picture_held_number].hide = True
           # 'Libera' todos os herois
           for i in xrange(0, len(self.pictures)):
               self.pictures[i].held = False
           for i in xrange(0, len(self.clients)):
               self.clients[i].held = False
           self.mouse_mode = False
           self.picture_held_number = -1
           self.picture_held_image_path = ""
           self.client_held_number = -1
           self.client_held_image_path =""

    # Funcao responsavel por atualizar a posicao de todos os herois
    def update_position(self):
        # Obtem a posicao atual do mouse
        mouse_pos = mouse.get_pos()
        for i in xrange(0, len(self.pictures)):
            # Se a variavel imagem_selecionada estiver "ativa" (True), atualiza a posicao da imagem
            if self.pictures[i].held:
                # Define as posicoes X e Y da imagem, posiciona a imagem com o mouse centralizado
                self.pictures[i].position[0] = mouse_pos[0] - self.pictures[i].scale[0]/2
                self.pictures[i].position[1] = mouse_pos[1] - self.pictures[i].scale[1]/2
        for i in xrange(0, len(self.clients)):
            if self.clients[i].held:
                self.clients[i].position[0] = mouse_pos[0] - self.clients[i].scale[0]/2
                self.clients[i].position[1] = mouse_pos[1] - self.clients[i].scale[1]/2

    def draw_rect(self):
        for i in xrange(0, len(self.rects)):
            if self.rects[i].on_click:
               for j in xrange(0,len(self.category)):
                   text = font.render(self.category_rects[j].text, True, BLACK)
                   pygame.draw.rect(ui.screen, WHITE, self.category_rects[j].table)                   
                   ui.screen.blit(text, self.category_rects[j].rect)
                   pygame.draw.rect(ui.screen, BLACK, self.category_rects[j].table, 2)
            else:
               text = font.render(self.rects[i].text, True, BLACK)
               ui.screen.blit(text, self.rects[i].rect)
               pygame.draw.rect(ui.screen, BLACK, self.rects[i].table, 2)

        
ui = UI()
x, y = ui.size

pygame.display.set_caption("Picture Server")

done = False
clock = pygame.time.Clock()

ui.init_picture()
ui.init_client()

socketserver.TCPServer.allow_reuse_address=True
httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.timeout = 0.5

#PictureServer2
# 6 Thread for more powerful
for i in range(6):
   print("serving at port", PORT)
   thread = threading.Thread(target = httpd.serve_forever)
   thread.daemon = True
   try:
      thread.start()
   except:
      pass

# Select the font to use, size, bold, italics
font = pygame.font.SysFont('Calibri', 25, True, False)
font1 = pygame.font.SysFont('Calibri', 10, True, False)
ui.rects.append(Rect(x-490, 20, 370, 25,"Category: "+ui.category[ui.category_number]))
server = MIMEServerThread()
ui.button(20, 20, 100, 25, BLACK, "Picks", True, WHITE, True, 1, 0)
ui.button(120, 20, 100, 25, BLACK, "ALL", True, WHITE, False, 1, 1)
ui.button(x-925, 20, 100, 25, BLACK, "Reset", True, WHITE, False, 2, -1)
ui.button(x-720, 20, 50, 25, BLACK, "   +", True, WHITE, False, 3, -1)
ui.button(x-670, 20, 50, 25, BLACK, "   -", True, WHITE, False, 4, -1)
ui.button(x-120, 20, 100, 25, BLACK, " SUB", True, WHITE, False, 5, -1)

# Loop until the user clicks the close button.
done = False
while not done:

    # Pygame Section
    for event in pygame.event.get():  # User did something
       if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE or event.unicode == 'q':
             done = True  # Flag that we are done so we exit this loop
             break
       elif event.type == pygame.MOUSEBUTTONDOWN:
          ui.mouse_button_down()
            # Chama a funcao que atualiza a posicao dos herois
    if ui.mouse_mode:
       ui.update_position()    

    # Clear the screen and set the screen background
    ui.screen.fill(WHITE)
    
    pygame.draw.rect(ui.screen, BLACK, [10,10, x-620 , y-20], 5)
    pygame.draw.rect(ui.screen, BLACK, [x-600,10, 590 , y-20], 5)
 
    ui.draw_button()    
    #text = font.render(str(x)+","+str(y), True, BLACK)
    #text = pygame.transform.rotate(text, 0)
    #screen.blit(text, [20, 40])
    #sy = 0
    #for xdir in dirlist:
    #   if xdir[xdir.find(".",0):]==".jpg":
    #      text = font.render(xdir, True, BLACK)
    #      screen.blit(text, [20, 60+sy])
    #      sy+=20
    pygame.draw.rect(ui.screen, BLACK, [x-820, 20, 100, 25], 2)
    text = font.render("Client "+str(ui.client_number), True, BLACK)
    ui.screen.blit(text, [x-818, 22])

    pygame.draw.rect(ui.screen, BLACK, [x-590, 20, 100, 25], 2)
    text = font.render("Server", True, BLACK)
    ui.screen.blit(text, [x-588, 22])

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    text = font.render("http://"+IPAddr+":8080/index1.html (for client 1)", True, BLACK)
    ui.screen.blit(text, [20, y-40])
    
    # Debug Section
    #text = font.render(ui.message, True, BLACK)
    #ui.screen.blit(text, [x-588, y-60])
    #ss =""
    #for i in xrange(0, len(ui.clients)):
    #    if ui.clients[i].num >= 0:
    #        ss = ss+str(i)+" "+str(ui.clients[i].num)+" "
    #if ui.mouse_mode:
    #    ss = ss+"True"
    #else:
    #    ss = ss+"False"
    #text = font.render(ss, True, BLACK)
    #ui.screen.blit(text, [x-588, y-40])
       
    sx = 0
    for i in xrange(0, len(ui.clients)):
       if ui.clients[i].hide == False:
          pygame.draw.rect(ui.screen, BLACK, [ui.clients[i].position[0]-5, ui.clients[i].position[1]-5, 85 ,110], 2)     
          ui.screen.blit(ui.clients[i].image, ui.clients[i].position)
          text = font.render(str(i+1), True, BLACK)
          ui.screen.blit(text, [ui.clients[i].position[0]+2, ui.clients[i].position[1]+2])          
    sx = 0
    for i in xrange(0, len(ui.pictures)):
       if ui.pictures[i].hide == False:
          ui.screen.blit(ui.pictures[i].image, ui.pictures[i].position)
          if ui.sub:
             text = font1.render(ui.pictures[i].image_path[:ui.pictures[i].image_path.find(".")], True, WHITE)
             ui.screen.blit(text, [ui.pictures[i].position[0]+2, ui.pictures[i].position[1]+90])
    ui.draw_rect()     
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)

# Be IDLE friendly
pygame.quit()
exit(0)