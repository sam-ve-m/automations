from abc import ABC
from typing import Coroutine, Any

from bokeh import models, plotting, events

from src.core.dto.graph import Graph
from src.core.static.bokeh.buttons import BokehButtonsModels
from src.core.static.javascript.buttons import ButtonsScripts
from src.core.static.javascript.graph_tool_reset import ResetToolScript
from src.services.abstract.graph_creator import AbstractGraphCreator


class CreateGraph(AbstractGraphCreator, ABC):
    @staticmethod
    async def _build_graph(graph: Graph) -> plotting.figure:
        to_plot_data = await CreateGraph._build_plot_data(graph.plot_data, graph.registers)
        source = models.ColumnDataSource(data=to_plot_data)
        figure = await CreateGraph._config_figure(graph.title, source, graph.interactions)
        return figure

    @staticmethod
    async def _build_plot_data(coverage: dict, registers: int) -> dict:
        covered, missing, labels = [], [], []
        for field, covered_ids in coverage.items():
            coverage_percent = 100 * len(covered_ids) / (registers or 1)
            covered.append(coverage_percent)
            missing.append(100 - coverage_percent)
            labels.append(field)
        return {"covered": covered, "missing": missing, "labels": labels}

    @staticmethod
    async def _config_figure(graph: str, source: models.ColumnDataSource, tap: Coroutine[Any, Any, models.TapTool]) -> plotting.figure:
        figure = await CreateGraph._build_figure(source, tap)
        styled_figure = await CreateGraph._config_figure_style(graph, figure)
        return styled_figure

    @staticmethod
    async def _build_figure(source: models.ColumnDataSource, tap: Coroutine[Any, Any, models.TapTool]) -> plotting.figure:
        tap = await tap
        figure = plotting.figure(
            width=1280,
            x_range=source.data.get("labels"),
            tooltips="@labels: @covered% x @missing%",
            tools=["hover", "pan,wheel_zoom,box_zoom,save,reset", tap],
        )
        figure.vbar_stack(
            ['missing', 'covered'],
            x='labels',
            width=0.9,
            source=source,
            color=("red", "green"),
            legend_label=['missing', 'covered']
        )
        reset_graph = models.CustomJS(code=ResetToolScript.reset_graph)
        figure.js_on_event(events.DoubleTap, reset_graph)
        figure.js_on_event(events.Reset, reset_graph)
        return figure

    @staticmethod
    async def _config_figure_style(graph: str, figure: plotting.figure) -> plotting.figure:
        figure.y_range.start = 0
        figure.x_range.range_padding = 0.25
        figure.xaxis.major_label_orientation = 0.333
        figure.xgrid.grid_line_color = None
        figure.axis.minor_tick_line_color = None
        figure.outline_line_color = None
        figure.legend.location = "top_right"
        figure.legend.orientation = "horizontal"
        figure.title = graph
        return figure

    @staticmethod
    async def _build_filter_button(graph_name: str) -> models.Button:
        filter_button = await BokehButtonsModels.crete_filter_button()
        filter_button.js_on_event(events.ButtonClick, models.CustomJS(
            args={'graph_name': graph_name},
            code=ButtonsScripts.filter_button,
        ))
        return filter_button

    @staticmethod
    async def _build_excel_button(graph_name: str) -> models.Button:
        excel_button = await BokehButtonsModels.create_excel_button()
        excel_button.js_on_event(events.ButtonClick, models.CustomJS(
            args={'representation': graph_name},
            code=ButtonsScripts.resource_excel_button,
        ))
        return excel_button
