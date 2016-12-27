import pygame, sys
from pygame.locals import *

WINDOWWIDTH = 1000
WINDOWHEIGHT = 800
FPS = 30

#                  R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)
SILVER =        (192, 192, 192)
RED =           (255,   0,   0)
YELLOW =        (255, 255,   0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BASICFONTSIZE = 20

ROOMWIDTH = 720 
ROOMHEIGHT = 370
ROOMX = 100
ROOMY = 150

INVENTWIDTH = 700
INVENTHEIGHT = 120
INVENTX = 105
INVENTY = 550
INVENTTILE = 100
CAPACITY = 6
INVENTCOLOR = BRIGHTBLUE
LETTERSCOLOR = SILVER

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

class Room:
  def __init__(self, h, p, u, d, l, r, img):
        self.home = h
        self.place = p

        self.up = u
        self.down = d
        self.left = l
        self.right = r

        self.image = img
        self.items = []
        
  # def shift(self, )
      
  def draw(self):
     pygame.draw.rect(DISPLAYSURF, self.image, ( ROOMX, ROOMY, ROOMWIDTH, ROOMHEIGHT))
     for i in self.items:
       i.draw()

class Item:
  def __init__(self, x, y, h, w, p, st, t, img):
    self.x = x
    self.y = y
    self.height = h
    self.width = w

    self.pair = p
    self.static = st
    self.text = t
    self.image = img

  def draw(self):
     pygame.draw.rect(DISPLAYSURF, self.image, ( self.x, self.y, self.width, self.height))

def main():
  global FPSCLOCK, DISPLAYSURF, BASICFONT, SHFT, CURRENT , ROOMS ,INVENTORY, LETTERS, DIARY, NEW, INVENTSURF, INVENTRECT, msg, match, show
  pygame.init()
  FPSCLOCK = pygame.time.Clock()
  DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
  pygame.display.set_caption('Game')
  BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
  ROOMS = []
  INVENTORY = []
  LETTERS = []
  DIARY = []
  NEW = []
  stuffInit()
  msg = 'Welcome!'
  roomsInit()
  CURRENT = 0
  SHFT = True
  drawInvent()
  match = None
  show = None
  
  while True: # main game loop
    checkForQuit()
    for event in pygame.event.get(): # event handling loop
      if show == None:
        msg = '' 
        if event.type == MOUSEBUTTONUP:
          if not getSpotClicked(event.pos[0], event.pos[1]):
            match = None
            if INVENTRECT.collidepoint(event.pos):
              SHFT = not SHFT
        elif event.type == KEYUP: # check if the user pressed a key to slide a tile
          if event.key in (K_LEFT, K_a):
            if not changeDir(LEFT):
              msg = 'No way'
          elif event.key in (K_RIGHT, K_d):
            if not changeDir(RIGHT):
              msg = 'No way'
          elif event.key in (K_UP, K_w):
            if not changeDir(UP):
              msg = 'No way'
          elif event.key in (K_DOWN, K_s):
            if not changeDir(DOWN):
              msg = 'No way'
      else:
        show = None
    drawGame()
    if show!= None:
      showDiary()
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def terminate():
  pygame.quit()
  sys.exit()

def checkForQuit():
  for event in pygame.event.get(QUIT): # get all the QUIT events
    terminate() # terminate if any QUIT events are present
  for event in pygame.event.get(KEYUP): # get all the KEYUP events
    if event.key == K_ESCAPE:
      terminate() # terminate if the KEYUP event was for the Esc key
    pygame.event.post(event) # put the other KEYUP event objects back

def roomsInit():
  room1 = Room (0, 0, 1, None, None, 2, GREEN)
  item1 = Item(400, 400, 50, 50, 4, True, 'place', RED)
  room1.items.append(item1)
  ROOMS.append(room1)
  room2 = Room (1, 3, None, 0 , None, None, WHITE)
  item2 = Item( 500, 400, 40, 40, 2, False, 'golden key', YELLOW)
  room2.items.append(item2)
  item3 = Item(200, 400, 60, 30, 4, False, 'key', RED )
  room2.items.append(item3)
  ROOMS.append(room2)
  room3 = Room (2, 1, None, None, 0, None, BLACK)
  ROOMS.append(room3)

def stuffInit():
  DIARY.append('0')
  DIARY.append('1')
  DIARY.append('2')
  DIARY.append('3')
  DIARY.append('Story')
  DIARY.append('5')
  LETTERS.append('')
  LETTERS.append('')
  LETTERS.append('')
  LETTERS.append('')
  LETTERS.append('')
  LETTERS.append('')
  item4 = Item(400, 400, 50, 50, 4, True, 'peaceful place', SILVER)
  NEW.append('')
  NEW.append('')
  NEW.append('')
  NEW.append('')
  NEW.append(item4)
  NEW.append('')

def showDiary():
  global show
  pygame.draw.rect(DISPLAYSURF, WHITE, ( 250, 200, 300, 320))
  textSurf, textRect = makeText(LETTERS[show], BLACK, WHITE, 300, 300)
  DISPLAYSURF.blit(textSurf, textRect) 

def changeDir(direction):
  global CURRENT
  if direction == UP:
    if ROOMS[CURRENT].up == None:
      return False
    else:
      CURRENT = ROOMS[CURRENT].up
  if direction == DOWN:
    if ROOMS[CURRENT].down == None:
      return False
    else:
      CURRENT = ROOMS[CURRENT].down
  if direction == LEFT:
    if ROOMS[CURRENT].left == None:
      return False
    else:
      CURRENT = ROOMS[CURRENT].left
  if direction == RIGHT:
    if ROOMS[CURRENT].right == None:
      return False
    else:
      CURRENT = ROOMS[CURRENT].right
  return True

def getSpotClicked(x, y):
  global msg, match, show
  j = 0
  if ROOMX<x<ROOMX+ROOMWIDTH and ROOMY<y<ROOMY+ROOMHEIGHT:
    for i in ROOMS[CURRENT].items:
      if i.x<x<i.x+i.width and i.y<y<i.y+i.height:
        if i.static==False:
          INVENTORY.append(ROOMS[CURRENT].items.pop(j))
          return True
        else:
          if match!=None and INVENTORY[match].pair == i.pair:
            LETTERS.pop(i.pair)
            LETTERS.insert(i.pair, DIARY[i.pair])
            ROOMS[CURRENT].items.pop(j)
            ROOMS[CURRENT].items.insert(j,NEW[INVENTORY[match].pair])
            INVENTORY.pop(match)
            match = None
            return True
          else:
            msg = i.text
      j = j+1
  elif INVENTX<x<INVENTX+INVENTWIDTH and INVENTY<y<INVENTY+INVENTHEIGHT:
    while j<CAPACITY:
      if INVENTX+15*(j+1)+j*INVENTTILE<x<INVENTX+(15+INVENTTILE)*(j+1) and INVENTY+10<y<INVENTTILE+INVENTY+10:
        if SHFT and len(INVENTORY)>j:
          msg = INVENTORY[j].text
          match = j
          return True
        elif not SHFT and LETTERS[j]!='':
          match = None
          show = j
          return True
        else:
          msg = 'Empty here'
      j = j+1
  return False

def makeText(text, color, bgcolor, top, left):
# create the Surface and Rect objects for some text.
  textSurf = BASICFONT.render(text, True, color, bgcolor)
  textRect = textSurf.get_rect()
  textRect.topleft = (top, left)
  return (textSurf, textRect)

def drawInvent():
  global INVENTRECT, match
  i = 0
  if SHFT:
    buttontext = 'to LETTERS'
    pygame.draw.rect(DISPLAYSURF, INVENTCOLOR, ( INVENTX, INVENTY, INVENTWIDTH, INVENTHEIGHT))
    for it in INVENTORY:
      if i == match:
        pygame.draw.rect(DISPLAYSURF, WHITE, ( INVENTX+15*(i+1)+i*INVENTTILE-5, INVENTY+10-5, INVENTTILE+10, INVENTTILE+10))  
      pygame.draw.rect(DISPLAYSURF, it.image, ( INVENTX+15*(i+1)+i*INVENTTILE, INVENTY+10, INVENTTILE, INVENTTILE))
      i = i+1
    while i < CAPACITY:
      pygame.draw.rect(DISPLAYSURF, BLACK, ( INVENTX+15*(i+1)+i*INVENTTILE, INVENTY+10, INVENTTILE, INVENTTILE))
      i = i+1
  else:
    buttontext = 'to INVENTORY'
    pygame.draw.rect(DISPLAYSURF, LETTERSCOLOR, ( INVENTX, INVENTY, INVENTWIDTH, INVENTHEIGHT))
    while i < CAPACITY:
      for it in LETTERS:
        if it=='':
          pygame.draw.rect(DISPLAYSURF, BLACK, ( INVENTX+15*(i+1)+i*INVENTTILE, INVENTY+10, INVENTTILE, INVENTTILE))
          i = i+1    
        else:
          pygame.draw.rect(DISPLAYSURF, WHITE, ( INVENTX+15*(i+1)+i*INVENTTILE, INVENTY+10, INVENTTILE, INVENTTILE))
          i = i+1
  INVENTSURF, INVENTRECT = makeText(buttontext, TEXTCOLOR, TILECOLOR, INVENTX+INVENTWIDTH+50, INVENTY+40)
  DISPLAYSURF.blit(INVENTSURF, INVENTRECT)  
    
def drawGame():
  DISPLAYSURF.fill(BGCOLOR)
  ROOMS[CURRENT].draw()
  drawInvent()
  if msg:
    textSurf, textRect = makeText(msg, TEXTCOLOR, BGCOLOR, 5, 5)
    DISPLAYSURF.blit(textSurf, textRect)
  
if __name__ == '__main__':
  main()
