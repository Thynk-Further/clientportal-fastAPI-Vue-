import uuid
from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # Dictionary mapping project_id (as string) to a list of active WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # Dictionary mapping user_id (as string) to a list of active WebSockets (Freelancers)
        self.user_rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, project_id: str):
        await websocket.accept()
        if project_id not in self.active_connections:
            self.active_connections[project_id] = []
        self.active_connections[project_id].append(websocket)

    def disconnect(self, websocket: WebSocket, project_id: str):
        if project_id in self.active_connections:
            if websocket in self.active_connections[project_id]:
                self.active_connections[project_id].remove(websocket)
            # Clean up empty lists
            if not self.active_connections[project_id]:
                del self.active_connections[project_id]

    async def connect_user(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.user_rooms:
            self.user_rooms[user_id] = []
        self.user_rooms[user_id].append(websocket)

    def disconnect_user(self, websocket: WebSocket, user_id: str):
        if user_id in self.user_rooms:
            if websocket in self.user_rooms[user_id]:
                self.user_rooms[user_id].remove(websocket)
            if not self.user_rooms[user_id]:
                del self.user_rooms[user_id]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast_to_project(self, project_id: str, message: dict):
        if project_id in self.active_connections:
            for connection in self.active_connections[project_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    # In case the connection is already closed/broken but not yet cleaned up
                    pass

    async def broadcast_to_user(self, user_id: str, message: dict):
        if user_id in self.user_rooms:
            for connection in self.user_rooms[user_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

manager = ConnectionManager()
