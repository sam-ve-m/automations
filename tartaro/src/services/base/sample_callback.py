from abc import ABC

from bokeh import models, embed

from src.core.static.javascript.buttons import ButtonsScripts
from src.core.static.javascript.graph_tool_tap import TapToolScripts
from src.services.abstract.graph_creator import AbstractGraphCreator
from src.utils import async_auxiliary


class SampleCallback(AbstractGraphCreator, ABC):
    @staticmethod
    async def _build_select_sample_callback(coverage: dict, id_list: set, graph: str) -> models.TapTool:
        ticker_sample = await SampleCallback._extract_sample(coverage, id_list)
        callback = models.CustomJS(
            args={
                'tickers_sample': ticker_sample,
                'graph_name': graph,
            },
            code=TapToolScripts.select_sample
        )
        tap = models.TapTool(callback=callback)
        return tap

    @staticmethod
    async def _extract_sample(coverage: dict, id_list: set) -> dict:
        ticker_sample = {field: SampleCallback._extract_field_sample(tickers, id_list) for field, tickers in coverage.items()}
        ticker_sample = await async_auxiliary.gather_dict_values(ticker_sample)
        return ticker_sample

    @staticmethod
    async def _extract_field_sample(tickers: list, id_list: set) -> dict:
        missing = list(id_list.difference(set(tickers)))
        tickers_sample = {
            "covered": SampleCallback._wrap_tickers_in_html(tickers[:10], "Covered: "),
            "missing": SampleCallback._wrap_tickers_in_html(missing[:10], "Missing: "),
        }
        tickers_sample = await async_auxiliary.gather_dict_values(tickers_sample)
        return tickers_sample

    @staticmethod
    async def _wrap_tickers_in_html(tickers: list, description: str) -> str:
        # tickers = [value[:40] for value in tickers]
        ticker_buttons = models.RadioButtonGroup(labels=tickers, orientation="vertical")
        ticker_buttons.js_on_click(models.CustomJS(code=ButtonsScripts.details_buttons))
        script, embed_models = embed.components((models.Div(text=description), ticker_buttons))
        return script + "".join(embed_models)

