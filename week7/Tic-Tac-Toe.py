"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    copy_board = board.clone()
    empty_squares = copy_board.get_empty_squares()
    if empty_squares == []:
        return SCORES[copy_board.check_win()], (-1, -1)
    else:
        score = []
        for empty_square in empty_squares:
            test_board = copy_board.clone()
            test_board.move(empty_square[0], empty_square[1], player)
            if test_board.check_win() != None:
                score.append((SCORES[test_board.check_win()], empty_square))
            else:
                move_rec = mm_move(test_board, provided.switch_player(player))
                score.append((move_rec[0], empty_square))
        if player == provided.PLAYERX:         
            return max(score)          
        else:
            return min(score)
            
def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

#provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
