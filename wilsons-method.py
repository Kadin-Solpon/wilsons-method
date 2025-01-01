import pygame
import random

pygame.init()

cellSize = 25
columns = 50
rows = 30
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
def find_wilson_neighbors(z):
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

#the tentative path will be added to this
definedPath = []

def wilsons_method_implementation():

    #path that we will add all coordinates to, it will be cleared once a defined path is created
    tentativePath = [random.choice(listOfBoxCoords)]
    currentBox = listOfBoxObj[listOfBoxCoords.index(tentativePath[0])]
    currentBox.color = (0,190,0)
    currentBox.update_box()
    currentBox.draw_walls()
    pygame.display.update()
    
    
    #all end coordinates that can be  trying to reach
    allPossibleRandomCoords = [box for box in listOfBoxCoords if box not in tentativePath]

    #selects an end goal and removes it from the list of end points
    end = random.choice(allPossibleRandomCoords)
    allPossibleRandomCoords.pop(allPossibleRandomCoords.index(end))
    
    endBox = listOfBoxObj[listOfBoxCoords.index(end)]
    endBox.color = (255,255,255)
    endBox.update_box()
    endBox.draw_walls()
    
    definedPath.append(end)

    while allPossibleRandomCoords:
        #testing definedPath size
        print(f"definedPath Size: {len(definedPath)}")
        print(f"remaining random choices: {len(allPossibleRandomCoords)}")
        #finding next coordinate
        next = random.choice(find_wilson_neighbors(tentativePath[-1]))

       
        #changing both the current and next boxes so their walls match
        if next in tentativePath:
          
            #cutting off loop
            for b in tentativePath[tentativePath.index(next)::]:
                currentBox = listOfBoxObj[listOfBoxCoords.index(b)]
                #resets their walls and color
                currentBox.walls = {"top": True, "bottom":True, "left":True, "right": True}
                if b != tentativePath[0]:
                    currentBox.color = (150,150,150)
                currentBox.update_box()
                currentBox.draw_walls()
            
            #cuts off the loop by starting tentative path at the index of next - 1 (effectively the coordinate before the next block. the first time it was put into the list)
            tentativePath = tentativePath[:tentativePath.index(next) + 1:] #+1
            
            
            if len(tentativePath) > 1:
                print("here")
                change_neighbors(next, tentativePath[-2])

                
        if next in definedPath:
            
            #print("found defined path")
            change_neighbors(next, tentativePath[-1])
            tentativePath.append(next)
            print("step")

            for item in tentativePath:
                currentBox = listOfBoxObj[listOfBoxCoords.index(item)]
                currentBox.color = (255,255,255)
                currentBox.update_box()
                currentBox.draw_walls()

                if item not in definedPath:
                    definedPath.append(item)
            
            #removing all the boxes in tentativePath from allPossibleRandomCoords
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

        
        if next not in tentativePath:
            print("here2")
            change_neighbors(next,tentativePath[-1])
            tentativePath.append(next)

    pygame.display.update()
    print(f"defined path: {definedPath}, length of defined path: {len(definedPath)}")

wilsons_method_implementation()


#takes in one coordinates. returns list of valid neighboring box coords
def find_dfs_neighbors(z):
    allNeighbors = []
    x,y = z
    zBox = listOfBoxObj[listOfBoxCoords.index(z)]

    #checks if there is a valid left neighbor
    if x > 0:
        neighbor1 = listOfBoxObj[listOfBoxCoords.index((x - cellSize, y))]
        if neighbor1.walls["right"] == False and zBox.walls["left"] == False:
            allNeighbors.append((x - cellSize, y))

    #checks if there is a valid right neighbor
    if x < (columns - 1) * cellSize:
        neighbor2 = listOfBoxObj[listOfBoxCoords.index((x + cellSize, y))]
        if neighbor2.walls["left"] == False and zBox.walls["right"] == False:
            allNeighbors.append((x + cellSize, y))

    #checks if there is a valid top neighbor
    if y > 0:
        neighbor3 = listOfBoxObj[listOfBoxCoords.index((x, y - cellSize))]
        if neighbor3.walls["bottom"] == False and zBox.walls["top"] == False:
            allNeighbors.append((x, y - cellSize))

    #checks if there is a valid bottom neighbor
    if y < (rows - 1) * cellSize:
        neighbor4 = listOfBoxObj[listOfBoxCoords.index((x, y + cellSize))]
        if neighbor4.walls["top"] == False and zBox.walls["bottom"] == False:
            allNeighbors.append((x, y + cellSize))
    
    return allNeighbors
    
def depth_first_search():

    #sets starting coords to top left box and end coords to bottom right box
    start = (0,0)
    end = ((columns - 1)  * cellSize, (rows - 1) * cellSize)

    #changes both the start and end box colors to purple
    currentBlock = listOfBoxObj[listOfBoxCoords.index(start)]
    endBlock = listOfBoxObj[listOfBoxCoords.index(end)]

    currentBlock.color = (200,0,200)
    endBlock.color = (200,0,200)

    currentBlock.update_box()
    endBlock.update_box()

    currentBlock.draw_walls()
    endBlock.draw_walls()

    pygame.display.update()

    #sets the two lists
    visited = []
    #acts as a stack
    unvisited = [start]


    while unvisited:
        print(f"unvisited: {unvisited}")
        #sets current to the last item put in to univisited. removes it from unvisited
        current = unvisited.pop()

        #skips block if its visited
        if current in visited:
            continue
        
        #checks if the current is the end block
        if current == end:
            print(f"found end")
            pygame.time.delay(10000)
            pygame.quit()

        #puts current into visited
        visited.append(current)

        currentBox = listOfBoxObj[listOfBoxCoords.index(current)]
        currentBox.color = (200,0,200)
        currentBox.update_box()
        currentBox.draw_walls()
        pygame.display.update()


        #makes sure that the only boxes that are added are ones that are neither in visited or unvisited. this ensures that no duplicates will appear in unvisited, and no box that is already checked wil be added
        unvisited.extend([box for box in find_dfs_neighbors(current) if box not in visited and box not in unvisited])

        pygame.time.delay(20)     
                


depth_first_search()


pygame.time.delay(7000)
pygame.quit()