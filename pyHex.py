from pygame import *
from pygame import gfxdraw
from math import *
from random import *
import os,fixList


class Game:
    def __init__(self):
        self.width = 960
        self.height = 540
        self.size = self.width,self.height

        self.mode = 'menu'

        self.score = 0

        self.icon = Surface((32,32))
        self.iconFont = font.Font('font/p8.ttf',36)
        self.iconPic = self.iconFont.render('H',True,(255,255,255))
        self.icon.blit(self.iconPic, (8,0))

        self.clock = time.Clock()

        self.boom1 = mixer.Sound('sound/boom1.wav')
        self.boom2 = mixer.Sound('sound/boom2.wav')

        self.winFont = font.Font('font/p8.ttf',260)
        self.winTxt = self.winFont.render('WIN!',True,(240,240,240))

        time.set_timer(USEREVENT+1,100)
        self.seconds = 0

    def eventLoop(self):
        global running,keyDown
        keyDown = False
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN:
                keyDown = True
            if e.type == USEREVENT + 1:
                if game.mode == 'play':
                    self.seconds += 0.1

        mixer.music.queue('sound/techno.ogg')

    def checkInput(self,inputType):
        '''inputType can be mx or my or mb'''
        inputs ={ 'mx': mouse.get_pos()[0], 
                  'my': mouse.get_pos()[1], 
                  'mb': mouse.get_pressed(),
                  'keys': key.get_pressed() } 
        return inputs[inputType]

    def distance(self,tuple1,tuple2):
        return ((tuple2[0]-tuple1[0])**2 + (tuple2[1]-tuple1[1])**2)**0.5

    def draw(self):
        screen.fill((45,45,70))
        
        if self.mode == 'menu': 
            environment.drawStars()
            play.draw()
            player.draw()
            environment.draw()
            menu.draw()

            self.clock.tick(50)

        if self.mode == 'play':  #whats drawn to the screen during gameplay
            environment.drawStars()
            play.draw()
            player.draw()
            environment.draw()

            player.bulletFunctions()


            self.clock.tick(50)

        if self.mode == 'win':
            environment.drawStars()
            play.draw()
            player.draw()
            environment.draw()

            screen.blit(self.winTxt,(960//2 - self.winTxt.get_width()//2, 540//2 - self.winTxt.get_height()//2-100))
            winTime = menu.titleFont.render(str(round(game.seconds,2)),True,(240,240,240))
            screen.blit(winTime,(960//2 - winTime.get_width()//2, 540//2 - winTime.get_height()//2+200))
            
        display.flip()

    def scoreUpdate(self):
        scoreFile = open('highscores.txt','r')
        scores = scoreFile.read().split('\n')
        scores.append(str(round(game.seconds,2))+' '+os.getlogin())
        scoreFile = open('highscores.txt','w')
        for i in scores:
            scoreFile.write(i+'\n')
        


class Menu:
    '''Class pertaining to menu, its drawing, and its functions'''
    def __init__(self):
        ## Title on Menu Screen
        self.titleFont = font.Font('font/p8.ttf',96)
        self.titlePic = self.titleFont.render('pyHex',True,(240,240,240))
        ## text 'pyHex' that appears largely on the menu screen
        self.titlePicWidth = self.titlePic.get_width()
        self.titlePicHeight = self.titlePic.get_height()

        self.pc = 100 #play colour
        self.pcMod = 2 #to cause a fade-in fade-out

        self.playFont = font.Font('font/sb.ttf',16)
        ## the 'Sansation' font by Bernd Montag
        self.playText = self.playFont.render('play',True,(self.pc,self.pc,self.pc))
        self.centeredPlayW = game.width//2 - self.playText.get_width()//2
        self.centeredPlayH = game.height//2 - self.playText.get_height()//2

        self.frame = 0

        for i in range(24):  #the game starts off with 24 active asteroids already on screen
            play.asteroidList.append(Asteroid(randint(0,960),randint(0,540),  #menu -> game transition is seamless
                                              choice(play.asteroidPool[randint(0,9)])))


    def playButton(self):
        if game.mode == 'menu':
            if game.checkInput('mb')[0]:
                game.mode = 'play'
                game.seconds = 0

            self.playText = self.playFont.render('play',True,(self.pc,self.pc,self.pc))
            if self.pc >= 230: #once RGB hits 230,230,230, resets back to 100,100,100
                self.pc = 100
            self.pc += self.pcMod  #adds to the RGB value to cause a fade effect                 
                
    def draw(self):
        screen.blit(self.titlePic,(15,440)) #function draws the title in the bottom left corner, and the play text in the center
        screen.blit(self.playText,(self.centeredPlayW,self.centeredPlayH))  #this function only called when game.mode == 'menu'
        for a in play.asteroidList:
            a.move()


class Play:
    '''Class pertaining to the gameplay'''
    def __init__(self):
        self.hexagonPoints = [(456,229), (503,229), ## top 2 points #(Y formerly 229)
                              (526,270), (503,310), ## middle/bottom right points (Y formerly 310)
                              (456,310), (433,270)] ## bottom/middle left points

        self.asteroidList = []  #this is a list of all active asteroid objects
        self.asteroidGenFrame = 0  #this allows asteroid generation at a given rate
        self.largeAsteroids = [  #3 different types of large polygons
            [(18, 85), (46, 82), (74, 88), (88, 73), (81, 46), (88, 25), (64, 11), (22, 19), (11, 34), (19, 54), (12, 72)],
            [(11, 25), (17, 42), (12, 71), (27, 75), (37, 89), (74, 84), (88, 57), (83, 35), (88, 19), (66, 11), (46, 16), (34, 11)],
            [(62, 11), (48, 24), (22, 13), (12, 36), (29, 59), (16, 84), (44, 88), (85, 73), (71, 36), (86, 25)],
            ]
        self.medAsteroids = [  #3 different types of medium polygons
            [(43, 31), (31, 35), (38, 45), (31, 50), (31, 63), (41, 69), (62, 66), (68, 61), (63, 56), (69, 49), (66, 33)],
            [(59, 31), (68, 42), (57, 50), (65, 65), (43, 63), (34, 67), (32, 53), (37, 44), (34, 33)],
            [(52, 68), (68, 60), (58, 50), (68, 37), (56, 32), (33, 36), (40, 47), (37, 65)]
            ]
        self.smallAsteroids = [  #3 different types of small polygons
            [(42, 42), (45, 49), (42, 53), (50, 59), (58, 54), (58, 45), (51, 41)],
            [(44, 58), (51, 54), (58, 57), (60, 49), (54, 40), (42, 44), (46, 50)],    #all are point lists
            [(42, 41), (45, 48), (42, 55), (56, 58), (59, 56), (57, 47), (59, 41), (50, 43)]
            ]
        self.asteroidPool = [self.largeAsteroids,self.largeAsteroids,self.largeAsteroids,self.largeAsteroids,self.largeAsteroids,self.largeAsteroids,self.largeAsteroids,self.largeAsteroids,self.largeAsteroids, #medium asteroids most common, then large, then small (small are annoying and less fun)
                          self.medAsteroids,self.medAsteroids,self.medAsteroids,self.medAsteroids,self.medAsteroids,
                          self.smallAsteroids,self.smallAsteroids] #added more or less for probability reasons
        

        self.timeFont = font.SysFont('Courier New',12)
    def play(self):
        '''Function to call gameplay functions only when game.mode == 'play'.'''
        if game.mode == 'play':
            player.move()   #these functions are called only during gameplay
            player.shoot()  #the player can only move or shoot during gameplay
            for a in play.asteroidList:
                a.hexCollide()   #hexagon collisions are non-existent in the menu, they simply "pass over"
                a.move() #moves the asteroids
            player.checkWin()

    def timeTxt(self):
        return self.timeFont.render(str(round(game.seconds,2)),True,(240,240,240))    
              
    def draw(self):
        #Draws the centre hexagon
        gfxdraw.filled_polygon(screen,self.hexagonPoints,(15,75,0))
        gfxdraw.aapolygon(screen,self.hexagonPoints,(25,220,0))

        #environment.explosionSurface = Surface((960,540),SRCALPHA) #re declare the explosion surface for clearing (do to per-pixel alpha)
        environment.explosionSurface.fill((0,0,0,0))
        for e in environment.explosionList:
            e.draw() #draws explosions
            e.manage() #makes explosions cool
        for a in self.asteroidList:
            a.draw()

        screen.blit(self.timeTxt(),(2,2))

class Asteroid:
    '''Class pertaining to an asteroid'''
    def __init__(self,x,y,polygon):
        self.x = x
        self.y = y
        self.points = fixList.fix2(polygon,x,y)
        self.sx = choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6]) #speed x is random between -6 and 6
        self.sy = choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6]) #speed y is random between -6 and 6

        play.asteroidList.append(self)
        self.frame = 0

        if polygon in play.smallAsteroids: self.radius = 7
        elif polygon in play.medAsteroids: self.radius = 15
        elif polygon in play.largeAsteroids: self.radius = 35

    def move(self):
        if self.frame == 3: #asteroids only move every 3 ticks
            self.frame = 0

            if self.points[0][0] < -60 or self.points[0][0] > 1020:
                self.sx *= -1 #if asteroid leaves x boundry, it changes direction
            if self.points[0][1] < -60 or self.points[0][1] > 620:
                self.sy *= -1 #if asteroid leaves y boundry, it changes direction
            self.points = fixList.fix2(self.points,self.sx,self.sy)

            self.x = 0
            self.y = 0
            for i in self.points:
                self.x += i[0]
                self.y += i[1]
            self.x = self.x // len(self.points)
            self.y = self.y // len(self.points)

        else:
            self.frame += 1

    def explode(self):
        explosionColours = [(255,175,0),(255,150,0),(255,125,0),(255,100,0),
                            (210,80,0),(255,70,33),(255,75,75)]
        for i in range(10):
            colour = choice(explosionColours)
            posx,posy = self.x+randint(0,self.radius),self.y+randint(0,self.radius)
            radius = randint(3,8)

            environment.explosionList.append(Explosion(posx,posy,radius,colour))

    def hexCollide(self):
        for p in self.points:
            if game.distance((480,270),(p)) < 40.8: #40.8 - apothem of hexagon
                self.explode()
                game.boom1.play()
                try:
                    play.asteroidList.remove(self)
                except: continue
                game.mode = 'menu'
                player.bullets = []
                for i in range(24-len(play.asteroidList)):  #the game starts off with 12 active asteroids already on screen
                    play.asteroidList.append(Asteroid(randint(0,960),randint(0,540),  #menu -> game transition is seamless
                                              choice(play.asteroidPool[randint(0,9)])))
             
    def draw(self):
        gfxdraw.filled_polygon(screen,self.points,(18,18,18))
        gfxdraw.aapolygon(screen,self.points,(240,240,240))        


class Explosion:
    '''Class pertaining to individual explosions(each circle)'''
    def __init__(self,x,y,r,col):
        self.x = x
        self.y = y
        self.r = r
        self.col = col
        self.frame = 0

    def manage(self):
        if self.frame == 25:
            environment.explosionList.remove(self)
        else:
            self.frame += 1

        if self.frame %2 == 0:
            self.x += randint(-3,3)
            self.y += randint(-3,3)

    def draw(self):
        gfxdraw.aacircle(environment.explosionSurface,
                    self.x,self.y,
                    self.r,self.col)
        gfxdraw.filled_circle(environment.explosionSurface,
                    self.x,self.y,
                    self.r,self.col)


class Environment:
    '''Class pertaining to environment details mainly in gameplay'''
    ## Things that do NOT affect gameplay
    def __init__(self):
        self.patternOverlay = Surface((960,540))
        for i in range(1,541,4):
            gfxdraw.hline(self.patternOverlay,
                          0,960,i,
                          (255,255,255))
            gfxdraw.hline(self.patternOverlay, ## draws to hlines of white
                          0,960,i+1,
                          (255,255,255))
            gfxdraw.hline(self.patternOverlay, ## and two hlines of black
                          0,960,i+2,
                          (0,0,0))
            gfxdraw.hline(self.patternOverlay, ## throughout the whole screen
                          0,960,i+3,
                          (0,0,0))
        self.patternOverlay.set_alpha(5)
        ## ^^ All pertains to the pattern overlayed on the whole game

        ## Stars
        self.stars = []  # holds all the star positions on the screen
        self.starFrame = 0  #starFrame for use with blinking or w/e
        self.starExt = 0 # the extension on the star (blinking)
        for i in range(10):
            self.makeStar() #generates 10 stars

        self.staticSurf = Surface((960,540)) ## Static Overlay Surface
        self.staticLayers = []
        self.staticFrame = 0

        self.explosionSurface = Surface((960,540),SRCALPHA)
        self.explosionList = []
        
    def makeStar(self):
        starPos = randint(0,960),randint(0,540)
        self.stars.append(starPos)

    def drawStars(self):
        for s in self.stars:
            gfxdraw.vline(screen,s[0],
                          s[1] - 2 - self.starExt,
                          s[1] + 2 + self.starExt,
                          (220,220,220))
            gfxdraw.hline(screen,
                          s[0] - 2 - self.starExt,
                          s[0] + 2 + self.starExt,
                          s[1], (220,220,220))
            gfxdraw.filled_circle(screen,s[0],s[1],1+self.starExt,(255,255,255))
            

        self.starFrame += 1
        if self.starFrame > 10:
            self.starFrame = 0

        if self.starFrame > 5:
            self.starExt = 1
        else: self.starExt = 0
            
    def genStatic(self):
        for i in range(5):
            for x in range(960):
                for y in range(540):
                    self.staticSurf.set_at((x,y),choice([(0,0,0),(255,255,255)]))
            self.staticLayers.append(self.staticSurf.copy())

    def drawStatic(self):
        self.staticSurf.set_alpha(5)
        self.staticSurf.blit(self.staticLayers[self.staticFrame],(0,0))
        self.staticFrame += 1
        if self.staticFrame == 5: self.staticFrame = 0
        screen.blit(self.staticSurf,(0,0))
        
    def draw(self):
        screen.blit(self.explosionSurface,(0,0))
        screen.blit(self.patternOverlay,(0,0))
        #self.drawStars()
        self.drawStatic()

        
class Player:
    '''Class pertaining to the player attributes and controls'''
    def __init__(self):
        self.angle = 90
        ## the angle where the trigon lies on the circle

        ## starts at 90 (top)

        self.x = self.xChange(0,62)
        self.y = self.yChange(0,62)
        ## the coordinates of the trigon's point

        self.trigonPointLeftX = self.xChange(7,52)
        self.trigonPointLeftY = self.yChange(7,52)
        ## the coordinates of the trigon's lower left point
        ## the angle is modified to make the trigon wider
        ## the hypotenuse is different from the point to add height

        self.trigonPointRightX = self.xChange((-7),52)
        self.trigonPointRightY = self.yChange((-7),52)
        ## the coordinates of the trigons lower left point
        ## the angle is modified to make the trigon wider
        ## the hypotenuse is different from the point to add height

        self.bullets = []
        ## list of Bullet() objects will be contained here, as they are
        ## player bullets
        
    def xChange(self,angleMod,hypotenuse):
        '''Function uses similar triangles to change x-coord of trigon'''
        return int(game.width//2 + cos(radians(self.angle + angleMod)) * hypotenuse)
        ## width//2 accomplishes center of screen
        ## cosine of the angle (in radians) multiplied by a hypotenuse

    def yChange(self,angleMod,hypotenuse):
        '''Function uses similar triangles to change y-coord of trigon'''
        return int(game.height//2 - sin(radians(self.angle + angleMod)) * hypotenuse)
        ## height//2 accomplishes center of screen
        ## sin of the angle (in radians) multiplied by the hypotenuse

    def move(self):
        '''Checks for input, moves trigon accordingly'''
        if game.checkInput('keys')[K_RIGHT]:
            ## calls for the keys list and checks for the right arrow
            self.angle -= 6 ## angle decreases to move trigon clockwise
        elif game.checkInput('keys')[K_LEFT]:
            ## calls for the keys list and checks for the left arrow
            self.angle += 6 ## angle increases to move trigon clockwise

        self.x = self.xChange(0,62) ## update player-x, function uses new player-angle
        self.y = self.yChange(0,62) ## updates player-y, function uses new player-angle

        self.trigonPointLeftX = self.xChange(7,52) ## ^
        self.trigonPointLeftY = self.yChange(7,52) ## ^

        self.trigonPointRightX = self.xChange((-7),52) ## ^
        self.trigonPointRightY = self.yChange((-7),52) ## ^

    def draw(self):
        gfxdraw.filled_trigon(screen,
                         self.trigonPointLeftX,self.trigonPointLeftY,
                         self.trigonPointRightX,self.trigonPointRightY,
                         self.x,self.y,
                         (0,0,0))
        gfxdraw.aatrigon(screen,
                         self.trigonPointLeftX,self.trigonPointLeftY,
                         self.trigonPointRightX,self.trigonPointRightY,
                         self.x,self.y,
                         (240,240,240))#clean this line
        
    def shoot(self):
        if keyDown and game.checkInput('keys')[K_SPACE]:
            self.bullets.append(Bullet(self.x,self.y,self.angle))

    def bulletFunctions(self):
        for b in player.bullets:
            b.move()
            b.checkBoundry()
            b.collideCheck()
            b.draw()

    def checkWin(self):
        if len(play.asteroidList) == 0:
            game.mode = 'win'
            game.scoreUpdate()
            mixer.music.load('sound/win.mp3')
            mixer.music.play()


class Bullet:
    '''Class for bullets.  Each bullet will be its own object.'''
    def __init__(self,x,y,angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.frame = 0

    def xChange(self,angleMod,hypotenuse):
        '''Function uses similar triangles to change x-coord of trigon'''
        return int(game.width//2 + cos(radians(self.angle + angleMod)) * hypotenuse)
        ## width//2 accomplishes center of screen
        ## cosine of the angle (in radians) multiplied by a hypotenuse

    def yChange(self,angleMod,hypotenuse):
        '''Function uses similar triangles to change y-coord of trigon'''
        return int(game.height//2 - sin(radians(self.angle + angleMod)) * hypotenuse)
        ## height//2 accomplishes center of screen
        ## sin of the angle (in radians) multiplied by the hypotenuse

    def move(self):
        '''Calls the x&yChange methods to move bullets along the hypotenuse.'''
        self.x = self.xChange(0,62+self.frame*4) #moves the bullet along the hypotenuse
        self.y = self.yChange(0,62+self.frame*4)# ^^
        self.frame += 1

    def checkBoundry(self): #removes bullets once off-screen
        if self.x > game.width or self.x < 0 or self.y > game.height or self.y < 0:
            try:
                player.bullets.remove(self)  #if bullet leaves x boundry, it gets deleted
            except: return True

    def collideCheck(self):
        '''Checks for bullet collisions with asteroids'''
        for a in play.asteroidList:
            if game.distance((a.x,a.y),(self.x,self.y)) <= a.radius:
                play.asteroidList.remove(a)
                try:
                    player.bullets.remove(self)
                except: continue
                a.explode()
                game.boom2.play()

    def draw(self):
        gfxdraw.filled_circle(screen,int(self.x),int(self.y),2,(0,0,0))
        gfxdraw.aacircle(screen,int(self.x),int(self.y),2,(240,240,240))

        
    
def main():
    global running,game,menu,play,player,screen,environment
    init()  #initializes the Pygame Module
    running = True

    game = Game()  #concerns the game functions (drawing, event loop, etc.)
    play = Play() #concerns the gameplay
    menu = Menu() #concerns the main menu and its functions (play, effects, etc.)
    player = Player() #the player trigon
    environment = Environment()
    environment.genStatic()

    

    display.set_icon(game.icon)
    screen = display.set_mode(game.size) #(960,540)
    display.set_caption('pyHex')

    mixer.music.load('sound/techno.ogg')
    mixer.music.play()
    
    while running:
        game.eventLoop()

        play.play()
        play.draw()
        menu.playButton()

        game.draw()
    quit()

main()
