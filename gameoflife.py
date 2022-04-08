import pygame
import numpy as np
import time

#initalize the pygame
pygame.init()

weight, height = 600, 600 # pixels

screen = pygame.display.set_mode((height, weight))

bg = (25,25,25) #background color
screen.fill(bg)

nxC, nyC = 25, 25 #number of cells

#dimension of the cells
dimCW = weight/nxC 
dimCH = height/nyC

#state of the board: 0 -> dead, 1 -> alive
gameState = np.zeros((nxC,nyC))

pauseExecute = False

#gameloop
running = True 
while running:
       
       newGameState = np.copy(gameState)
       #reset the state to add the new one
       screen.fill(bg)
       #add delay between states
       time.sleep(0.2)

       #allow exit of the GUI
       for event in pygame.event.get():
              if event.type == pygame.QUIT:
                     running = False
              #controll if the game is paused
              elif event.type == pygame.KEYDOWN:
                     pauseExecute = not pauseExecute
              
              #get the mouse state
              mouseClick = pygame.mouse.get_pressed()
              #if one mouse button is clicked then we get its possition
              if sum(mouseClick) > 0:
                     posX, posY = pygame.mouse.get_pos() #pixels
                     celX, celY = int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH))
                     newGameState[celX,celY] = not mouseClick[2]
              

       for x in range(0,nxC):
              for y in range(0,nyC):

                     #only update the state if game not paused
                     if not pauseExecute:
                            numNeigh =    gameState[(x-1) % nxC,(y-1) % nyC] + \
                                          gameState[(x)   % nxC,(y-1) % nyC] + \
                                          gameState[(x+1) % nxC,(y-1) % nyC] + \
                                          gameState[(x-1) % nxC,(y)   % nyC] + \
                                          gameState[(x+1) % nxC,(y)   % nyC] + \
                                          gameState[(x-1) % nxC,(y+1) % nyC] + \
                                          gameState[(x)   % nxC,(y+1) % nyC] + \
                                          gameState[(x+1) % nxC,(y+1) % nyC]

                            #rule 1: 3 neighbours alive -> alive
                            if gameState[x,y] == 0 and numNeigh == 3:
                                   newGameState[x,y] = 1
                            
                            #rule 2: less than 2 or more than 3 -> dead
                            if gameState[x,y] ==  1 and (numNeigh < 2 or numNeigh > 3):
                                   newGameState[x,y] = 0

                     poly = [((x)  * dimCW, (y)   * dimCH),
                            ((x+1) * dimCW, (y)   * dimCH),
                            ((x+1) * dimCW, (y+1) * dimCH),
                            ((x)   * dimCW, (y+1) * dimCH)]
 
                     #painting the cell if alive
                     if newGameState[x,y] == 0:
                            pygame.draw.polygon(screen, (128,128,128), poly, 1)
                     else:
                            pygame.draw.polygon(screen, (255,255,255), poly, 0)

       #updating the game state
       gameState = np.copy(newGameState)

       pygame.display.flip()


