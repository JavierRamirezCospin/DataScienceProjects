import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from dash import no_update
from pyrsistent import v

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

supermaket_data = pd.read_csv('SupermarketData.csv')

app.layout = html.Div(children=[
    html.H1('Supermarket Statistics by Product Type',
            style={'textAlign': 'center','color': '#503D36','font-size':50,'font-wight':'bold'}
    ),
    html.Div([
        html.Div(
            html.H2('Year Range',style={'margin-right':'2em'})
        ),
        dcc.Dropdown(id='producttype-dropdown',
            options=[
                {'label':'Fashion accessories','value':'cat1'},
                {'label':'Food and beverages','value':'cat2'},
                {'label':'Electronic accessories','value':'cat3'},
                {'label':'Sports and travel','value':'cat4'},
                {'label':'Home and lifestyle','value':'cat5'},
                {'label':'Health and beauty','value':'cat6'}
            ],
            value='cat1'
        ),
        html.Div([
            html.Div([],id="plot1",style={'display':'inline-block','width':'48%'}),
            html.Div([],id="plot2",style={'display':'inline-block','width':'48%'})
            ],style={'display':'flex'}
        ),
        html.Div([
            html.Div([],id="plot3",style={'display':'inline-block','width':'48%'}),
            html.Div([],id="plot4",style={'display':'inline-block','width':'48%'})
            ],style={'display':'flex'}
        ),
        html.Div([
            html.Div([],id="plot5",style={'display':'inline-block','width':'48%'}),
            html.Div([],id="plot6",style={'display':'inline-block','width':'48%'})
            ],style={'display':'flex'}
        )
    ])
])

@app.callback([Output(component_id='plot1',component_property='children'),
                Output(component_id='plot2',component_property='children'),
                Output(component_id='plot3',component_property='children'),
                Output(component_id='plot4',component_property='children'),
                Output(component_id='plot5',component_property='children'),
                Output(component_id='plot6',component_property='children')],
                Input(component_id='producttype-dropdown',component_property='value')
)
def display_supermarket_charts(value):
    if value == 'cat1': category = "Fashion accessories"
    elif value == 'cat2': category = "Food and beverages"
    elif value == 'cat3': category = "Electronic accessories"
    elif value == 'cat4': category = "Sports and travel"
    elif value == 'cat5': category = "Home and lifestyle"
    else: category = "Health and beauty"
    # Main df
    df = supermaket_data[supermaket_data['Product line'] == category]
    # Customer gender Pie
    genders = df['Gender'].value_counts()
    genders.sort_index(inplace=True)
    gendersfig = go.Figure(data=[go.Pie(labels=genders.index,values=genders,hole=0.35,
                                        sort=False,marker=dict(colors=['#FF4D4D','#4D94FF']))])
    gendersfig.update_layout(title=dict(text="Customer gender proportion",x=0.5))
    # Customer type Pie
    ctypes = df['Customer type'].value_counts()
    ctypes.sort_index(inplace=True)
    ctypesfig = go.Figure(data=[go.Pie(labels=ctypes.index,values=ctypes,hole=0.35,
                                        sort=False,marker=dict(colors=['#4DFFA6','#FFB84D']))])
    ctypesfig.update_layout(title=dict(text="Customer type proportion",x=0.5))
    # Total Boxplot
    totalfig = go.Figure(data=[go.Box(y=df['Total'],marker_color='#996633')])
    totalfig.update_layout(title=dict(text="Total Boxplot",x=0.5))
    # Income Boxplot
    incomefig = go.Figure(data=[go.Box(y=df['gross income'],marker_color='#D24DFF')])
    incomefig.update_layout(title=dict(text="Gross income boxplot",x=0.5))
    # Quantity Bar graph
    quantities = df['Quantity'].value_counts()
    quantities.sort_index(inplace=True)
    quantitiesfig = go.Figure(data=[go.Bar(x=list(map(str,quantities.index)),y=quantities,marker_color="#70DBDB")])
    quantitiesfig.update_layout(title=dict(text="Quantity frequencies",x=0.5))
    # Ratings Bar graph
    labels = ["4 - 4.9","5.0 - 5.9","6.0 - 6.9","7.0 - 7.9","8.0 - 8.9","9.0 - 10.0"]
    ratings_dict = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0}
    df_ratings = np.asarray(df['Rating'])
    for rating in df_ratings:
        if 4.0 <= float(rating) <= 4.9: ratings_dict['1'] += 1
        elif 5.0 <= float(rating) <= 5.9: ratings_dict['2'] += 1
        elif 6.0 <= float(rating) <= 6.9: ratings_dict['3'] += 1
        elif 7.0 <= float(rating) <= 7.9: ratings_dict['4'] += 1
        elif 8.0 <= float(rating) <= 8.9: ratings_dict['5'] += 1
        else: ratings_dict['6'] += 1
    ratings = list(ratings_dict.values())
    ratingsfig = go.Figure(data=[go.Bar(x=labels,y=ratings,marker_color='#A6A6A6')])
    ratingsfig.update_layout(title=dict(text="Rating frequencies",x=0.5),font=dict())
    # Returning charts
    return [dcc.Graph(figure=gendersfig),
            dcc.Graph(figure=ctypesfig),
            dcc.Graph(figure=totalfig),
            dcc.Graph(figure=incomefig),
            dcc.Graph(figure=quantitiesfig),
            dcc.Graph(figure=ratingsfig)]

if __name__ == '__main__':
    app.run_server()