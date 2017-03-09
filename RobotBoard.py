import Game
import random
import Agent # replace by game_agent.py


class MyBot(object):
    """ controller for any non-humanControlled playing tokens. Using a board-representation, it can decide where
    to move, and what tiles to remove. Calls to the RandomBot must be made for each moving-or-removing turn. Future
    inheriting classes, should they fail in taking a turn, should call super() on their take_move_player_turn and
    take_remove_tile_turn, since these base functions will take any possible turn.
    """

    def __init__(self, board, player):
        self.board = board  # keep reference of game for tracking success of move (game.turnSuccessfull)
        self.player = player
    
    def take_move_player_turn(self, move_player_fxn):
        """ move player token to a random nearby tile """
        x, y = self.player.x, self.player.y
        tiles = self.board.game.get_legal_moves(self.board.game.active_player)
        target = self.board.game.machine_moves()
        move_player_fxn(target[0], target[1])


class RobotGame(Game.Game):
    """ game handles adding robots to gameplay """
    robots = dict()
    def __init__(self,player1,player2, boardsize):
        super(RobotGame, self).__init__(player1,player2)
        numPlayers = 0
        numRobots  = 0

        self.board.Player = self.Player  # set up proper inheritance
        self.board.Tile = self.Tile
        self.board.setup(boardsize)
        starting_positions = self.board.add_players(2)
        for pos in starting_positions:
            self.board.game.apply_move(pos)

        if player1.isHuman:
            numPlayers += 1
        else:
            self.setup_robot(0)
            numRobots += 1
        if player2.isHuman:
            numPlayers += 1
        else:
            numRobots += 1
            self.setup_robot(1)

        self.turnType = self.MOVE_PLAYER  # first player's turn is to move
        self.get_active_player().active = True

    def setup_robot(self, num_robot):
        """ set up robots to handle appropriate number player token """
        for ind, player in enumerate(self.board.players):
                if ind == num_robot:
                    robot = MyBot(self.board, player)
                    self.robots[player] = robot
                    player.humanControlled = False

    def robot_takes_turn(self):
        """ if active player is robot (AI), will guide robot into taking part of its turn (remove-tile or move-player) """
        activePlayer = self.get_active_player()
        if activePlayer.humanControlled:
            return
        activeRobot = self.robots[activePlayer]
        if self.turnType == self.MOVE_PLAYER:
            move_player_fxn = super(RobotGame, self).player_moves_player
            activeRobot.take_move_player_turn(move_player_fxn)
        elif self.turnType == self.GAME_OVER:
            pass  # game over, we do nothing
        else:
            raise  # problem with our logic
    
    def player_removes_tile(self, x, y):
        """ if active player is human, carry out function. Otherwise exit """
        activePlayer = self.get_active_player()
        if activePlayer.humanControlled:
            super(RobotGame, self).player_removes_tile(x, y)

    def player_moves_player(self, x, y):
        """ if active player is human, carry out function. Otherwise exit """
        activePlayer = self.get_active_player()
        if activePlayer.humanControlled:
            super(RobotGame, self).player_moves_player(x, y)
