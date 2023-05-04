import pygame
from .constants import *
from checkers.board import *

class Game:
    def __init__(self, window):
        #initialize game
        self._init()
        self.window = window

    #updating
    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    #private method because its called by two other methods
    def _init(self):
        #initial game state
        self.selected = None
        self.board = Board()
        self.turn = BROWN
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    #reset game to initial state
    def reset(self):
        self._init()

    def select(self, row, col):
        #if something selected
        if self.selected:
            #try to move selected piece somewhere
            result = self._move(row, col)
            #if cant move
            if not result:
                #keep it unselected
                self.selected = None
                #reselect something else
                self.select(row, col)
            
        
        #get piece
        piece = self.board.get_piece(row, col)
        #if not empty place and  its the piece turn
        if piece != 0 and piece.color == self.turn:
            #select piece and add it to valid moves
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        
        return False

    def _move(self, row, col):
        #get piece
        piece = self.board.get_piece(row, col)
        #if selected piece isnt another piece(empty) and its a valid move
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            #move piece to passed row, col
            self.board.move(self.selected, row, col)
            #position of the piece is in skipped
            skipped = self.valid_moves[(row, col)]
            
            #if skipped remove it entirely
            if skipped:
                self.board.remove(skipped)
            
            self.change_turn()
        else:
            return False
        
        return True
    
    #drawing the little circles that indicate valid positions to move to
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            #to get them right in the middle of the square with length 15 pixels
            pygame.draw.circle(self.window, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    #changing turns
    def change_turn(self):
        self.valid_moves = {}
        #if its BROWN's turn, time to give it to white
        if self.turn == BROWN:
            self.turn = WHITE
        #if not do the opposite
        else:
            self.turn = BROWN


######FOR AI######

#define the board FOR THE AI
    def get_board(self):
        return self.board

#guess the move
    def ai_move(self, board):
        self.board = board
        self.change_turn()