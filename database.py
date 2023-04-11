from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


class GraphDB:
    def __init__(self) -> None:
        self.conn = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')

    def get_traversal(self):
        return traversal().withRemote(self.conn)
