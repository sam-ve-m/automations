class ButtonsScripts:
    filter_button: str = """
        const ticker_details_placeholder = document.getElementById("ticker_details_placeholder");
        ticker_details_placeholder.innerHTML = "";
        const covered_tickers_placeholder = document.getElementById("covered_tickers");
        covered_tickers_placeholder.innerHTML = "";
        const missing_tickers_placeholder = document.getElementById("missing_tickers");
        missing_tickers_placeholder.innerHTML = "";
        for (const selection of Object.entries(active_highlights)) {
            const selected_graph = selection[0];
            const selected_values = selection[1];
            var highlighted_values = highlights[selected_graph];
            if (highlighted_values == undefined){
                highlighted_values = {};
            };
            highlighted_values = {...highlighted_values, ...selected_values};
            highlights[selected_graph] = highlighted_values
        };
        request_filter(highlights);
    """

    details_buttons: str = """
        const ticker = cb_obj.labels[cb_obj.active];
        request_details(ticker);
    """

    read_table_rows = """
            function get_collection_fields(rows) {
            var collection_fields = {};
            for (var row_index = 2; row_index < rows.length; row_index++){
                const row = rows[row_index]; 
                const cells = row.children;
                const editable_cell = cells[1];
                const initial_value = editable_cell.textContent;
                var active_value = editable_cell.children[0].value;
                if (initial_value != active_value){
                    const field = cells[0].textContent;
                    active_value = active_value.replaceAll('"s', 's').replaceAll("'s", 's').replaceAll("'", '"')
                    try {active_value = JSON.parse(active_value);} 
                    catch (ex) {
                        if(!ex.message.includes("JSON")){
                            throw ex;
                        }
                        console.log(ex.message);
                    }
                    finally {collection_fields[field] = active_value;}
                };
            };
            return collection_fields;
        }
    """

    read_ticker_details_from_table = """
        const tables = document.getElementsByTagName("table");
        var ticker_fields = {};
        for (var table of tables){
            const collection = table.caption.textContent;
            var rows = table.tBodies[0].getElementsByTagName("tr");
            const collection_fields = get_collection_fields(rows);
            if (Object.keys(collection_fields).length > 0){
                collection_fields["_id"] = rows[1].children[1].textContent;
                ticker_fields[collection] = collection_fields;
            };
        };
    """

    update_button = f"""
        {read_table_rows}
        {read_ticker_details_from_table}
        request_update(ticker_fields);
    """

    disable_all_excel_buttons = """
        const excel_buttons = document.getElementsByClassName("excel_button");
        for (var button_div of excel_buttons){
            var button = button_div.getElementsByTagName("button")[0];
            button.disabled = true;
        };
    """

    resource_excel_button = f"""
        {disable_all_excel_buttons}
        request_excel(resource_name, representation);
    """

    details_excel_button = f"""
        {disable_all_excel_buttons}
        details = representation;
        request_details_excel();
    """
