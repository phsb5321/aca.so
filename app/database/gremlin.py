# app/database/gremlin.py
import asyncio
from aiogremlin import DriverRemoteConnection, Graph
from gremlin_python.process.traversal import T


class GraphDB:
    def __init__(self, conn=None) -> None:
        # Initialize the event loop and set the connection to None
        self.loop = asyncio.get_event_loop()
        self.conn = conn

    async def get_traversal(self):
        """
        Get a graph traversal instance using the connection.
        If a connection is not available, create a new connection to the Gremlin server.

        :return: Graph traversal instance
        """
        if not self.conn:
            self.conn = await DriverRemoteConnection.open('ws://localhost:8182/gremlin')
        g = Graph().traversal().withRemote(self.conn)
        return g

    async def close_connection(self):
        """
        Close the connection if it exists.
        """
        if self.conn:
            await self.conn.close()
            self.conn = None

    async def create_vertex(self, label: str, properties: dict) -> dict:
        """
        Create a new vertex with the specified label and properties.

        :param label: Label for the new vertex
        :param properties: Dictionary containing the properties for the new vertex
        :return: The created vertex as a dictionary
        """
        g = await self.get_traversal()
        vertex = g.addV(label).property(T.id, properties["id"])

        # Iterate over the properties and add them to the new vertex
        for key, value in properties.items():
            vertex = vertex.property(key, value)

        result = await vertex.toList()
        await self.close_connection()
        return result[0]

    async def create_relationship(self, from_id: str, to_id: str, relationship_label: str) -> None:
        """
        Create a relationship between two vertices using the specified relationship label.

        :param from_id: ID of the vertex from which the relationship starts
        :param to_id: ID of the vertex to which the relationship points
        :param relationship_label: Label for the relationship
        """
        g = await self.get_traversal()

        # Create the relationship between the vertices with the specified label
        await g.V(from_id).addE(relationship_label).to(g.V(to_id)).toList()

        await self.close_connection()
