import numpy as np
import math
from Board import GameBoard
import Isolation

class Tile:
    """ A GameBoard is composed of rows and columns of Tiles. Each Tile has a specific x and y coordinate. It is up to
    the GameBoard setup to ensure a Tile has the correct x and y coordinates. When a Tile is NOT visible, it is
    considered removed from the Board, and can not be occupied by a Player.
    Tiles are considered "Landable" if a player can move onto it. "Removable" indicates the tile can be removed

    :Attributes
        visible: if the Tile has not been removed from the GameBoard. True=> NOT removed. False=> REMOVED FROM BOARD
        solid: specifies if Tile is removable. If True, Tile cannot be removed
        player: reference to player token. player = None if Tile is unoccupied. When checking if a player occupies a
            particular Tile, use player == tile, or player in board[i, j] also works
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = True
        self.solid = False
        self.player = None

    def __repr__(self):
        pos = str(self.x) + ',' + str(self.y)
        player = '' if self.player is None else self.player.color + '@'
        return player + pos

    def __eq__(self, obj):
        """ match both the tile and player
        so that we can match if a player is IN board[x,y]
        """
        if obj is None:
            return False
        if obj == self.player:
            return True
        if obj is self:
            return True
        return False

    def __hash__(self):
        """ must define a hash method if you override __eq__ in python 3. Hashing allows sets to hold tiles """
        return id(self)

    def set_visible(self, tf):
        """
        :param tf: boolean True or False to set visible attribute.
        """
        self.visible = tf


class Player:
    """ Player is moved around the board, and is trapped once it cannot move on it's own turn.

    Attributes:
        x, y: x, y coordinate on the GameBoard
        color: the color of the player token.
        active: set to True when it is player's turn to move and remove tiles.
        disabled: permanently set to True when player has active turn and is unable to move. Usually this indicates
            player will remain inactive for the rest of the game.
        humanControlled: set to False if a robot is expected to control this Player Token's turn.
    """
    _colors = [("#FF0000", "Red"), ("#0000FF", "Blue"), ("#00FF00", "Green"),
               ("#FF00FF", "Purple"), ("#00FFFF", "Cyan"), ("#FFFF00", "Yellow")]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color, self.colorName = self._colors.pop(0)
        self._colors.append(self.color)  # put first color at end of class-wide list -> so next instance gets new color
        self.disabled = False
        self.active = False  # for determining style. Game will set Player's currentPlayer to True when it has turn
        self.humanControlled = True  # for determining which Players are robots / AI controlled

    def move_to(self, x, y):
        """ reassigns coordinates. Because it does not reassign player to Tile, this function should only be called by
        board's move_to() function
        """
        self.x = x
        self.y = y
        

class BoardExporter:
    """ allow exporting board to grid. Copies all relevant data from the board and then gives access to analyzing functions
    """
    def __init__(self, board):
        self._board = board

    def export_gap_points(self):
        """ return list of coordinates for removed tiles """
        gaps = []
        for x, y, tile in self._board:
            if not tile.visible:
                gaps.append((x, y))
        return gaps

    def export_player_points(self):
        """ return list of coordinates for players """
        players = []
        for x, y, tile in self._board:
            if tile.player:
                players.append(x, y)
        return players

    def export_board_size(self):
        """ return width and height of board """
        w, h = self._board.w, self._board.h
        return w, h


class Game:
    """ Game keeps track of the GameBoard and game-state. It is responsible for interfacing with the user/player,
    checking that any tile remove or player token move action is valid and then applying the action. It also keeps
    track of whose turn it is, and what type of turn it is (removing tile or moving player).

    Attributes:
        turnSuccessful: True or False if the last command (to move player or remove tile) was valid and executed
        turnType: type of turn, REMOVE_TILE or MOVE_PLAYER, or GAME_OVER
        board: reference to the gameboard.
    """
    REMOVE_TILE = 5
    MOVE_PLAYER = 6
    GAME_OVER = 4
    GameBoard = GameBoard
    Player = Player
    Tile = Tile
    turnSuccessful = False  # a status indicator only.
    turnType = None


    def __init__(self, player1, player2, startsFirst = 1):

        if(startsFirst == 1):
            self.control_game = Isolation.Board(player1, player2)
        else:
            self.control_game = Isolation.Board(player2, player1)
        self.board = self.GameBoard(self.control_game)

    def setup(self, numPlayers=2, shape=(7,7)):
        """ set up board shape and populate players, set active player. After this, game will be ready to play """
        self.board = self.GameBoard()
        self.board.Player = self.Player  # set up proper inheritance
        self.board.Tile = self.Tile
        self.board.setup(shape)
        starting_positions = self.board.add_players(numPlayers)
        for pos in starting_positions:
            self.control_game.apply_move(pos)
        self.turnType = self.MOVE_PLAYER  # first player's turn is to move
        self.get_active_player().active = True
    
    def get_active_player(self):
        """ return player who has "control" of current turn """
        return self.board.players[0]

    def setup_next_active_player(self):
        """ Cycle through players, making next player active. Check that newly active player is not trapped. If trapped,
        mark player as inactive and cycle to next player. Inactive players will be skipped in future cycles.
        """
        if not self.is_game_over():
            pastPlayer = self.board.players.pop(0)  # cycle to next player
            pastPlayer.active = False
            self.board.players.append(pastPlayer)
            activePlayer = self.get_active_player()
            activePlayer.active = True
    
    def setup_next_turn(self):
        """ Cycle game state from one turn to the next, cycling through active players as necessary. """
        if self.is_game_over():
            self.end_game()
            return
        if self.turnType == self.MOVE_PLAYER:
            self.setup_next_active_player()
            return

    def end_game(self):
        """ perform end-game functions that ensure the game grinds to a halt """
        self.turnType = self.GAME_OVER

    def is_game_over(self):
        """ return True if game over"""
        if self.board.game.is_winner(self.board.game.active_player) or \
           self.board.game.is_loser(self.board.game.active_player):
            return True
        return False


    def player_moves_player(self, x, y):
        """ take turn on game by moving player. Checks that turn is valid, and afterwards rolls over to next turn """
        player = self.get_active_player()
        if self.turnType == self.MOVE_PLAYER and self.board.game.move_is_legal((x,y)):
            old_x = player.x
            old_y = player.y
            self.board.move_player(player, x, y)
            self.board.remove_at(old_x, old_y)
            self.board.game.apply_move((x,y))
            self.setup_next_turn()
            self.turnSuccessful = True
        else:
            self.turnSuccessful = False


# only run this code if run directly, NOT imported
if __name__ == '__main__':
    game = Game()
    game.setup()
    board = game.board
    print(board)
