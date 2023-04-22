class Game:

    def __init__(self, nodes: list):
        self._winner = None
        self._current_player = None
        self._game_id = None
        self._nodes = nodes
        self._players = ["first", "second"]

    @property
    def game_id(self):
        return self._game_id

    @game_id.setter
    def game_id(self, value):
        self._game_id = value

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        self._nodes = value

    @property
    def current_player(self):
        return self._current_player

    @current_player.setter
    def current_player(self, value):
        self._current_player = value

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, value):
        self._winner = value

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, value):
        self._players = value

    def get_nodes(self):
        _nodes = []
        for n in self.nodes:
            _nodes.append(n.get_node())
        return _nodes
