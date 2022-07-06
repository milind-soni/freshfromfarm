import pandas as pd 
import numpy as np 
import dash 
import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.dash_table.Format import Group

import plotly.offline as py     #(version 4.4.1)
import plotly.graph_objs as go


mapbox_access_token = 'pk.eyJ1IjoibWlsaW5kc29uaSIsImEiOiJjbDRjc2ZxaTgwMW5hM3Bqbmlka3VweWVkIn0.AM0QzfbGzUZc04vZ6o2uaw'


df = pd.read_csv("profiling2.csv")

app = dash.Dash(__name__)

blackbold={'color':'black', 'font-weight': 'bold'}

sku_list = ["Apple", "Banana", "Mango"]
quality_list = ["A","B","C"]

app.layout = html.Div([
#---------------------------------------------------------------
# Map_legen + Borough_checklist + Recycling_type_checklist + Web_link + Map
    html.Div([
        html.Div([
            # Map-legend

            html.Ul([
                html.Div(
                    html.Img(src = app.get_asset_url('fff.webp')))
               
            ], style={'border-bottom': 'solid 3px', 'border-color':'#00FC87','padding-top': '6px'}
            ),

            # Borough_checklist
            html.Label(children=['SKU: '], style=blackbold),
            dcc.Checklist(id='boro_name',
                    options=[{'label':str(b),'value':b} for b in sku_list],
                    value=[b for b in sku_list],
            ),
            html.Label(children=['Quality Index: '], style=blackbold),
            dcc.Checklist(id='quality',
                    options=[{'label':str(b),'value':b} for b in sorted(df['quality'].unique())],
                    value=[b for b in sorted(df['quality'].unique())],
            ),
     
            # # Recycling_type_checklist
            # html.Label(children=['Quality Index '], style=blackbold),
            # dcc.Checklist(id='recycling_type',
            #         options=[{'label':str(b),'value':b} for b in quality_list],
            #         value=[b for b in quality_list],
            # ),

            html.Label(children=['Sales Exec Name: '], style=blackbold),
            dcc.Checklist(id='sales_exec',
                    options=[{'label':str(b),'value':b} for b in sorted(df['Sales Exec Name'].unique())],
                    value=[b for b in sorted(df['Sales Exec Name'].unique())],
            ),
           

        ], className='three columns'
        ),

        # Map
        html.Div([
            dcc.Graph(id='graph', config={'displayModeBar': False, 'scrollZoom': True},
                style={'background':'#00FC87','padding-bottom':'2px','padding-left':'2px','height':'100vh'}
            )
        ], className='nine columns'
        ),

    ], className='row'
    ),

], className='ten columns offset-by-one'
)


# Output of Graph
@app.callback(Output('graph', 'figure'),
              [Input('quality', 'value'),
              Input('sales_exec','value')])



def update_figure(chosen_quality,chosen_exec):
    df_sub = df[(df['quality'].isin(chosen_quality)) &
            (df['Sales Exec Name'].isin(chosen_exec))]

    # Create figure
    locations=[go.Scattermapbox(
                    lon = df_sub['Longitude'],
                    lat = df_sub['Latitude'],
                    mode='markers',
                    marker={'color' :df_sub['Color']  , 'size' : 2*df['Total'] },
                    unselected={'marker' : {'opacity':1}},
                    selected={'marker' : {'opacity':0.5, 'size':100}},
                    hoverinfo='text',
                    hovertext=df_sub['hov_text']
    )]


    return {
        'data': locations,
        'layout': go.Layout(
            uirevision= 'foo', #preserves state of figure/map after callback activated
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=2,
            title=dict(text="Dashboard",font=dict(size=50, color='green')),
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=25,
                style='streets',
                center=dict(
                     
                    lat=28.636534588228688,
                    lon=77.26948797090003
                ),
                pitch=40,
                zoom=11.5
            ),
        )
    }


if __name__ == '__main__':
    app.run(debug=True)
