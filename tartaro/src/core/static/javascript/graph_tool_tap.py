class TapToolScripts:
    register_filter: str = """
            const cursor_y_axis = cb_data.geometries.y;
        const graph_data = cb_data.source.data;

        const selected_indexes = cb_data.source.selected.indices;
        const selected_indexes_labels = [];
        selected_indexes.forEach(index => selected_indexes_labels.push(graph_data.labels[index]))
        const last_selected_label = selected_indexes_labels[selected_indexes.length - 1];
        const last_selected_index = selected_indexes[selected_indexes.length - 1];
        const missing_percentage = graph_data.missing[last_selected_index];

        if (active_highlights[graph_name] == undefined){
            active_highlights[graph_name] = {};
        };
        const highlighted_labels = Object.getOwnPropertyNames(active_highlights[graph_name]);
        const obsolete_labels = highlighted_labels.filter(label => !selected_indexes_labels.includes(label));
        obsolete_labels.forEach(obsolete_label => delete active_highlights[graph_name][obsolete_label]);

        active_highlights[graph_name][last_selected_label] = cursor_y_axis > missing_percentage;
    """

    show_filter: str = """
        const graph_filters_place_holder = document.getElementById("graph_filters_place_holder");
        debug_here();
        var graph_filter = "";
        for (const selection of Object.entries(active_highlights)) {
            const selected_graph = selection[0];
            const selected_values = selection[1];
            graph_filter += "Of " + selected_graph + ":";
            for (const values_selection of Object.entries(selected_values)) {
                const field = values_selection[0];
                const exists = values_selection[1];
                graph_filter += " " + field + " ";
                if (exists) {
                    graph_filter += "covered";
                } else {
                    graph_filter += "missing";
                }
            }
            graph_filter += "; ";
        }
        graph_filters_place_holder.innerHTML = graph_filter;
    """

    show_sample: str = """
        const sample_tickers = tickers_sample[last_selected_label];

        const covered_tickers = sample_tickers.covered;
        const covered_tickers_placeholder = document.getElementById("covered_tickers");
        covered_tickers_placeholder.innerHTML = covered_tickers;

        const missing_tickers = sample_tickers.missing;
        const missing_tickers_placeholder = document.getElementById("missing_tickers");
        missing_tickers_placeholder.innerHTML = missing_tickers;

        const tickers_samples = document.getElementById("tickers_samples");
        Array.from(tickers_samples.querySelectorAll("script")).forEach( oldScript => {
            const newScript = document.createElement("script");
            Array.from(oldScript.attributes).forEach( attr => newScript.setAttribute(attr.name, attr.value) );
            newScript.appendChild(document.createTextNode(oldScript.innerHTML));
            oldScript.parentNode.replaceChild(newScript, oldScript);
        });
    """

    select_sample: str = register_filter + show_filter + show_sample

