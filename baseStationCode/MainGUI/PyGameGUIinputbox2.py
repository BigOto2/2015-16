import io
import sys, pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.joystick.init()

# Create array of connected joysticks
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
# https://www.pygame.org/docs/ref/joystick.html

# Define fonts to use in loop
fontobject = pygame.font.Font(None, 18) # Font size 18 in box
fontCoordinateEntry = fontobject.render("Coordinate Entry:", 0, (255,255,255)) # (text, antialias, (r, g, b))

# Define positions of certain GUI elements
CoordBoxPosX, CoordBoxPosY = 125, 500

# Define screen size, set screen
screenSize = (screenWidth, screenHeight) = (1600, 720)
screen = pygame.display.set_mode(screenSize)

# Set fps
clock = pygame.time.Clock()
fps = 60

# Load images
background = pygame.image.load("MarsDesertResearchStation.png")
ball = pygame.image.load("ball.png")

#defines a new class to store coordinates
#this class stores the string representations of GPS coordinates that can be converted to pixels when needed.
#TODO: fix coordinate return methods
#TODO: create mapping function
class Coordinate:
    def __init__(self):
        self.lat = ""
        self.long = ""
    #converts lat to a x position for display
    def xPos(self):
        if self.lat == "":
            return 0
        return int(self.lat)
    #converts long to a y position fo display
    def yPos(self):
        if self.long == "":
            return 0
        return int(self.long)





# Initialize preset variables
textboxEnabled = False
x, y, axisx, axisy = 0, 0, 0, 0
markerList = []

def display_box(screen, message, boxPosX, boxPosY): # Taken from inputbox.py library - display box on screen w/ inputted text

    if len(message) != 0:
        fontDisplayBox = fontobject.render(message, 0, (255,255,255)) # (text, antialias, (r, g, b))
        screen.blit(fontDisplayBox, (boxPosX + 4, boxPosY)) # (font object, (xpos, ypos))

# end

if len(joysticks) >= 1: # Determine if joystick input can be used, if not, run w/o this functionality
    joysticks[0].init()
    joystickson = True
else:
    joystickson = False

# end

while True:

    clock.tick(fps)

    screen.fill((0, 0, 0)) # Black background
    screen.blit(background,(screenWidth - 1280,0)) # Display map on right side of screen, map has size 1280x720

    screen.blit(ball,(x,y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:sys.exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_LEFT) and (textboxEnabled == False):
                textboxEnabled = True
                current_string = []
            #reads in the coordinates
            if textboxEnabled == True:
                if event.type == pygame.KEYDOWN:
                    inkey = event.key
                    if inkey == K_BACKSPACE:
                        current_string = current_string[0:-1]
                    #converts typed coordinates to integers and adds them to the lists of coordinates
                    elif inkey == K_RETURN:
                        textboxEnabled = False
                        commaSeen = False
                        coordRead = ""
                        newCoord = Coordinate()
                        #loops through all characters in the text box
                        for chars in range(len(current_string) + 1):
                            if chars == len(current_string):
                                newCoord.long = coordRead
                            elif current_string[chars] == ",":
                                if not commaSeen:
                                    newCoord.lat = coordRead
                                    commaSeen = True
                                coordRead = ""
                            else:
                                coordRead = coordRead + str(current_string[chars])
                        markerList.append(newCoord)
                    elif inkey == K_MINUS:
                        current_string.append("_")
                    #TODO: allow numberpad inputs.
                    elif (inkey >= 48 and inkey <= 57) or inkey == 44 or inkey == 46: # If key pressed is in the ASCII number range, or is a comma or period...
                        current_string.append(chr(inkey))

    # end event queue loop

    screen.blit(fontCoordinateEntry, (10, 500))

    if textboxEnabled == True:
        display_box(screen, string.join(current_string,""), CoordBoxPosX, CoordBoxPosY)
        pygame.draw.rect(screen, (255, 0, 0), (125, 500, 150, 16), 1) # Draw white box (x, y, xlength, ylength, ?)
    else:
        pygame.draw.rect(screen, (255, 255, 255), (125, 500, 150, 16), 1) # Draw white box (x, y, xlength, ylength, ?)

    for balls in range(len(markerList)):
        screen.blit(ball, (markerList[balls].xPos(), markerList[balls].yPos()))

    if joystickson == True:
        axisx = joysticks[0].get_axis(0)
        axisy = joysticks[0].get_axis(1)

    x += axisx
    y += axisy

    pygame.display.flip()

    pygame.event.pump()

# ---------------- end update loop -------------------------------