# database.py
import asyncio
from aiogremlin import DriverRemoteConnection, Graph
from gremlin_python.process.traversal import T


class GraphDB:
    def __init__(self, conn=None) -> None:
        self.loop = asyncio.get_event_loop()
        self.conn = conn

    async def get_traversal(self):
        if not self.conn:
            self.conn = await DriverRemoteConnection.open('ws://localhost:8182/gremlin')
        g = Graph().traversal().withRemote(self.conn)
        return g

    async def close_connection(self):
        if self.conn:
            await self.conn.close()
            self.conn = None

    async def create_vertex(self, label: str, properties: dict) -> dict:
        g = await self.get_traversal()
        vertex = g.addV(label).property(T.id, properties["id"])
        for key, value in properties.items():  # Iterate over the properties
            vertex = vertex.property(key, value)
        result = await vertex.toList()
        await self.close_connection()
        return result[0]
