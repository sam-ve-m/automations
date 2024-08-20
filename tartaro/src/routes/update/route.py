from fastapi import APIRouter, WebSocket

from src.routes.base.route import disconnectable_socket_function
from src.services.update_ticker import TickerUpdate
from src.utils.env_config import config

update_route = APIRouter()
allowed_passwords = config("UPDATE_ALLOWED_PASSWORDS").split(",")


@disconnectable_socket_function(update_route, "/ws/update")
async def update_ticker_fields(websocket: WebSocket):
    await websocket.accept()
    while True:
        message = await websocket.receive_json()
        password = message.get("password")
        ticker_update = message.get("ticker_fields")
        if password not in allowed_passwords:
            await websocket.send_text("Not authorized password.")
        elif not ticker_update:
            await websocket.send_text("Nothing updated.")
        else:
            update_status = await TickerUpdate.update_ticker(ticker_update)
            success_message = "; ".join((
                table + (" success" if status else " failed")
                for table, status in update_status.items()
            ))
            await websocket.send_text(success_message)


__all__ = ["update_route"]
