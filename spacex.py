import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt
import os
import calendar
#Create app
app = dash.Dash(__name__)
# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
if 'spacex.csv' in os.listdir():
    df = pd.read_csv('spacex.csv')
else:
# Read the wildfire data into pandas dataframe
    df =  pd.read_csv(URL)
    df.to_csv('spacex.csv')

#Layout Section of Dash
#TASK 2.1: Create a Dash application and give it a meaningful title
app.layout = html.Div(
    children=[
        html.H1('SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
# #           #Dropdown to select site
            html.Div([
                    dcc.Dropdown(id='site-dropdown', 
                        options=[{'label': i, 'value': i} for i in list(df['Launch Site'].unique())],
                        value='ALL',
                        placeholder='All Sites')
            ]),
            html.Div([
                html.Div(id='success-pie-chart', className='chart-grid', style={'display': 'flex'}),
            ]),
            html.Div([
                        dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       2500: '2500',
                       5000: '5000',
                       7500: '7500'
                       },
                value=[0, 10000])
                    ], style={'display': 'in-line-box'}
            ),
            html.Div([
                html.Div(id='success-payload-scatter-chart', className='chart-grid', style={'display': 'flex'}),
            ])
        ])
# #Second Inner division for adding 2 inner divisions for 2 output graphs
# #TASK 2.3: Add two empty divisions for output inside the next inner division.
    # ])
#     #outer division ends
# ])
#layout ends
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
            names='Launch Site', 
            title='Total Success Launches by Site')
        return [
            html.Div(className='chart-item', children=[
                html.Div(children=fig),
                ], style={'display': 'inline-box'})
            ]
    else:
        filtered_df = df[df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, values='class',
                     names='Launch Site', 
        title='Total Success Launches by Site')
        return [
            html.Div(className='chart-item', children=[
                html.Div(children=fig),
                ], style={'display': 'inline-box'})
            ]

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
        [Input(component_id='site-dropdown', component_property='value'), 
         Input(component_id="payload-slider", component_property="value")])
def get_payload_chart(site, payload):
    if site == 'ALL':
        fig = px.scatter(
            f_df, 
            x='Payload_Mass', 
            y='Class', 
            title='Correlation between Payload and Success for All Sites', 
            color="Booster Version Category")
        return [
            html.Div(className='chart-item', children=[
                html.Div(children=fig),
                ], style={'display': 'inline-box'})
            ]
    else:
        f_df = df[(['Launch Site'] == site) & (['Payload_Mass'] == payload)]
        fig = px.scatter(
            f_df, 
            x='Payload_Mass', 
            y='Class', 
            title='Correlation between Payload and Success for {} Sites'.format(site), 
            color="Booster Version Category")
        return [
            html.Div(className='chart-item', children=[
                html.Div(children=fig),
                ], style={'display': 'inline-box'})
            ]
if __name__ == '__main__':
    app.run_server()