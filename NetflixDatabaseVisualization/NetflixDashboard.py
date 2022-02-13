import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from dash import no_update

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

netflix_data = pd.read_csv('NetflixCleanData.csv')

app.layout = html.Div(children=[
    html.H1('Netflix Statistics by Year Range',
            style={'textAlign': 'center','color': '#503D36','font-size':45}),
    html.Div([
        html.Div(
            html.H2('Year Range',style={'margin-right':'2em'})
        ),
        dcc.Dropdown(id='yearrange-dropdown',
            options=[
                {'label':'1936 - 1945','value':'cat1'},
                {'label':'1946 - 1955','value':'cat2'},
                {'label':'1956 - 1965','value':'cat3'},
                {'label':'1966 - 1975','value':'cat4'},
                {'label':'1976 - 1985','value':'cat5'},
                {'label':'1986 - 1995','value':'cat6'},
                {'label':'1996 - 2005','value':'cat7'},
                {'label':'2006 - 2015','value':'cat8'},
                {'label':'2016 - 2021','value':'cat9'}
            ],
            value='cat1'
        ),
        html.Div([
            html.Div([],id='plot1'),
            html.Div([],id='plot2')        
        ],style={'display':'flex'}
        ),
        html.Div([
            html.Div([],id='plot3'),
            html.Div([],id='plot4')
        ],style={'display':'flex'})
    ])
])

@app.callback([
    Output(component_id='plot1',component_property='children'),
    Output(component_id='plot2',component_property='children'),
    Output(component_id='plot3',component_property='children'),
    Output(component_id='plot4',component_property='children')],
    Input(component_id='yearrange-dropdown',component_property='value')
)
def display_netflix_yearly_charts(value):
    # main df
    if value == 'cat1': years = [1936,1945]
    elif value == 'cat2': years = [1946,1955]
    elif value == 'cat3': years = [1956,1965]
    elif value == 'cat4': years = [1966,1975]
    elif value == 'cat5': years = [1976,1985]
    elif value == 'cat6': years = [1986,1995]
    elif value == 'cat7': years = [1996,2005]
    elif value == 'cat8': years = [2006,2015]
    else: years = [2016,2021]
    df = netflix_data[(netflix_data['release_year'] >= years[0]) & (netflix_data['release_year'] <= years[1])]
    # Movies vs TV Shows
    netflix_types = df['type'].value_counts()
    typesfig = go.Figure(data=[go.Pie(labels=netflix_types.index,values=netflix_types,hole=0.3,pull=[0.0,0.2])])
    typesfig.update_layout(
        title={'text':'Movies vs TV Shows Proportion','x':0.5,'xanchor':'center'}
    )
    typesfig.update_traces(
        marker=dict(colors=['#316395','#B82E2E'])
    )
    # Top 10 countries of origin
    df_top_countries = df['country'].value_counts(ascending=False).head(10)
    countriesfig = go.Figure(data=[go.Bar(x=df_top_countries.index,y=df_top_countries,marker_color='#FFA15A')])
    countriesfig.update_layout(
        title={'text':'Top countries of origin','x':0.5,'xanchor':'center'}
    )
    # Releases per year
    df_years_releases = df['release_year'].value_counts()
    yearsfig = go.Figure(data=[go.Bar(x=list(map(str,df_years_releases.index)),y=df_years_releases,marker_color="#66AA00")])
    yearsfig.update_layout(
        title={'text':'Top years by number of releases','x':0.5,'xanchor':'center'}
    )
    # Top categories
    df_categories = np.asarray(df['categories'])
    categories_dict = {}
    for category in df_categories:
        categories = category.split(", ")
        for cat in categories:
            if cat in categories_dict.keys(): categories_dict[cat] = categories_dict[cat] + 1
            else: categories_dict[cat] = 1
    categories_dict = sorted(categories_dict.items(),key=lambda x:x[1])
    sorted_categories_dict = dict(categories_dict)
    categories_series = pd.Series([x for x in sorted_categories_dict.values()],
                              index=[x for x in sorted_categories_dict.keys()])
    categories_series = categories_series[:10]
    categoriesfig = go.Figure(data=[go.Bar(x=categories_series.index,y=categories_series,marker_color='#7F7F7F')])
    categoriesfig.update_layout(
        title={'text':'Top 10 categories','x':0.5,'xanchor':'center'}
    )

    return [dcc.Graph(figure=typesfig),
            dcc.Graph(figure=countriesfig),
            dcc.Graph(figure=yearsfig),
            dcc.Graph(figure=categoriesfig)]

if __name__ == '__main__':
    app.run_server()
