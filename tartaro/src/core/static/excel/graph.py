from typing import Any

from openpyxl.worksheet.worksheet import Worksheet


class GraphExcelFile:
    @staticmethod
    async def populate_sheet(sheet: Worksheet, values: list, columns: dict):
        row = 1
        for column, field in columns.items():
            sheet.cell(row=row, column=column).value = field
        for ticker in values:
            row += 1
            for column, field in columns.items():
                sheet.cell(row=row, column=column).value = str(ticker.get(field, ""))
