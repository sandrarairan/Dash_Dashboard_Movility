import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_table
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#ece2e1',
    'text': '#161d6f'
}

##############################################################
        #DATA MANIPULATION (MODEL)
##############################################################

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



# this is needed for the procfile to deploy to heroku
server = app.server

df = pd.read_excel("/Users/sandrarairan/Documents/desarrollo/dash_mobility/movilidad.xlsx", engine='openpyxl')

df_table = df.groupby(['Ciudad', 'dFlag']).agg({'Viajes_std':'size', 'Viajes_lab':'size', 'Viajes_tr':'size'}).reset_index()

fig = px.scatter_matrix(df,
    dimensions=["Viajes_std", "Viajes_tr", "Viajes_lab"],
    color="dFlag")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

#fig = px.bar(df, x="Ciudad", y="Tiempo1", color="Transporte1", barmode="group")


##############################################################
        #DATA LAYOUT (VIEW)
##############################################################



app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Dash: A web application - Transport Area Metropolitan Medellín.',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    dcc.Graph(
        id='bar',
        figure=fig
    ),
    html.Div(children='Tabla - Ciudad y dFlag y calcula la cantidad de Viajes_std, Viajes_lab, Viajes_tr', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df_table.columns],
    data=df_table.to_dict('records'),
    editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
)
])



if __name__ == '__main__':
    app.run_server(debug=True)