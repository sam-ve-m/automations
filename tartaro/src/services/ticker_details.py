from bokeh import models, embed

from src.core.static.bokeh.buttons import BokehButtonsModels
from src.core.static.html.ticker_details_table import HTMLTable
from src.core.static.javascript.buttons import ButtonsScripts
from src.infrastructure.mongo import MongoDBInfrastructure
from src.infrastructure.redis import RedisKeyDBInfrastructure
from src.repository.data_base_analysis import MongoDatabaseRepository


class TickerDetails:
    @staticmethod
    async def get_ticker_details(ticker_id: str, wrap_color: str = "black") -> str:
        mongo_infrastructure = await MongoDBInfrastructure.get_singleton_connection()
        redis_infrastructure = await RedisKeyDBInfrastructure.get_singleton_connection()
        repository = MongoDatabaseRepository(mongo_infrastructure, redis_infrastructure)
        if not (ticker_details_json := await repository.find_ticker_by_id(ticker_id.upper())):
            return "Ticker not found."

        collections_tables = [
            await HTMLTable.create_table(
                title=collection,
                columns=["Field", "Ticker"],
                rows=list(ticker_fields.items())
            )
            for collection, ticker_fields in ticker_details_json.items()
        ]
        ticker_details = await HTMLTable.union_tables(collections_tables, wrap_color)
        request_update = models.CustomJS(code=ButtonsScripts.update_button)
        request_excel = models.CustomJS(
            args={"resource": "details", "representation": ticker_id},
            code=ButtonsScripts.details_excel_button
        )
        update_button = await BokehButtonsModels.create_update_button()
        update_button.js_on_click(request_update)
        download_excel_button = await BokehButtonsModels.create_excel_button()
        download_excel_button.js_on_click(request_excel)
        components = embed.components((update_button, download_excel_button))
        layout_html = "".join((components[0], *components[1]))
        return layout_html + ticker_details
