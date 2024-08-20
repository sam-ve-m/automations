import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import nest_asyncio

from src.routes.coverage.route import coverage_route
from src.routes.details.route import details_route
from src.routes.screen.route import product_screen_route
from src.routes.update.route import update_route

nest_asyncio.apply()

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/routes/base"), name="static")


app.include_router(update_route)
app.include_router(details_route)
app.include_router(coverage_route)
app.include_router(product_screen_route)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=3334,
        debug=True,
    )
