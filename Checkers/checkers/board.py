import pygame
from .constants import *
from .piece import *

class Board:
    def __init__(self):
        self.board = []
        #default no. of BROWN & white pieces
        self.BROWN_left = self.white_left = 12
        #no. of kings
        self.BROWN_kings = self.white_kings = 0
        #board initialization
        self.create_board()

    def draw_places(self, window):
        #paint initial window with black
        window.fill(BLACK)

        #for every row
        for row in range(ROWS):
            #for every other column(do one and skip the next)
            for col in range(row % 2, COLS, 2):
                            #on window, in BROWN,     x,                y,                width,     height
                pygame.draw.rect(window, BROWN, (row*SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    ######FOR AI######
#get board score(negative or positive) heauristic function
    def evaluate(self):
    #equation is from the internet :(
        return self.white_left - self.BROWN_left + (self.white_kings * 0.5 - self.BROWN_kings * 0.5)
    
    #get all pieces of this color
    def get_all_pieces(self, color):
    #list of pieces without zero place
        pieces = []
    #loop in rows
        for row in self.board:
        #loop in cols
            for piece in row:
            #if the piece my color piece 
                if piece != 0 and piece.color == color:
                #add piece to list of pieces
                    pieces.append(piece)
        return pieces
    
    def move(self, piece, row, col):

        #swap piece position with desiBROWN board position 
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        
        #move piece
        piece.move(row, col)
        
        if row == ROWS - 1 or row == 0:
            #if piece at 1st/last row, make piece king
            piece.make_king()
            if piece.color == WHITE:
                #if white piece, update no. of white kings
                self.white_kings += 1
            else:
                #if BROWN piece, update no. of BROWN kings
                self.BROWN_kings += 1

    #get piece at input position
    def get_piece(self, row, col):
        return self.board[row][col]

    #create internal structure of board
    def create_board(self):

        for row in range(ROWS):

            #make a list for every row
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    #put white pieces in rows 0, 1, 2 in the column of the above condition
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    #put BROWN pieces in rows 5, 6, 7 in the column of the above condition
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BROWN))
                    
                    #rows 3, 4 have empty places/squares(no pieces)
                    else:
                        self.board[row].append(0)
                
                #places/squares between the pieces are empty 
                else:
                    self.board[row].append(0)
    
    #draw places/squares & pieces
    def draw(self, window):
        #draw places/squares
        self.draw_places(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    #if place is not empty, draw piece on window
                    piece.draw(window)

    def remove(self, pieces): #skipped dictionary pieces
        for piece in pieces:

            #replace every piece with 0
            self.board[piece.row][piece.col] = 0
            
            #if its an actual piece, not a place
            if piece != 0:
                #if BROWN, decrease number of BROWN pieces by 1
                if piece.color == BROWN:
                    self.BROWN_left -= 1
                #if white, decrease number of white pieces by 1
                else:
                    self.white_left -=1
    
    #to declare the game winner
    def winner(self):
        #if there're no BROWN pieces left, WHITE IS THE WINNER
        if self.BROWN_left <= 0:
            return WHITE
        #if there're no white pieces left, BROWN IS THE WINNER
        elif self.white_left <= 0:
            return BROWN
        
        return None

    #getting VALID moves of a piece
    def get_valid_moves(self, piece):
        
        #initialize empty dictionary
        moves = {}
        #left diagonal
        left = piece.col - 1
        #right diagonal
        right = piece.col + 1
        #the whole row which the piece belongs to
        row = piece.row

        #if its a BROWN piece or king
        if piece.color == BROWN or piece.king:
            #update the moves dictionary with:
            #starting from the row above your own row (row - 1), and either row-2 or -1 is your
            #limit(depending on the existence of a piece to skip or not),taking 1 step, to the left
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            #same procedure with the right side
            moves.update(self._traverse_right(row - 1, max(row -3, -1), -1, piece.color, right))
        
        #of course the same procedure with white but DIFFERENT/REVERSE/INVERTED COORDINATES
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves
    
    #left-diagonal traversal
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        
        #empty dictionary for the moves
        moves = {}
        #empty list for the OPPONENT PIECES
        last = []

        #for every row starting from "start", until "stop", "step" steps
        for r in range(start, stop, step):
            #if your left diagonal is less than zero (outside game borders)
            if left < 0:
                #break out the loop, do NOTHING
                break

            #current is the place at row r and left diagonal
            current = self.board[r][left]
            
            #if this current is empty
            if current == 0:
                #and if your skipped dictionary has something but your LAST DOESNT
                if skipped and not last:
                    #break out of the loop, do NOTHING
                    break
                #if you did jump over a piece
                elif skipped:
                    #then update moves with the value of "last" + "skipped"
                    moves[(r, left)] = last + skipped
                #if NO JUMPS
                else:
                    #then just update your moves with the "last" value (in that case, the "last" value will be EMPTY)
                    moves[(r, left)] = last

                #if your diagonal has an OPPONENT PIECE/ if your piece has a "jump history"
                if last:
                    #if moving upwards
                    if step == -1:
                        #update the piece position to 2 rows above the initial position 
                        row = max(r - 3, 0)
                    #if moving downwards
                    else:
                        #update position but in OPPOSITE DIRECTION
                        row = min(r + 3, ROWS)
                    #recurse with the new data
                    moves.update(self._traverse_left(r+step, row, step, color, left - 1, skipped = last))
                    moves.update(self._traverse_right(r+step, row, step, color, left + 1, skipped = last))
                break
            #if this diagonal has a piece of the same color as me, do NOTHING. its INVALID
            elif current.color == color:
                break
            #if all goes well, update your "last"
            else:
                last = [current]
            #update left diagonal to search in the next r
            left -= 1
        return moves 

    #same as _traverse_left but REVERSED COORDINATES/DIRECTIONS
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right - 1, skipped = last))
                    moves.update(self._traverse_right(r+step, row, step, color, right + 1, skipped = last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves

