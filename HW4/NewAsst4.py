import os
import dash
import numpy                as      np
import pandas               as      pd
import dash_core_components as      dcc
import dash_html_components as      html
import plotly.graph_objs    as      go
from   dash.dependencies    import  Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

CSV_URL     = 'https://data.cityofnewyork.us/resource/uvpi-gqnh.json'
CSV_PATH    = 'data.csv'

def get_options(df): 
    #Get all unique species, remove null entries
    species = df['spc_common'].unique()
    species = species[~pd.isnull(species)]

    return [
        {'label': x, 'value': x.replace(' ', '_')} for x in species
        ]

def get_columns(df):
    return [
        {'label': x, 'value': x} for x in df.columns
        ]

def create_layout(df):
    app.layout = html.Div([
        html.H1('Trees Health by species')                                  ,
        html.Label('Columns')                                               ,
        dcc.Dropdown(id = 'columns',
        options=get_columns(df),value=['boroname', 'health'],
        multi=True)                                                         ,
        html.Label('Max rows')                                              ,
        dcc.Input( value='10', id='n_rows')                                 ,
        html.Label('Species')                                               ,
        dcc.Dropdown( options=get_options(df), value='ash', id='species')   ,
        html.Div(id='content')                                              ])

def get_df():
    #If the data is already saved to disk
    if os.path.isfile(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    #If the data is not saved, download and save
    df = pd.read_json(CSV_URL)
    df.to_csv(CSV_PATH)
    return df

def get_stats(df, species):
    df_s = df[df['spc_common']== species.replace('_', ' ')]
    return df_s

def create_table(df, n_rows, columns):
    return html.Table(
        [html.Tr([html.Th(col) for col in columns]) ] +
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in columns
        ]) for i in range(min(len(df), n_rows))]
    )

def get_bars_values(df, species, col1, col2):
    df_s        = df[df['spc_common']== species]
    df_size     = df_s.groupby([col1, col2]).size()

    sizes_dict = {}
    for health in df_size.index.levels[0]:
        sizes_dict[health] = {
            'names' : [] ,
            'values': [] }
        for boro in df_size.index.levels[1]:
            try :
                sizes_dict[health]['names'].append(boro)
                sizes_dict[health]['values'].append(df_size[health][boro])
            except:
                sizes_dict[health]['values'].append(0)
    return sizes_dict

def create_graph(sizes_dict, id, title):
    data = [
        go.Bar(
            x = sizes_dict[health]['names'],
            y = sizes_dict[health]['values'],
            name = health
            )
            for health in sizes_dict]
    return html.Div([
        dcc.Graph(id=id,figure=go.Figure(data=data,layout=go.Layout(barmode='group', title = title)))
        ])

df = get_df()

create_layout(df)

@app.callback(
    Output(component_id='content'   , component_property='children' ),
    [Input(component_id='species'   , component_property='value'),
    Input(component_id='n_rows'   , component_property='value'),
    Input(component_id='columns'   , component_property='value')]  )
def update_output_div(input_value,n_rows, columns, df= df):
    sizes_dict_health = get_bars_values(df, input_value.replace('_', ' '), 'health', 'boroname')
    sizes_dict_steward = get_bars_values(df, input_value.replace('_', ' '), 'steward', 'boroname')
    return html.Div([
        create_table(get_stats(df, input_value),int(n_rows), columns ),
        create_graph(sizes_dict_health  , 'plt_health'  , 'Health'),
        create_graph(sizes_dict_steward , 'plt_steward' , 'Steward')
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
