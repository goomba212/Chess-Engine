# Chess-Engine

# How to use Demo (https://goomba212.github.io/Chess-Engine/)
- To select piece click on it, it’s square should go green.
- Then all the possible moves will go blue to move it click on a possible move.
- If your king is not undercheck
- Bot will then move

# How to use Code
  # Chessboard + Board.
    Every chessboard, has a board class in it "Board".
    You can make as many Board objects as you want.
    
    The chessboard class has a main board variable called "self.board".
    This is usually the board that the game you are playing on takes place.
    
    Boards are just to hold information, they do not do any move calculations.
    To make calculations, feed the board that you want to make the move/calculation to the Chessboard.
    It will usually output another updated board class, but sometimes it just outputs a list (for legal_moves methods).
    
  # Bot
    You can use the Bot class in the Demo, but I will not explain it here as it is not intentded for reuse.
    
  
