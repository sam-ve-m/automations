from functools import wraps

from fastapi import Request, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

base_templates = Jinja2Templates(directory="src/routes/base")


def load_html_with_a_title(page_title: str, request: Request):
    return base_templates.TemplateResponse("page.html", {"request": request, "query": page_title})


def socket_function(route_sockets: list):
    def register_socket_function(function):
        route_sockets.append(function)
    return register_socket_function


def disconnectable_socket_function(router, url):
    def disconnectable_function(function):
        @wraps(function)
        async def websocket_function(*args, **kwargs):
            try:
                await function(*args, **kwargs)
            except RuntimeError as error:
                if "disconnect message" not in str(error):
                    raise error
            except WebSocketDisconnect:
                pass
        router.websocket(url)(websocket_function)
    return disconnectable_function
