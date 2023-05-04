#pygame is a python game library that allows coding the UI along with the
#algorithm. it was a much more reliable, effecient and convenient option
#to play the game install pygame first
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BROWN
from checkers.game import Game
from checkers.algorithm import alphabeta
#build module

#frame rate/fps
FPS = 60
#interface
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#game name/title
pygame.display.set_caption("Checkers")

def get_mouse_row_col(pos):
    
    #unpack pos tuple into x, y
    x, y = pos

    #int divide x, y by SQUARE_SIZE to get no. of row, col
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()

    game = Game(WIN)
    
    #whole game loop
    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = alphabeta(game.get_board(), 6, WHITE, game)
            game.ai_move(new_board)

        #if you have a winner:
        if game.winner() != None:
            #declare the winner
            print(game.winner())
            #& stop the game loop
            run = False


        #event loop (some pygame essentials for mouse clicks)
        for event in pygame.event.get():
            #if user exits/closes the game
            if event.type == pygame.QUIT:
                #IMPORTANT: stop the game loop
                run = False

            #when the mouse is clicked    
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                #get mouse position
                pos = pygame.mouse.get_pos()

                #unpack mouse position tuple into row, col
                row, col = get_mouse_row_col(pos)

                game.select(row, col)
        
        game.update()

    pygame.quit()

main()