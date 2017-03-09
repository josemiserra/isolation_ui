from Game import Tile, Player
from RobotBoard import RobotGame
from Game import GameBoard
import Sample_players

class HtmlTile(Tile):
    """ Provides export-to-html functionality on top of the traditional Tile class. For each tile, you'll need to save
    The Tile's html. Only once do you need to get the tile's style. If you want to include a link on the Tile, set
    tile's link attribute to desired link, and then call get_html
    """
    link = None

    def get_html(self):
        """ export tile state to html """
        if self.visible:
            visibility = 'visible'
        else:
            visibility = 'hidden'
        html = '<div class="tile ' + visibility  + '">'  # build html representing tile
        if self.visible and not self.player:  # do not allow clicking on tile if it's removed or player occupied
            if self.link:
                html += '<a href="' + self.link + '" class="tile-link"></a>'
        if self.player:
            html += self.player.get_html()
        html += '</div>'
        return html

    @classmethod
    def get_style(cls, size='50px'):
        """ return tile style, with an optional size parameter """
        style = 'div.tile { position: relative; width: ' + size + '; height: ' + size + ';'
        style += 'float: left; margin: 2px; }'
        style += 'div.tile.visible { background-color: #00BF4D }'
        style += 'div.tile.hidden { background-color: transparent; }'
        style += 'a.tile-link { display: block; width: ' + size + '; height: ' + size + '; }'
        return style

    def reset_links(self):
        """ reset link on tile. Useful when changing game turns """
        self.link = None

    def set_link(self, link):
        """ set tile link. After setting link, get_html() call will return html with link included """
        self.link = link
    

class HtmlPlayer(Player):
    """ Provides access to html for player token """

    def get_html(self):# build html representing player
        """ return player state in html format """
        activity = ''
        if self.disabled:
            activity = 'disabled'
        elif self.active:
            activity = 'active'
        html = '<div class="player ' + activity + '" style="background-color:' + self.color + '"></div>'
        return html

    @classmethod
    def get_style(cls, size='50px'):
        """ return player token style """
        style =  'div.player { width: ' + size + '; height: ' + size + '; border-radius: 50%; }'
        style += 'div.player.active { border: 2px solid white; box-sizing: border-box; }'
        style += 'div.player.disabled { background-image: repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(0, 0, 0, 0.5) 5px, rgba(0, 0, 0, 0.5) 10px)}'
        return style


class HtmlGameBoard(GameBoard):
    """ provides html-export functions for controlling gameboard and getting visual feel """
    Player = HtmlPlayer
    Tile = HtmlTile

    def __init__(self, *args, **kwargs):
        super(HtmlGameBoard, self).__init__(*args, **kwargs)
        self.footer = ''

    def get_html(self):
        """ return html representing board """
        html = ''
        for row in self.board:
            html += '<div class="row">'
            for tile in row:
                html += tile.get_html()
            html += '</div>'  # or some other visual break between rows
        html += self.footer  # add extras
        return html

    def set_footer(self, footer):
        """ set text at botom of html board. Typically used for announcing end-of-game message """
        self.footer = footer

    @classmethod
    def get_style(cls, size='50px'):
        """ return board style """
        return 'div.row { overflow: hidden; }'  # set each row on newline

    def reset_links(self):
        """ reset links in all tiles """
        for x, y, tile in self:
            tile.reset_links()

    def set_tile_links_for_player_move(self, player):
        """ set tile links around player for moving the player there """
        x, y = player.x, player.y
        tiles = self.get_tiles_around(x, y)
        for tile in tiles:
            x2, y2 = tile.x, tile.y
            if x == x2 and y == y2:  # skip tile under player
                continue
            tile.set_link("/move_player_to/" + str(x2) + ',' + str(y2))

class HtmlGame(RobotGame):
    """ provide html-export options to Game class """
    GameBoard = HtmlGameBoard
    Player = HtmlPlayer  # "magically" this now will spawn an HtmlPlayer, not just a normal player
    Tile = HtmlTile

    def __init__(self,player1, player2, boardsize = (7,7)):
        super(HtmlGame, self).__init__(player1,player2, boardsize)

    def get_html(self):
        """ get html of game. This will force links in board and tiles to update, and then get all html and styles for board
        and tiles and players
        """
        self.prep_links()
        html = self.board.get_html()
        style = self.get_style('50px')  # even though it's a class method, we called using self, meaning
                            # that the function will use this instance and its variables instead of the class's
        script = self.get_scripts()
        return '<style>' + style  + '</style>' + html + script
    
    @classmethod
    def get_style(cls, size='50px'):
        """ return style of game, which gathers styles from all elements of the game including board, tile, and player """
        style = cls.GameBoard.get_style(size)
        style += cls.Tile.get_style(size)
        style += cls.Player.get_style(size)
        return style

    def get_scripts(self):
        """ return scripts to execute after loading html """ 
        if not self.get_active_player().humanControlled:
            return """<script>
                                setTimeout(function(){
                                   window.location='/robot_takes_turn/';
                                }, 1000);
                            </script>"""  # reloads page after 1 second, to call robot_takes_turn
        else:
            return ""

    def prep_links(self):
        """ erase links on board and prepare new links corresponding to game state (and what turn it is) """
        self.board.reset_links()
        if self.turnType == self.MOVE_PLAYER:
            player = self.get_active_player()
            self.board.set_tile_links_for_player_move(player)
        elif self.turnType == self.GAME_OVER:
            self.board.reset_links()
            winner = self.get_active_player()
            self.board.set_footer(winner.colorName + ' player wins!!!!!!!!!!')
        else:
            raise  # problem with our logic




