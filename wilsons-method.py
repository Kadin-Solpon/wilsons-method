import pygame
import random

pygame.init()

screen = pygame.display.set_mode((750, 500)) # (W,H) 50 boxes in a row, 75 in a column
background = (255,255,255)
screen.fill(background)

running = True

class Box:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.walls = {"top": True, "bottom":True, "left":True, "right": True}
        self.color = (150,150,150)

    #draws the Box onto the screen
    def update_box(self):
        pygame.draw.rect(screen, (255,0,0), (self.xPos, self.yPos, 10, 10)) #draws box

    #draws walls of Box
    def draw_walls(self):
        #builds the top wall
        if self.walls["top"]:
           pygame.draw.rect(screen, (0,0,0), (self.xPos, self.yPos, 10, 2))

        #builds the bottom wall
        if self.walls["bottom"]:
           pygame.draw.rect(screen, (0,0,0), (self.xPos, self.yPos + 10, 10, 2))
        
        #builds the left wall
        if self.walls["left"]:
           pygame.draw.rect(screen, (0,0,0), (self.xPos, self.yPos, 2, 10))

        #builds the right wall
        if self.walls["right"]:
           pygame.draw.rect(screen, (0,0,0), (self.xPos + 10, self.yPos, 2, 10))

    #returns list of start and end coordinates of walls as tuples
    def get_wall_coords(self):
        return [(self.xPos, self.yPos),(self.xPos, self.yPos + 10), (self.xPos, self.yPos), (self.xPos + 10, self.yPos)]


#lists of all boxes and their coords
listOfBoxCoords = []
listOfBoxObj = []

#list of lists of coordinates of walls of boxes
listofWallCoords = []

#adds boxes and their coordinates to lists
for row in range(50):
    for column in range(75):
        listOfBoxObj.append(Box(column * (10 + 2), row * (10 + 2)))
        listOfBoxCoords.append((column * (10 + 2), row * (10 + 2)))


#draws boxes onto screen
for box in listOfBoxObj:
    
    #adds wall coordinates to lists
    #listofWallCoords.append([box.])
    box.walls = {"top": False, "bottom":False, "left":False, "right": True}
    box.update_box()
    box.draw_walls()
    
    
pygame.display.update()
pygame.time.delay(7000)
pygame.quit()