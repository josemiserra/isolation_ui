from HtmlBoard import HtmlGame
from Sample_players import null_score, open_move_score, improved_score, HumanPlayer
from Agent import CustomPlayer, custom_score



if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)  # http://flask.pocoo.org/docs/0.10/quickstart/#quickstart


    AB_ARGS = {"search_depth": 5, "method": 'alphabeta', "iterative": False}
    player1 = CustomPlayer(score_fn=improved_score, **AB_ARGS)
    player2 = HumanPlayer()
    board_dimensions = (7, 7)
    game = HtmlGame(player1, player2, board_dimensions)

    @app.route("/")
    def root_url():
        return game.get_html()

    @app.route("/move_player_to/<int:x>,<int:y>")
    def move_player_to(x, y):
        game.player_moves_player(x, y)
        return game.get_html()

    @app.route("/robot_takes_turn/")
    def robot_takes_turn():
        game.robot_takes_turn()
        return game.get_html()

    app.run(debug=False)  # run with debug=True to allow interaction & feedback when
                    # error / exception occurs.
                    # however, debug mode is super unsecure, so don't use it when allowing any ip connection

