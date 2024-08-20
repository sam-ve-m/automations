from abc import ABC, abstractmethod

from bokeh import models, layouts, plotting

from src.core.dto.graph import Graph
from src.core.static.html.static_components import GraphsHTMLAuxiliaries


class AbstractGraphCreator(ABC):
    @classmethod
    async def _create_figure(cls, coverage: dict, graph_title: str) -> models.LayoutDOM:
        ids_list = set(coverage.get("_id", []))
        select_sample_callback = cls._build_select_sample_callback(coverage, ids_list, graph_title)
        documents_found = len(ids_list)
        graph = Graph(
            title=graph_title,
            plot_data=coverage,
            registers=documents_found,
            interactions=select_sample_callback
        )
        figure = await cls._build_graph(graph)
        excel_button = await cls._build_excel_button(graph_title)
        filter_button = await cls._build_filter_button(graph_title)
        query_result_text = f"Documents found: {documents_found}."
        tickers_samples = models.Div(text=GraphsHTMLAuxiliaries.ticker_interactive_analysis)
        graphs_filter = models.Div(text=GraphsHTMLAuxiliaries.graph_filters_place_holder, width=1280)
        layout = layouts.column([layouts.row(*components) for components in {
            "zero_row": (graphs_filter, ),
            "first_row": (models.PreText(text=query_result_text), filter_button, excel_button),
            "second_row": (layouts.row(figure, layouts.column(tickers_samples)), ),
        }.values()])
        return layout

    @staticmethod
    @abstractmethod
    async def _build_select_sample_callback(coverage: dict, id_list: set, graph_name: str) -> models.TapTool:
        pass

    @staticmethod
    @abstractmethod
    async def _build_graph(graph: Graph) -> plotting.figure:
        pass

    @staticmethod
    @abstractmethod
    async def _build_filter_button(graph_name: str) -> models.Button:
        pass

    @staticmethod
    @abstractmethod
    async def _build_excel_button(graph_name: str) -> models.Button:
        pass
