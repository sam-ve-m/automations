from fastapi import APIRouter, WebSocket, Request

from src.routes.base.route import load_html_with_a_title, disconnectable_socket_function
from src.services.excel import ToExcelFileService
from src.services.ticker_details import TickerDetails

details_route = APIRouter()


@details_route.get("/details/{ticker}")
def details(request: Request, ticker: str):
    return load_html_with_a_title(ticker, request)


@disconnectable_socket_function(details_route, "/ws/message/details/{ticker}")
async def details_message(websocket: WebSocket, ticker: str):
    await websocket.accept()
    await websocket.send_text("Loading")
    while True:
        ticker_details = await TickerDetails.get_ticker_details(ticker)
        await websocket.send_text(ticker_details)
        await websocket.receive_text()


@disconnectable_socket_function(details_route, "/ws/details/details")
async def details_details(websocket: WebSocket):
    await websocket.accept()
    await websocket.receive_text()
    this_line_is_never_ment_to_be_reached = ConnectionRefusedError("This feature is not implemented in this route")
    raise this_line_is_never_ment_to_be_reached


@disconnectable_socket_function(details_route, "/ws/excel/details/{ticker}")
async def details_excel(websocket: WebSocket, ticker: str):
    await websocket.accept()
    while True:
        await websocket.receive()


@disconnectable_socket_function(details_route, "/ws/excel/details")
async def details_excel(websocket: WebSocket):
    await websocket.accept()
    while True:
        ticker = await websocket.receive_text()
        ticker_excel = await ToExcelFileService.get_ticker_excel(ticker)
        await websocket.send_bytes(ticker_excel)


__all__ = [
    "details_route",
]
