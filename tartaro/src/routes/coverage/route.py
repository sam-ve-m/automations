from fastapi import APIRouter, Request, WebSocket

from src.core.dto.requests import RequestExcel
from src.routes.base.route import load_html_with_a_title, disconnectable_socket_function
from src.services.excel import ToExcelFileService
from src.services.percent_coverage import FieldsCoverage
from src.services.ticker_details import TickerDetails

coverage_route = APIRouter()


@coverage_route.get("/coverage/{collection}")
def details(request: Request, collection: str):
    return load_html_with_a_title(collection, request)


@disconnectable_socket_function(coverage_route, "/ws/message/coverage/{collection}")
async def coverage_message(websocket: WebSocket, collection: str):
    await websocket.accept()
    await websocket.send_text("Loading")
    await FieldsCoverage.get_figure(collection, websocket.send_text)
    while True:
        active_highlights = await websocket.receive_json()
        await websocket.send_text("Loading")
        active_highlights = active_highlights.get(collection, {})
        figure_as_html = await FieldsCoverage.get_filtered_figure(collection, active_highlights)
        await websocket.send_text(figure_as_html)


@disconnectable_socket_function(coverage_route, "/ws/details/coverage")
async def coverage_details(websocket: WebSocket):
    await websocket.accept()
    while True:
        ticker = await websocket.receive_text()
        ticker_details = await TickerDetails.get_ticker_details(ticker)
        await websocket.send_text(ticker_details)


@disconnectable_socket_function(coverage_route, "/ws/excel/coverage/{collection}")
async def coverage_excel(websocket: WebSocket, collection: str):
    await websocket.accept()
    while True:
        excel_request = await websocket.receive_json()
        validated_excel_request = RequestExcel(**excel_request)
        highlights = validated_excel_request.highlights.get(collection, {})
        collection_excel = await ToExcelFileService.get_collection_excel(collection, highlights)
        await websocket.send_bytes(collection_excel)


__all__ = ["coverage_route"]
