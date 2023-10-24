import branca
import folium
import geopandas as gpd
import numpy as np
import pandas as pd
import streamlit as st
from branca.element import MacroElement, Template

from utils import float_format, format, monetize, percentize


def create_choropleth(data, target_variable, geom_granularity, folium_layer_name="my_choropleth", legend_title="my_legend_title", legend_subtitle="", n_bins=6, formatting=None, reference_variable=None, scaler='linear', power=None, cbsa_internal_points=None, flip_color_scale=False):
    """
    Generates an interactive choropleth (Folium Map Object) with the intensity of color determined by "target_variable"

    Parameters
    ----------
    data : geopandas.DataFrame
        Geopandas Dataframe containing the numerical variable used to color the choropleth, 
        and a geometry column named "geom" corresponding to polygons for the map

    target_variable : str
        Column name of Geopandas Dataframe of type float or int

    geom_granularity : str
        A string specifying whether to use ZCTA or CBSA for choropleth

    folium_layer_name : str, default 'my_choropleth'
        Label used for the Layer Control of Folium Map Object

    legend_title : str, default 'my_legend_title'
        Title for Draggable Legend

    legend_subtitle : str, default 'my_legend_subtitle'
        Title for Draggable Legend

    n_bins : int, default 6
        Number of bins / colors used to create the choropleth

    formatting : str, default None
        Defines the formatting function to use for Map Legend and Map Popups. Can be either None, `percent`, `float`, or `dollar`

    reference_variable : str, default None
        An optional reference variable to include in the Map Popup, usually to help understand the KPI being displayed

    scaler : str, default 'linear'
        The type of scaler to use when defining bins for the Choropleth. Can be either `linear`, `log`, or `power`

    power : float, default None
        Can only be used when `scaler == 'power'`. The power which you raise the data to when using the `power` scaler.

    cbsa_internal_points : list
        A list of single pair of Latitude and Longitude. Can only be used when `geom_granularity == 'ZCTA'`. Sets the `folium.Map` location and zoom_start to the center of the selected CBSA

    Returns
    -------
    folium.folium.Map
        Returns a Folium Map Object that can be further customized.
    """
    if geom_granularity == "ZCTAs":
        m = folium.Map(location=cbsa_internal_points,
                       zoom_start=9, tiles='CartoDB positron', scrollWheelZoom=False)
    else:
        # Base Map centered on USA
        m = folium.Map(location=[37.8, -96],
                       zoom_start=5, tiles='CartoDB positron', scrollWheelZoom=False)

    # Color Scale
    if scaler == 'linear':
        colormap = branca.colormap.LinearColormap(
            vmin=data[target_variable].quantile(0.0),
            vmax=data[target_variable].quantile(1),
            colors=["#990000", "#fff7ec"] if flip_color_scale == True else [
                "#fff7ec", "#990000"],
        ).to_step(n=n_bins)
    elif scaler == 'log':
        if data[target_variable].quantile(0.0) <= 0:
            st.error(
                "Log-scale works only with strictly positive values, choose another scaling method")
            st.stop()
        colormap = branca.colormap.LinearColormap(
            vmin=data[target_variable].quantile(0.0),
            vmax=data[target_variable].quantile(1),
            colors=["#990000", "#fff7ec"] if flip_color_scale == True else [
                "#fff7ec", "#990000"],
        ).to_step(n=n_bins)
        # Scale the numeric variable however you'd like
        scaled_colormap = [np.log(x) for x in colormap.index]
        # Apply the scaling to the colormap
        colormap = colormap.scale(
            vmin=min(scaled_colormap), vmax=max(scaled_colormap))
    elif scaler == 'power':
        if (data[target_variable].quantile(0.0) <= 0 and power % 1 != 0):
            st.error("Power must be an integer >= 1 when dealing with negative numbers, choose another scaling method (Root of negative number is imaginary)")
            st.stop()
        colormap = branca.colormap.LinearColormap(
            vmin=data[target_variable].quantile(0.0),
            vmax=data[target_variable].quantile(1),
            colors=["#990000", "#fff7ec"] if flip_color_scale == True else [
                "#fff7ec", "#990000"],
        ).to_step(n=n_bins)
        # Scale the numeric variable however you'd like
        scaled_colormap = [x**power for x in colormap.index]
        if (np.inf in scaled_colormap or np.NINF in scaled_colormap):
            st.error(
                "Scaling led to Inifite or Negative Inifinite value. Try another power, or use another scaler")
            st.stop()
        # Apply the scaling to the colormap
        colormap = colormap.scale(
            vmin=min(scaled_colormap), vmax=max(scaled_colormap))
    hex_colors = [colormap.rgb_hex_str(x) for x in colormap.index]
    hex_colors[0] = '#d9d9d9'
    # Polygon Style Function

    def style_function(x): return {
        "fillColor": colormap(x["properties"][target_variable])
        if (x["properties"][target_variable] != 0 and x["properties"][target_variable] is not None)
        else "#d9d9d9",
        "color": "black",
        'weight': 2,
        "fillOpacity": 0.8,
    }
    # Polygon Hover Highlight Function

    def highlight_function(x): return {'fillColor': '#000000',
                                       'color': '#000000',
                                       'fillOpacity': 0.50,
                                       'weight': 0.1}
    if formatting == None:
        format(data, data.drop(columns=["geom"]).columns.values)
        formatted_cols = [col for col in data.columns if '_formatted' in col]
    elif formatting == 'float':
        if reference_variable is not None:
            float_format(data, data.drop(
                columns=["geom", reference_variable]).columns.values)
            format(data, [reference_variable])
        else:
            float_format(data, data.drop(columns=["geom"]).columns.values)
        formatted_cols = [col for col in data.columns if '_formatted' in col]
    elif formatting == 'dollar':
        if reference_variable is not None:
            monetize(data, data.drop(
                columns=["geom", reference_variable]).columns.values)
            format(data, [reference_variable])
        else:
            monetize(data, data.drop(columns=["geom"]).columns.values)
        formatted_cols = [col for col in data.columns if '_formatted' in col]
    elif formatting == 'percent':
        if reference_variable is not None:
            percentize(data, data.drop(
                columns=["geom", reference_variable]).columns.values)
            format(data, [reference_variable])
        else:
            percentize(data, data.drop(columns=["geom"]).columns.values)
        formatted_cols = [col for col in data.columns if '_formatted' in col]
    folium.GeoJson(
        data=data,
        style_function=style_function,
        highlight_function=highlight_function,
        name=f"{folium_layer_name} by {geom_granularity}",
        overlay=True,
        control=True,
        show=True,
        smooth_factor=None,
        #    zoom_on_click= True,
        tooltip=folium.features.GeoJsonTooltip(
            fields=formatted_cols,
            aliases=[x.replace("_formatted", "").replace(
                "_", " ").title() for x in formatted_cols],
            style="""
            border: 2px solid black;
            border-radius: 2px,
            """,
        ),
        popup=folium.features.GeoJsonPopup(
            fields=formatted_cols,
            aliases=[x.replace("_formatted", "").replace(
                "_", " ").title() for x in formatted_cols],
            style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 2px,
            box-shadow: 3px;
            """,
        )
    ).add_to(m)
    ####################################### Adding in Legend #######################################
    # Set up Legend Bins

    def set_bins():
        if formatting == 'float':
            bins = [round(x, 2) for x in colormap.index]
        else:
            bins = [int(x) for x in colormap.index]
        return bins
    bins = set_bins()
    # Generate a n length <li> element for the legend html
    legend_text = []
    for i in range(1, n_bins+1):
        if formatting == 'dollar':
            legend_text.append("""<li><span style='background:""" +
                               f"{hex_colors[i]}" + """;opacity:0.8;'></span>""" + f"$ {bins[i-1]:,.2f}" + """ to """ + f"$ {bins[i]:,.2f}" + """</li>""")
        elif formatting == 'percent':
            legend_text.append("""<li><span style='background:""" +
                               f"{hex_colors[i]}" + """;opacity:0.8;'></span>""" + f"{bins[i-1]:,.2f} %" + """ to """ + f"{bins[i]:,.2f} %" + """</li>""")
        else:
            legend_text.append("""<li><span style='background:""" +
                               f"{hex_colors[i]}" + """;opacity:0.8;'></span>""" + f"{bins[i-1]:,}" + """ to """ + f"{bins[i]:,}" + """</li>""")
    legend_text = ''.join(legend_text)
    template = """
    {% macro html(this, kwargs) %}

    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>jQuery UI Draggable - Default functionality</title>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    
    <script>
    $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });

    </script>
    </head>
    <body>
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
        border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
        
    <div class='legend-title'>""" + f"{legend_title}" + """</div>
    <div class='legend-sub-title'>""" + f"{legend_subtitle}" + """</div>
    <div class='legend-scale'>
    <ul class='legend-labels', style="font-weight: bold;">
    <li><span style='background:""" + f"{hex_colors[0]}" + """;opacity:0.8;'></span>""" + f"{0 if len(data[data[target_variable].isnull()]) == 0  else 'Not Applicable' }" + """</li>
        """ + legend_text + """
    </ul>
    </div>
    </div>
    </body>
    </html>
    <style type='text/css'>
    .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
    .maplegend .legend-sub-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 80%;
        }
    .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
    .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
    .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
    .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
    .maplegend a {
        color: #777;
        }
    </style>
    {% endmacro %}"""

    macro = MacroElement()
    macro._template = Template(template)
    m.add_child(macro)
    return m
