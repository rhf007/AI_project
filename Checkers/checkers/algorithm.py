from copy import deepcopy #create copy of object 
import pygame

BROWN = (80, 38, 17)
WHITE = (255,255,255)

#"position" is board, state tree depth, bool value for max/min player, game, "cond=float('inf") is a ython trick to define infinity"
def alphabeta(position, depth, max_player, game, cond = float('inf')):
    
    #leaf node or winner
    if depth == 0 or position.winner() != None:
        #return board and its evaluation/score
        return position.evaluate(), position
    
    #if in max side of the tree/maximizing score
    if max_player:

        #first initialize your max evaluation equal to -infinity to choose greatest values
        maxEval = float('-inf')
        #best move
        best_move = None

        #for every single board in the game state tree
        for move in get_all_moves(position, WHITE, game):
            #perform the alphabeta on the board (with the new depth, depth goes backwards/upwards) and the min player
            evaluation = alphabeta(move, depth - 1, False ,game ,maxEval)[0]
            
            #this is to prevent the infinite  loop,
            #definitely paid the price and
            #learned the lesson the hard way
            if evaluation >= cond:
                break
            
            #update the maxEval to the new/greater value/evaluation
            maxEval = max(maxEval, evaluation)
            
            #if maxEval is UPDATED
            if maxEval == evaluation:
                #then this board leads me to a better turn/game/score, etc.
                best_move = move

        return maxEval, best_move
    
    #if in min side of the tree/ minimizing score
    else:
        #same but REVERSE EVERYTHING
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, BROWN, game):
            evaluation = alphabeta(move, depth - 1, True, game, minEval)[0]
            if evaluation <= cond:
                break
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
                
        return minEval, best_move

#function to get all possible moves, all possible scenarios. THE WHOLE GAME STATE TREE
def get_all_moves(board, color, game):
    
    #make a list for BOARDS. "moves" is just a name
    moves = []

    #for every piece of a color
    for piece in board.get_all_pieces(color):
        #get all valid moves for that piece
        valid_moves = board.get_valid_moves(piece)

        #for every key:value(move:skipped) in those valid moves
        for move, skip in valid_moves.items():
            #create a temporary/imaginary board and copy everything to it
            temp_board = deepcopy(board)
            #same to the pieces, copy the pieces
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            #new_board: contains the temporay board after doing a movement simulation on it.
            #contains the returned board from move_sim
            new_board = move_sim(temp_piece, move, temp_board, game, skip)
            #add it to your list of moves(boards in that case)
            moves.append(new_board)
    return moves

#function to simulate movement of pieces on the temporary/imaginary board.
def move_sim(piece, move, board, game, skip):
    #move the piece to row, col
                        #row    #col
    board.move(piece, move[0], move[1])
    
    #if theres a piece to be skipped
    if skip:
        #remove it entirely (from your display, etc.)
        board.remove(skip)
    return board

