class HTMLTable:
    @staticmethod
    async def _table_style(color: str):
        return """
        <style>
            table {
                border-collapse: collapse;
                border-spacing: 0;
                border: 3px solid """ + color + """;
                table-layout: fixed;
                width: fit-content;
                min-width: 400px;
            }
            caption {
                border: 3px solid """ + color + """;
                background: """ + color + """;
                color: white;
            }
            table th, table td, table textarea {
                border: 1px solid black;
                align-content: center;
                text-align: center;
            }
            table td:first-child {
                font-style: italic;
            }
            table textarea {
                resize: vertical;
                height: 1px;
                width: 100%;
                padding: 0;
                border: 0;
            }
        </style>
        <script type="text/javascript">
            var text_areas = document.getElementsByTagName("textarea")
            for (element of text_areas){
             element.style.height = element.scrollHeight+'px'; 
            }
        </script>
        """

    @staticmethod
    async def create_table(title: str, columns: list, rows: list):
        table = f"<table><caption><b><i>{title}</i></b></caption>"
        table_columns = "</th><th>".join(columns)
        table += "<tr><th>" + table_columns + "</th></tr>"
        for field, value in rows:
            table += f"""<tr>
                <td>{field}</td>
                <td><textarea>{value}</textarea></td>
            </tr>"""
        table += "</table>"
        return table

    @staticmethod
    async def union_tables(tables: list, color: str) -> str:
        tables = '<div style="align-content: center;">' + "<br>".join(tables) + "</div>"
        return await HTMLTable._table_style(color) + tables
