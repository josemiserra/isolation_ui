### Isolation for AIND
A python implementation of the game Isolation. Users take turns moving their character, then removing a tile from the board. As the board shrinks, movement becomes limited until eventually a player is unable to move and therefore loses.
The game defaults to running in the browser, but can also be played through the command-line. Directly running main.py will launch the game with 2 players, one Human Player and 1 AI player. Game will be at http://127.0.0.1:5000/ where you can begin playing immediately.

HTML code generation thanks to https://github.com/lancekindle.

Agents logic engine based on Udacity Nanodegree lectures.

Code adaptation from José Miguel Serra Lleti (serrajosemi@gmail.com).

#### HOW TO ADD YOUR OWN HEURISTIC
At the beginning of main.py, modify your parameters for player 1 (robot)
and then choose your favourite heuristic.

    AB_ARGS = {"search_depth": 5, "method": 'alphabeta', "iterative": False}
    player1 = CustomPlayer(score_fn=improved_score, **AB_ARGS)


In game_agent.py YOU NEED TO ADD the field inside Custome_Player :

    isHuman = False


Note: game_agent.py is not included in the upload, replace by your
own file "game_agent.py"



Required packages:
flask

