import pygame
from .constants import SQUARE_SIZE, GREY, BROWN, WHITE, CROWN

class Piece:

    #padding between piece & place
    PADDING = 15
    #piece outline/border 
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        #place coordinates
        self.x = 0
        self.y = 0
        #calculate piece position in place
        self.calc_pos()

    def calc_pos(self):
        #column center 
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        #row center
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    #change king status
    def make_king(self):
        self.king = True

    def draw(self, window):
        
        #radius of piece and exclude padding in order not to draw in the whole place/square
        radius = SQUARE_SIZE // 2 - self.PADDING
        #               on window, in grey, at same coord. , draw circle of size radius+outline(draw a bigger circle thats grey)
        pygame.draw.circle(window, GREY, (self.x, self.y), radius + self.OUTLINE)

        #               on window, in color, at place/square coord. , with size radius
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        #draw image on window, subtract 0.5 width & 0.5 height from x & y to draw crowm right in th middle
        if self.king:
            window.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    #BROWNraw piece at input position
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
    
    def __repr__(self):
        return str(self.color)