from fastapi import APIRouter, Request, WebSocket

from src.core.dto.requests import RequestExcel
from src.routes.base.route import disconnectable_socket_function, load_html_with_a_title
from src.services.excel import ToExcelFileService
from src.services.product_page_analysis import ProductPage
from src.services.ticker_details import TickerDetails

product_screen_route = APIRouter()


@product_screen_route.get("/product_screen/{screen}")
def details(request: Request, screen: str):
    return load_html_with_a_title(screen, request)


@disconnectable_socket_function(product_screen_route, "/ws/message/product_screen/{screen}")
async def product_screen_message(websocket: WebSocket, screen: str):
    await websocket.accept()
    await websocket.send_text("Loading")
    await ProductPage.get_figure(screen, websocket.send_text)
    while True:
        active_highlights = await websocket.receive_json()
        await websocket.send_text("Loading")
        figure_as_html = await ProductPage.get_filtered_figure(screen, active_highlights)
        await websocket.send_text(figure_as_html)


@disconnectable_socket_function(product_screen_route, "/ws/details/product_screen")
async def product_screen_details(websocket: WebSocket):
    await websocket.accept()
    while True:
        ticker = await websocket.receive_text()
        ticker = ticker.split(':')[0]
        ticker_details = await TickerDetails.get_ticker_details(ticker)
        await websocket.send_text(ticker_details)


@disconnectable_socket_function(product_screen_route, "/ws/excel/product_screen/{screen}")
async def product_screen_excel(websocket: WebSocket, screen: str):
    await websocket.accept()
    while True:
        excel_request = await websocket.receive_json()
        validated_excel_request = RequestExcel(**excel_request)
        representation = validated_excel_request.representation
        highlights = validated_excel_request.highlights.get(representation, {})
        collection_excel = await ToExcelFileService.get_collection_group_excel(screen, representation, highlights)
        await websocket.send_bytes(collection_excel)


__all__ = ["product_screen_route"]
