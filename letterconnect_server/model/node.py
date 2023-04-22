class Node:

    def __init__(self, id: int, type: str, connections: list):
        self._type = type
        self._id = id
        self._connections = connections

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def connections(self):
        return self._connections

    @connections.setter
    def connections(self, value):
        self._connections.append(value)

    def get_node(self):
        return {
            "id": self.id,
            "type": self.type,
            "connection": self.connections
        }
