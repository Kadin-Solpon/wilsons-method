import pygame
import random

pygame.init()

cellSize = 10
columns = 75
rows = 50
screenWidth = cellSize * columns
screenHeight = cellSize * rows
screen = pygame.display.set_mode((screenWidth, screenHeight)) # (W,H) 50 boxes in a row, 75 in a column
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
        pygame.draw.rect(screen, self.color, (self.xPos, self.yPos, cellSize, cellSize)) #draws box

    #draws walls of Box
    def draw_walls(self):
        #builds the top wall
        if self.walls["top"]:
           pygame.draw.rect(screen, (0,0,0), (self.xPos, self.yPos, cellSize, 2))

        #builds the bottom wall
        if self.walls["bottom"]:
           pygame.draw.rect(screen, (0,0,0), (self.xPos, self.yPos + cellSize, cellSize, 2))
        
        #builds the left wall
        if self.walls["left"]:
           pygame.draw.rect(screen, (0,0,0), (self.xPos, self.yPos, 2, cellSize))

        #builds the right wall
        if self.walls["right"]:
           pygame.draw.rect(screen, (0,0,0), (self.xPos + cellSize, self.yPos, 2, cellSize))

    #returns list of start and end coordinates of walls as tuples
    def get_wall_coords(self):
        return [(self.xPos, self.yPos),(self.xPos, self.yPos + cellSize), (self.xPos, self.yPos), (self.xPos + cellSize, self.yPos)]


#lists of all boxes and their coords
listOfBoxCoords = []
listOfBoxObj = []

#list of lists of coordinates of walls of boxes
listofWallCoords = []

#adds boxes and their coordinates to lists
for row in range(rows):
    for column in range(columns):
        listOfBoxObj.append(Box(column * cellSize, row * cellSize))
        listOfBoxCoords.append((column * cellSize, row * cellSize))


#draws boxes onto screen
for box in listOfBoxObj:
    
    #adds wall coordinates to lists
    #listofWallCoords.append([box.])
    box.walls = {"top": True, "bottom":True, "left":True, "right": True}
    box.update_box()
    box.draw_walls()
pygame.display.update()

#returns a list of the 4 neighbors of the give box. z is a tuple, coordinate pair
def find_neighbors(z):
    #neighbors of current index
    neighbors = []
    x,y = z

    if x >= cellSize:  
        neighbors.append((x - cellSize, y))
    if x < screenWidth - cellSize:  
        neighbors.append((x + cellSize, y))
    if y >= cellSize:  
        neighbors.append((x, y - cellSize))
    if y < screenHeight - cellSize: 
        neighbors.append((x, y + cellSize))
        
    return [box for box in neighbors if box in listOfBoxCoords]
#tests for find_neighbors()
#print(f"""(50,50) pair{find_neighbors((50,50))}""")
#print(f"""(0,0) pair{find_neighbdors((0,0))}""")
#print(f"""(750,500) pair{find_neighbors((750,500))}""")
#print(f"""(750,0) pair{find_neighbors((750,0))}""")
#print(f"""(0,500) pair{find_neighbors((0,500))}""")



#c is a coordinate, x and y are the x and y coordinates, respectively
def round_down(c):
    x,y = c
    return ((x//10) * 10, (y//10) * 10)

#alters the walls of the current and neighbor box to create the path
def change_neighbors(neighbor, current):

    
    neighborBoxObj = listOfBoxObj[listOfBoxCoords.index(neighbor)]
    currentBoxObj = listOfBoxObj[listOfBoxCoords.index(current)]

    #coressponding coordinate
    neighborBoxObj.color = (0,190,0)
    
    #if neighbor is to the right of current box
    if neighborBoxObj.xPos > currentBoxObj.xPos:
        neighborBoxObj.walls["left"] = False
        currentBoxObj.walls["right"] = False
    #if neighbor is to the left of current box
    if neighborBoxObj.xPos < currentBoxObj.xPos:
        neighborBoxObj.walls["right"] = False
        currentBoxObj.walls["left"] = False

    #if neighbor is below current box
    if neighborBoxObj.yPos > currentBoxObj.yPos:
        neighborBoxObj.walls["top"] = False
        currentBoxObj.walls["bottom"] = False

    #if neighbor is aboveS current box
    if neighborBoxObj.yPos < currentBoxObj.yPos:
        neighborBoxObj.walls["bottom"] = False
        currentBoxObj.walls["top"] = False


    neighborBoxObj.update_box()
    neighborBoxObj.draw_walls()
    currentBoxObj.update_box()
    currentBoxObj.draw_walls()
    pygame.display.update()

def wilsons_method_implementation():

    #path that we will add all coordinates to, it will be cleared once a defined path is created
    tentativePath = [random.choice(listOfBoxCoords)]
    currentBox = listOfBoxObj[listOfBoxCoords.index(tentativePath[0])]
    currentBox.color = (0,190,0)
    currentBox.update_box()
    currentBox.draw_walls()
    pygame.display.update()
    pygame.time.delay(1000)
    #the tentative path will be added to this
    definedPath = []

    #all end coordinates that can be  trying to reach
    allPossibleRandomCoords = [box for box in listOfBoxCoords if box not in tentativePath]

    #selects an end goal and removes it from the list of end points
    end = random.choice(allPossibleRandomCoords)
    allPossibleRandomCoords.pop(allPossibleRandomCoords.index(end))
    
    endBox = listOfBoxObj[listOfBoxCoords.index(end)]
    endBox.color = (255,0,255)
    endBox.update_box()
    endBox.draw_walls()
    
    definedPath.append(end)

    while allPossibleRandomCoords:
        
        #testing definedPath size
        print(f"definedPath Size: {len(definedPath)}")
        print(f"remaining random choices: {len(allPossibleRandomCoords)}")
        #finding next coordinate
        next = random.choice(find_neighbors(tentativePath[-1]))

        #print(f"next: {next}")

        #checks if next is end/in the defined path
        #changing both the current and next boxes so their walls match
        if next in tentativePath:
            # print("found tentative path")
            # print(f"tentative path: {tentativePath}")
            #cutting off loop
            for b in tentativePath[tentativePath.index(next)::]:
                currentBox = listOfBoxObj[listOfBoxCoords.index(b)]
                #resets their walls and color
                currentBox.walls = {"top": True, "bottom":True, "left":True, "right": True}
                currentBox.color = (150,150,150)
                currentBox.update_box()
                currentBox.draw_walls()
            
            #cuts off the loop by starting tentative path at the index of next - 1 (effectively the coordinate before the next block. the first time it was put into the list)
            tentativePath = tentativePath[:tentativePath.index(next) + 1:] #+1

            #used to update just the walls of the last box of non loop section of the tentative path
            
            
            if len(tentativePath) > 1:
                print("here")
                change_neighbors(next, tentativePath[-2])

                #tentativePath[-2]
        
            #next = random.choice(find_neighbors(tentativePath[-1]))
                
        if next in definedPath:
            
            #print("found defined path")
            change_neighbors(next, tentativePath[-1])
            tentativePath.append(next)
            print("step")

            for item in tentativePath:
                currentBox = listOfBoxObj[listOfBoxCoords.index(item)]
                currentBox.color = (155,0,155)
                currentBox.update_box()
                currentBox.draw_walls()

                if item not in definedPath:
                    definedPath.append(item)


            #definedPath.extend([coord for coord in tentativePath if coord not in definedPath])

            
            #removing all the boxes in tentativePath from allPossibleRandomCoords
            #allPossibleRandomCoords = [box for box in allPossibleRandomCoords if box not in definedPath]
            allPossibleRandomCoords = [box for box in allPossibleRandomCoords if box not in definedPath]

            print(f"size of allpossible: {len(allPossibleRandomCoords)}")

            if len(allPossibleRandomCoords) > 0:
                tentativePath = [random.choice(allPossibleRandomCoords)]
                currentBoxObj = listOfBoxObj[listOfBoxCoords.index(tentativePath[0])]
                currentBoxObj.color = (0,190,0)
                currentBoxObj.update_box()
                currentBoxObj.draw_walls()
                pygame.display.update()
            
            continue
            #resets tentative path
            # if len(allPossibleRandomCoords) > 0:
            #     print(f"size of tent: {len(tentativePath)}")
            #     print(tentativePath)
            #     print(f"size of allPossibleRandomCoords: {len(allPossibleRandomCoords)}")
            #     print(allPossibleRandomCoords)
            #     tentativePath = [random.choice(allPossibleRandomCoords)]

                #drawing the first box onto the screen
            

            #next = random.choice([box for box in find_neighbors(tentativePath[-1]) if box not in tentativePath])

            #i think this one is right
            #next = random.choice(allPossibleRandomCoords)
            
            #print(f"defined path size: {len(definedPath)}")

        
        if next not in tentativePath:
            print("here2")
            change_neighbors(next,tentativePath[-1])
            tentativePath.append(next)

    pygame.display.update()
    print(f"defined path: {definedPath}, length of defined path: {len(definedPath)}")

        #pygame.time.delay(10)
        # testing 
        # print(f"tentative path: {tentativePath}")
        # print(f"next {next}, next type: {type(next)}")
        # print(f"next index{tentativePath.index(next)}")
wilsons_method_implementation()




pygame.time.delay(7000)
pygame.quit()