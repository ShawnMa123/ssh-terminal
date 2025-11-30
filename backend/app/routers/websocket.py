"""
WebSocket router for SSH terminal communication
"""
import asyncio
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.ssh_manager import ssh_manager


logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/ws/ssh/{session_id}")
async def websocket_ssh_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for SSH terminal communication

    Protocol:
        Client -> Server:
            {"type": "input", "data": "command"}
            {"type": "resize", "cols": 80, "rows": 24}

        Server -> Client:
            {"type": "output", "data": "terminal output"}
            {"type": "connected"}
            {"type": "disconnected", "reason": "..."}
            {"type": "error", "message": "..."}
    """
    await websocket.accept()
    logger.info(f"WebSocket connected for session {session_id}")

    # Get SSH connection
    connection = ssh_manager.get_connection(session_id)

    if not connection:
        await websocket.send_json({
            "type": "error",
            "message": f"SSH session {session_id} not found"
        })
        await websocket.close()
        return

    if not connection.connected:
        await websocket.send_json({
            "type": "error",
            "message": "SSH connection not established"
        })
        await websocket.close()
        return

    # Setup data callback to forward SSH output to WebSocket
    async def on_ssh_data(data: bytes):
        """Forward SSH data to WebSocket"""
        try:
            await websocket.send_json({
                "type": "output",
                "data": data.decode("utf-8", errors="replace")
            })
        except Exception as e:
            logger.error(f"Failed to send SSH output: {e}")

    # Register callback
    connection.on_data = on_ssh_data

    # Send connected message
    await websocket.send_json({"type": "connected"})

    try:
        # Main message loop
        while True:
            # Receive message from WebSocket
            message = await websocket.receive_text()

            try:
                data = json.loads(message)
                msg_type = data.get("type")

                if msg_type == "input":
                    # User input - send to SSH
                    user_input = data.get("data", "")
                    await connection.send(user_input)

                elif msg_type == "resize":
                    # Terminal resize
                    cols = data.get("cols", 80)
                    rows = data.get("rows", 24)
                    await connection.resize(cols, rows)

                elif msg_type == "ping":
                    # Heartbeat
                    await websocket.send_json({"type": "pong"})

                else:
                    logger.warning(f"Unknown message type: {msg_type}")

            except json.JSONDecodeError:
                logger.error(f"Invalid JSON message: {message}")

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })

    finally:
        # Cleanup
        connection.on_data = None
        logger.info(f"WebSocket handler finished for session {session_id}")
