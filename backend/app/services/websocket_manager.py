from fastapi import WebSocket
from typing import Dict, List
import uuid
import json

class ConnectionManager:
    def __init__(self):
        # Maps project_id to a list of active WebSockets
        self.active_connections: Dict[uuid.UUID, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, project_id: uuid.UUID):
        await websocket.accept()
        if project_id not in self.active_connections:
            self.active_connections[project_id] = []
        self.active_connections[project_id].append(websocket)

    def disconnect(self, websocket: WebSocket, project_id: uuid.UUID):
        if project_id in self.active_connections:
            if websocket in self.active_connections[project_id]:
                self.active_connections[project_id].remove(websocket)
            if not self.active_connections[project_id]:
                del self.active_connections[project_id]

    async def broadcast_to_project(self, project_id: uuid.UUID, message_data: dict):
        if project_id in self.active_connections:
            json_msg = json.dumps(message_data, default=str)
            for connection in self.active_connections[project_id]:
                await connection.send_text(json_msg)

manager = ConnectionManager()
