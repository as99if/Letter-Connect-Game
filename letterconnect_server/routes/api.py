from flask import Flask, jsonify, request

from letterconnect_server.model.node import Node
from letterconnect_server.model.game import Game


def api(app):
    global games
    games = []

    def validate_game_id(_id):
        """
        Validates if the game id is valid or not.
        :param _id: int
        :return: bool
        """
        for i in games:
            if _id == i.game_id:
                return True
        return False

    @app.route('/games/<int:id>', methods=['GET'])
    def game(id):
        """
        GET mtehod to return the current game with given id
        :param id: int
        :return: json str
        """
        if validate_game_id(id):
            return jsonify({
                "winner": games[id].winner,
                "current-player": games[id].current_player,
                "nodes": games[id].get_nodes()
            }), 200  # "200 - OK"

        return jsonify({'error-type': 'Game not found'}), 404  # "404 - Game not found."

    def validate_game(_game):
        """
        Validates if the node list in game is valid or not
        :param _game: dict
        :return: bool
        """
        # there can be no letter other than A, B, or C
        for i in _game.nodes:
            if i.type not in ['A', 'B', 'C']:
                return False
        return True

    @app.route('/new-game', methods=['POST'])
    def new_game():
        _nodes = [x.upper() for x in request.json['nodes']]

        nodes = []

        for i, _type in enumerate(_nodes):
            node = Node(id=i, type=_type, connections=[i])
            nodes.append(node)

        game = Game(nodes=nodes)

        # initiating game id (int)
        if len(games) > 0:
            game.game_id = games[-1].game_id + 1
        else:
            game.game_id = 0

        game.current_player = game.players[0]
        # checks if the game is valid
        if validate_game(game):
            game.current_player = game.players[0]
            games.append(game)

            return jsonify({'game-id': str(game.game_id)}), 200  # "200 - The game was created successfully."
        else:
            return jsonify({'error-type': 'Bad request, there can be no letter other than A, B, or C in nodes'}), \
                400  # "400 - Bad request"

    def if_game_over(_id, current_player):
        _game = games[_id]

        nodes = _game.nodes
        total_len = 0
        for i in nodes:
            total_len = total_len + len(i.connections)

        if total_len >= 3 * len(nodes):
            games[_id].winner = current_player
            return [True, 'Game is over']
        else:
            return [False]

    def validate_move(_id, node_from, node_to):
        """
        Validates moves from given request, returns is the move is valid and if not, why.
        :param _id: int
        :param node_from: int
        :param node_to: int
        :return: [bool, str]
        """
        _game = games[_id]
        nodes = _game.nodes

        # if node_from or node_to exceed the index of nodes
        if node_from >= len(nodes) or node_to >= len(nodes):
            return [False, 'Invalid, bad input.']

        node_connections = nodes[node_from].connections

        if validate_game_id(_id):
            # Two letters of the same kind cannot be connected to each other (i.e. A->A is not valid) - done
            if node_from == node_to or nodes[node_from].type == nodes[node_to].type:
                return [False, 'Invalid because two letters of the same kind cannot be connected to each other.']

            # A letter cannot be connected to two letters of the same type (i.e. B<-A->B is not valid)
            if node_to in node_connections:
                return [False, 'Invalid because a letter cannot be connected to two letters of the same type.']

            if len(node_connections) >= 3:
                return [False, 'Invalid because each letter can be connected with up to 2 other letters.']

            return [True]
        return [False, "Wrong game id."]

    @app.route('/games/<int:id>/move', methods=['POST'])
    def move(id):
        """
        POST method to take moves.
        :param id: int
        :return: json str
        """
        _move_from = request.json['from']  # int
        _move_to = request.json['to']  # int

        # validate if game is over
        game_over = if_game_over(id, games[id].current_player)
        if not game_over[0]:
            # validate if the move is valid
            valid = validate_move(id, _move_from, _move_to)
            if valid[0]:
                # add connection with the 'from' node according to move
                games[id].nodes[_move_from].connections = _move_to

                # if game is over, winner = games[id]['current-player']
                if_game_over(id, games[id].current_player)

                # switch current-player for the next move
                if games[id].current_player == games[id].players[0]:
                    games[id].current_player = games[id].players[1]
                else:
                    games[id].current_player = games[id].players[0]

                if games[id].winner is not None:
                    games[id].current_player = None

                return jsonify({
                    "winner": games[id].winner,
                    "current-player": games[id].current_player,
                    "nodes": games[id].get_nodes()
                }), 200  # "200 - OK"

            return jsonify({'error-type': valid[1]}), 400  # "400 - invalid move"
        return jsonify({'error-type': game_over[1]}), 400  # "400 - game_is_over"
