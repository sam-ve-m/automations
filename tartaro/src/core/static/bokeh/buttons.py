from bokeh import models


class BokehButtonsModels:
    @staticmethod
    async def create_excel_button():
        return models.Button(label="Excel", css_classes=["excel_button"])

    @staticmethod
    async def crete_filter_button():
        return models.Button(label="Filter")

    @staticmethod
    async def create_update_button():
        return models.Button(label="Update")
