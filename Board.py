import numpy as np
import random
#=================================================================
class _GamePieceAccess:

    def __iter__(self):
        for x in range(self.w):
            for y in range(self.h):
                yield x, y, self.board[x, y]

    def __getitem__(self, *args):
        return self.board.__getitem__(*args)

    def __setitem__(self, *args):
        self.board.__setitem__(*args)

    def get_player_at(self, x, y):
        """ return player attribute of tile at specified x, y coordinates """
        return self[x, y].player

    def remove_at(self, x, y):
        """ "Remove" Tile at specified coordinate. This will set the visible attribute to False """
        self.board[x, y].visible = False

    def move_player(self, player, x, y):
        """ move player from occupied tile to tile @ x, y coordinates. """
        tile = self[player.x, player.y]
        tile.player = None
        player.move_to(x, y)
        target = self[x, y]
        target.player = player


#=================================================================
class _BoardSetup(_GamePieceAccess):
    Player = None
    Tile = None
    board = None
    shape = (0, 0)

    def setup(self, size=(9,9)):
        """ populate board with Tiles, according to the size argument

        :param size: size of board to construct in (x, y) format.
        """
        w, h = size
        self.shape = (h, w)
        self.w = w
        self.h = h
        rows = []
        for x in range(w):
            col = [self.Tile(x,y) for y in range(h)]
            rows.append(col)
        self.board = np.array(rows)
        self.players = []

    def add_players(self, qty):
        """ add players to the board in quantity specified, spacing them equally apart """
        startingPositions = self.get_starting_positions_for_players(qty)
        self.players = [None]*qty
        for i in range(qty):
            p = self.Player(*startingPositions[i])
            self.players[i] = p
            self.move_player(p, p.x, p.y)
        return startingPositions

    def get_starting_positions_for_players(self, qty):
         """ calculate (x, y) coordinates for qty of players, equally distributing them around the edges of the board """
         positions = []
         for i in range(qty):
             x = random.choice(range(self.w))
             y = random.choice(range(self.h))
             while self.out_of_bounds(x, y) or (x,y) in positions:
                 x = random.choice(range(self.w))
                 y = random.choice(range(self.h))
             positions.append((x,y))

         return positions




#=================================================================
class GameBoard(_BoardSetup):
    """ GameBoard that holds the tiles and players in one place. Allow manipulation of Players and Tiles, and provide
    functions for gathering data about specific states of the GameBoard. After initilization, requires setup() function
    call in order to populate the GameBoard, then a call to add_players(x) to add x players to game

    Attributes:
        Player: reference to Player class. You can change which player class to instantiate by overriding this attribute
                with your own Player class. Easiest way to do this is to through inheriting GameBoard with your own
                GameBoard class.
        Tile:   reference to Tile class to use when populating the GameBoard. Just Like Player, you can overwrite this
                reference to use your own Tile class if desired.
        board:  The actual board: a numpy array of Tiles. the GameBoard class itself provides native get and set methods
                so that you do not have to access board directly. Instead, just use gameboard[x, y].
        shape:  a numpy-style shape describing shape of gameboard.
    """

    def __init__(self, game_controller):
        self.game = game_controller


    def to_number_grid(self, **kwargs):
        ''' returns a numpy array representing the state of the tiles. 
        defaults: 0 = invisible / removed, 1 = present, -1 = player occupying location
        '''
        playerVal = float(kwargs.get('players', -1))  # allow overriding of default values
        tileVal = float(kwargs.get('tiles', 1))
        gapVal = float(kwargs.get('gaps', 0))
        grid = np.zeros((self.w, self.h)) + gapVal
        for x in range(self.w):
            for y in range(self.h):
                if self.board[x, y].player:
                    grid[x, y] = playerVal
                elif self.board[x, y].visible:
                    grid[x, y] = tileVal
        return grid

    def __str__(self):
        return str(self.board.transpose())  # transpose because numpy's representation will show x/y reversed

    def out_of_bounds(self, x, y):
        """ Return True if coordinates x, y are outside the boundaries of the GameBoard. Return False if a Tile is
        accessible at those coordinates
        """
        w, h = self.w, self.h
        if x >= w or y >= h:
            return True
        if x < 0 or y < 0:
            return True
        return False

    def get_tiles_around(self,x,y):
         available_moves = self.game.get_legal_moves(self.game.active_player)
         return [ self.board[el[0],el[1]] for el in available_moves]

    def is_valid_player_move(self, player, x, y):
        """ :return: True if x, y coordinate is an open tile, visible, and next to the specified player, False otherwise. """
        if not self[x, y].visible:
            return False
        if not self[x, y] in self.game.get_legal_moves(self.game.get_active_player()):
            return False
        if self.get_player_at(x, y):
            return False
        return True

    def is_valid_tile_remove(self, x, y):
        """ :return: True if Tile is visible on board, not solid, and unoccupied by a player, False otherwise. """
        if not self[x, y].visible:
            return False
        if self[x, y].solid:
            return False
        if self.get_player_at(x, y):
            return False
        return True