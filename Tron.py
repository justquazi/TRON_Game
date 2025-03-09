# pygame intialization
import pygame

pygame.init()

# libraries
from random import randint, randrange
import time
from math import sqrt

# screen size
HEIGHT = 900
WIDTH = 1200
rows = 30
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))

# variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
outline = 0
clock = pygame.time.Clock()
# loading images
introImage = pygame.image.load("tron_intro.png")
introImage = pygame.transform.scale(introImage, (WIDTH, HEIGHT))
outroImage = pygame.image.load("tron_gameover.jpeg")
outroImage = pygame.transform.scale(outroImage, (WIDTH, HEIGHT))
backgroundImage = pygame.image.load("tron_background.jpeg")
backgroundImage = pygame.transform.scale(backgroundImage, (WIDTH, HEIGHT))

blueTronImage = pygame.image.load("blue_tron.png")
blueTronImage = pygame.transform.scale(blueTronImage, (20, 20))
greenTronImage = pygame.image.load("green_tron.png")
greenTronImage = pygame.transform.scale(greenTronImage, (20, 20))
powerUpImage = pygame.image.load("red_powerup.png")
powerUpImage = pygame.transform.scale(powerUpImage, (30, 30))

font = pygame.font.SysFont("Verdana", 30)
#music/sound effects
backgroundMusic = pygame.mixer.Sound('tron_background_music.mp3')
backgroundMusic.set_volume(0.5)
chargedSound = pygame.mixer.Sound('chargeup.mp3')
chargedSound.set_volume(0.8)
lobbyMusic = pygame.mixer.Sound('intro_music.mp3')
lobbyMusic.set_volume(0.5)
crashSound = pygame.mixer.Sound('crash.mp3')
crashSound.set_volume(0.5)

# ---------------------------------------#
# tron's properties                #
# ---------------------------------------#
# distance calculation
def distance(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)  # Pythagorean theorem


# tron class
class Tron(object):
    #initialization
    def __init__(self, size, speed, colour, a, b, speedX):
        self.BODY_SIZE = size
        self.HEAD_SIZE = size + 3
        self.SPEED = speed
        self.speedX = speedX
        self.speedY = 0
        self.colour = colour
        self.segX = [int(a)] * 3
        self.segY = [int(b)] * 3
        self.charge = 100

    def __str__(self):
        return '(segments =' + str(len(self.segX)) + ', body size =' + str(self.BODY_SIZE) + ', speed =' + str(
            self.SPEED) + ')'

    # blue tron
    def drawBLUE(self):
        # segment 1 (bike)
        headColour = self.colour
        #gameWindow.blit(blueTronImage, (self.segX[0], self.segY[0]))
        pygame.draw.circle(gameWindow,headColour,(self.segX[0],self.segY[0]),self.HEAD_SIZE,outline)
        # trail segments of the bike
        for i in range(1, len(self.segX)):
            segmentColour = self.colour[2] - 100
            pygame.draw.circle(gameWindow, headColour, (self.segX[i], self.segY[i]), self.BODY_SIZE, outline)

    # green tron
    def drawGREEN(self):
        # segment 1 (bike)
        headColour = self.colour
        #gameWindow.blit(greenTronImage, (self.segX[0], self.segY[0]))
        pygame.draw.circle(gameWindow, headColour, (self.segX[0], self.segY[0]), self.HEAD_SIZE, outline)
        # trail segments of the bike
        for i in range(1, len(self.segX)):
            # segmentColour = self.colour[1] - 100
            pygame.draw.circle(gameWindow, headColour, (self.segX[i], self.segY[i]), self.BODY_SIZE, outline)

    # trons move functions
    def move(self):
        #growing trons trail as it moves
        for i in range(len(self.segX) - 1, 0, -1):
            self.segX[i] = self.segX[i - 1]
            self.segY[i] = self.segY[i - 1]

        self.segX.append(self.segX[1])
        self.segY.append(self.segY[1])
        self.segX[0] = self.segX[0] + self.speedX
        self.segY[0] = self.segY[0] + self.speedY
        self.charge -= 0.5

    #tron's turning/moving functions
    def turnLeft(self):
        if self.speedY != 0:
            self.speedX = -self.SPEED
            self.speedY = 0

    def turnRight(self):
        if self.speedY != 0:
            self.speedX = self.SPEED
            self.speedY = 0

    def turnUp(self):
        if self.speedX != 0:
            self.speedX = 0
            self.speedY = -self.SPEED

    def turnDown(self):
        if self.speedX != 0:
            self.speedX = 0
            self.speedY = self.SPEED

    # trons collision functions
    def wallCollision(self, leftWall, rightWall, floor, ceiling):

        if leftWall.collidepoint(self.segX[0], self.segY[0]):
            print('collision left')
            #crashSound.play()
            return True

        elif rightWall.collidepoint(self.segX[0], self.segY[0]):
            print('collision right')
            #crashSound.play()
            return True

        elif floor.collidepoint(self.segX[0], self.segY[0]):
            print('collision floor')
            #crashSound.play()
            return True

        elif ceiling.collidepoint(self.segX[0], self.segY[0]):
            print('collision ceiling')
            #crashSound.play()
            return True
        return False

    def bikeCollsion(self, other):

        for i in range(len(self.segX)):
            if self.segX[0] == other.segX[i] and self.segY[0] == other.segY[i]:
                print("bike Collisions")
                #crashSound.play()
                return True
        return False
        # pygame.quit()

    def bikeSelfCollsion(self):

        for i in range(4, len(self.segX)):
            if self.segX[0] == self.segX[i] and self.segY[0] == self.segY[i]:
                print("bike Self Collisions")
                #crashSound.play()
                return True
        return False

    #powerup collection function
    def powerUpCollide(self, other, another):
        for i in range(len(other.posX)):
            if distance(other.posX[i], other.posY[i], self.segX[0], self.segY[0]) < 30:
                other.powerUpActive = True
                other.posX[i] = randrange(300, WIDTH - 300, 20)
                other.posY[i] = randrange(300, HEIGHT - 300, 20)
                print(other.posX[i], other.posY[i])
                if other.powerUptype[i] == 0:
                    chargedSound.play()

                    another.charge = 100
                    print("ChargeOther")
                if other.powerUptype[i] == 1:
                    chargedSound.play()

                    self.charge = 100
                    print("ChargeYOurself")

    # charge of tron
    def chargeDepleted(self):
        if self.charge <= 0:
            return True
        return False


# chargers for tron
class PowerUps(object):
    def __init__(self):
        self.posX = []
        self.posY = []
        self.colour = []
        self.powerUptype = []
        self.addPowerUps()
        self.duration = 0
        self.powerUpActive = False

    def draw(self):
        for i in range(4):
            gameWindow.blit(powerUpImage, (self.posX[i], self.posY[i]))
            # pygame.draw.circle(gameWindow, self.colour[i], (self.posX[i],self.posY[i]),20, 0)
        # remove circle when powerup is collected

    def addPowerUps(self):
        for i in range(4):
            self.posX.append(randrange(200, WIDTH - 200, 20))
            self.posY.append(randrange(200, HEIGHT - 200, 20))
            self.colour.append(RED)
            self.powerUptype.append(randint(0, 1))
        print(self.powerUptype)


'''
 def turbo(self,clock,other):
        if self.powerUpActive == True:
            other.SPEED = 20
            self.duration += 1
            print(self.duration)
            if self.duration == 2:
                other.SPEED = 10
                self.duration = 0
                self.powerUpActive = False
'''

'''
    def invincibility(self,clock,other):
        if self.powerUpActive == True:
            # other(tron) collisions disabled
            # change tron colour to gray to display that it is invincible
            self.duration += clock.get_time()
            if self.duration == 500:
            # start duration timer (5s) for invincibility
            # when timer hits 0 re enable collisions
'''

#grid that i thought i was going to use but never did
def drawGrid(w, row, surface):
    gridSize = w // rows
    x = 0
    y = 0
    for i in range(rows):
        x = x + gridSize
        y = y + gridSize
        pygame.draw.line(surface, (WHITE), (x, 0), (x, w))
        pygame.draw.line(surface, (WHITE), (0, y), (w, y))

#redrawing/refreshing the game window
def redrawGameWindow():
    #displaying the charge level of tron on screen
    tron1Text = font.render('Player 1 Charge: ' + str(tron.charge), 1, BLUE)
    tron2Text = font.render('Player 2 Charge: ' + str(tron2.charge), 1, GREEN)
    gameWindow.blit(backgroundImage, (0, 0))
    #boundaries
    pygame.draw.rect(gameWindow, WHITE, (leftWall))
    pygame.draw.rect(gameWindow, WHITE, (rightWall))
    pygame.draw.rect(gameWindow, WHITE, (floor))
    pygame.draw.rect(gameWindow, WHITE, (ceiling))
    # drawGrid(WIDTH,20,gameWindow)
    tron.drawBLUE()
    tron2.drawGREEN()
    powers.draw()
    gameWindow.blit(tron1Text, (WIDTH - 1000, 50))
    gameWindow.blit(tron2Text, (WIDTH - 500, 50))

    pygame.display.update()

#intro screen
def introScreen():
    gameWindow.blit(introImage, (0, 0))
    lobbyMusic.play()
    text = font.render("Player 1: ARROW keys to move BLUE snake", 1, BLUE)
    text2 = font.render("Player 2: WASD keys to move GREEN snake", 1, GREEN)
    text3 = font.render("Click the mouse pad to play!", 1, WHITE)
    instructionText = font.render('If you crash or your power runs out, you lose!',1,WHITE)
    gameWindow.blit(text, (WIDTH // 3 - 130, HEIGHT - 350))
    gameWindow.blit(text2, (WIDTH // 3 - 130, HEIGHT - 300))
    gameWindow.blit(text3, (WIDTH / 3 - 10, HEIGHT - 400))
    gameWindow.blit(instructionText,(WIDTH // 3 - 140, HEIGHT - 250))
    pygame.display.update()

#outro screen
def outroScreen():
    lobbyMusic.play()
    textGameOver1 = font.render('BLUE tron lost power.', 1, WHITE)
    textGameOver2 = font.render('GREEN tron lost power.', 1, WHITE)
    textGameOver3 = font.render('BLUE tron crashed.',1,WHITE)
    textGameOver4 = font.render('GREEN tron crashed.',1,WHITE)
    #textGameOver5 = font.render('BOTH trons lost power at the same time.',1,WHITE)
    textPlayAgain = font.render('Play Again? Press Y or N',1,WHITE)
    gameWindow.blit(outroImage, (0, 0))

    #displaying different texts on outro screen based on what happens in the game
    if tron.chargeDepleted():
        gameWindow.blit(textGameOver1, (WIDTH / 2 - 150, HEIGHT / 2 + 300))

    if tron2.chargeDepleted():
        gameWindow.blit(textGameOver2, (WIDTH / 2 - 150, HEIGHT / 2 + 300))

   # if tron.chargeDepleted() and tron2.chargeDepleted():
       # gameWindow.blit(textGameOver5, (WIDTH / 2 - 150, HEIGHT / 2 + 300))


    if tron.wallCollision(leftWall,rightWall,floor,ceiling) or tron.bikeSelfCollsion() or tron.bikeCollsion(tron2):
        gameWindow.blit(textGameOver3,(WIDTH / 2 - 150, HEIGHT / 2 + 300))

    if tron2.wallCollision(leftWall,rightWall,floor,ceiling) or tron2.bikeSelfCollsion() or tron2.bikeCollsion(tron):
        gameWindow.blit(textGameOver4, (WIDTH / 2 - 150, HEIGHT / 2 + 300))

    gameWindow.blit(textPlayAgain,(WIDTH / 2 - 175, HEIGHT / 2 - 300))
    pygame.display.update()


# Objects for the game
tron = Tron(5, 10, BLUE, WIDTH // 3, HEIGHT // 3, 10)
tron2 = Tron(5, 10, GREEN, WIDTH * 2 // 3, HEIGHT * 2 // 3, -10)

leftWall = pygame.Rect(WIDTH - 1100, HEIGHT - 800, 50, 700)
rightWall = pygame.Rect(WIDTH - 100, HEIGHT - 800, 50, 750)
floor = pygame.Rect(HEIGHT - 800, WIDTH - 400, 1005, 50)
ceiling = pygame.Rect(HEIGHT - 800, WIDTH - 1100, 1005, 50)

powers = PowerUps()
powers.addPowerUps()

# the main program begins here
introPlay = True
gameOn = False
while introPlay:
    #checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            introPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed():
                introPlay = False
                inPlay = True
                gameOn = True

    introScreen()

while gameOn:
    while inPlay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
        #play background music
        lobbyMusic.stop()
        backgroundMusic.play()

        # check for events
        keys = pygame.key.get_pressed()
        hold = pygame.key.get_repeat()

        # act upon key events (tron 1)
        if keys[pygame.K_LEFT]:
            tron.turnLeft()
        if keys[pygame.K_RIGHT]:
            tron.turnRight()
        if keys[pygame.K_UP]:
            tron.turnUp()
        if keys[pygame.K_DOWN]:
            tron.turnDown()

        # tron 2
        if keys[pygame.K_a]:
            tron2.turnLeft()
        if keys[pygame.K_d]:
            tron2.turnRight()
        if keys[pygame.K_w]:
            tron2.turnUp()
        if keys[pygame.K_s]:
            tron2.turnDown()

        # move the bikes
        tron.move()
        tron2.move()
        tron.wallCollision(leftWall, rightWall, floor, ceiling, )
        tron2.wallCollision(leftWall, rightWall, floor, ceiling, )
        tron.bikeCollsion(tron2)
        tron2.bikeCollsion(tron)
        tron.bikeSelfCollsion()
        tron2.bikeSelfCollsion()
        tron.powerUpCollide(powers, tron2)
        tron2.powerUpCollide(powers, tron)

        #ending game if collision is detected
        if tron.bikeCollsion(tron2) or tron2.bikeCollsion(tron):
            inPlay = False

        if tron.wallCollision(leftWall, rightWall, floor, ceiling, ) or tron2.wallCollision(leftWall, rightWall, floor,
                                                                                            ceiling, ):
            inPlay = False

        if tron.bikeSelfCollsion() or tron2.bikeSelfCollsion():
            inPlay = False

        if tron.chargeDepleted() or tron2.chargeDepleted():
            inPlay = False

        # update the screen
        redrawGameWindow()
        pygame.time.delay(60)

    # what happens after game ends
    while inPlay == False and introPlay == False:
        backgroundMusic.stop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_y]:
            inPlay = True
            tron = Tron(5, 10, BLUE, WIDTH // 3, HEIGHT // 3, 10)
            tron2 = Tron(5, 10, GREEN, WIDTH * 2 // 3, HEIGHT * 2 // 3, -10)
            # you need to reset your trons!!!
        if keys[pygame.K_n]:
            gameOn = False
            inPlay = False
            print("game over")
            pygame.quit()
        # YOU need to display these key options on the end screen!!!!!!
        # I displayed them ms G, thank you
        outroScreen()
pygame.quit()



