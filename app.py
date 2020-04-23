#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output 
import plotly.graph_objects as go
import pandas as pd
import dash_auth
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import plotly.express as px
import numpy as np


# In[2]:


colors = {'background': '#F5F1EC',
          'text': '#AC1C26',
          'cluster': ['rgb(171, 33, 43)',  # Red
                     'rgb(41, 128, 110)',  # green
                     'rgb(247, 183, 47)',  # yellow
                     'rgb(51, 170, 191)'  # lightblue
                     ]}

color_gradient = [['rgb(171, 33, 43)','rgb(194, 90, 82)','rgb(212, 135, 122)','rgb(171, 33, 160)'],
                ['rgb(41, 128, 110)','rgb(89, 151, 137)','rgb(137, 179, 170)','rgb(41, 128, 230)',],
                 ['rgb(247, 183, 47)','rgb(252, 203, 131)','rgb(225, 228, 192)','rgb(247, 183, 167)'],
                 ['rgb(51, 170, 191)','rgb(124, 191, 209)','rgb(177, 216, 226)','rgb(51, 170, 130)',]]

font_title = {'family':'Arial black','size':12,'color' : colors['text']}

link_logo = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTnxaeiaqzS5cmEthawZyB79MJtsY8lKOBo9fIKcvCy1tgHF-x4&usqp=CAU'

tabs_styles = {'height': '30px','font-size':12}


# In[22]:


url = 'https://raw.githubusercontent.com/ariformi/overview-dash/master/Dashboard.csv'


# In[23]:


df = pd.read_csv(url, sep="[;]", engine='python')
df.Day = pd.to_datetime(df.Day, format = "%d/%m/%y")
df.Data = pd.to_datetime(df.Data , format = "%d/%m/%y")
df.head()


# In[15]:


fig_clicks = go.Figure(data=[
    go.Bar(name='Budget FB & IG', x=df.Data, y=df['Budget FB/IG (sec. axis)']),
    go.Bar(name='Budget Google', x=df.Data, y=df['Budget GGL']),
    go.Scatter(name='Clicks FB/IG',x=df.Data, y= df['Click FB/IG'],mode='lines'),
    go.Scatter(name='Clicks GGL',x=df.Data, y= df['Click GGL'],mode='lines'),
    go.Scatter(name='Clicks overall',x=df.Data, y= df['Click overall'],mode='lines')
])
# Change the bar mode
fig_clicks.update_layout(barmode='stack')
fig_clicks.update_layout(template = 'plotly_white',
    title="Daily Clicks from different paid sources and relative budget",
    xaxis_title="Date",
    yaxis_title="Clicks & Budget in €",
    height = 600,
    width = 1100 )
fig_clicks.show()


# In[16]:


fig_sessions = go.Figure(data=[
    go.Bar(name='FB & IG', x=df[df.Source == 'Paid FB/IG'].Day, y=df[df.Source == 'Paid FB/IG']['Sessions per source']),
    go.Bar(name='Google', x=df[df.Source == 'Paid Google'].Day, y=df[df.Source == 'Paid Google']['Sessions per source']),
    go.Bar(name='Organic & Direct', x=df[df.Source == 'Organic-Direct source'].Day, y=df[df.Source == 'Organic-Direct source']['Sessions per source']),
    go.Bar(name='Referral', x=df[df.Source == 'Referral source'].Day, y=df[df.Source == 'Referral source']['Sessions per source']),
    go.Scatter(name='Tot Sessions',x=df[df.Source == 'Paid FB/IG'].Day, y= df.Sessions,mode='lines')
])
# Change the bar mode
fig_sessions.update_layout(barmode='stack')
fig_sessions.update_layout(template = 'plotly_white',
    title="Daily Sessions from different Sources",
    xaxis_title="Date",
    yaxis_title="Sessions",
    width = 1100 )
fig_sessions.show()


# In[6]:


fig_campaign =go.Figure(data=[
    go.Bar( x=df['Sessions from campaign'],y=df['Campaign'], orientation='h')])
# Change the bar mode
fig_campaign.update_layout(barmode='stack')
fig_campaign.update_layout(template = 'plotly_white',
    title="Number of sessions from different campaigns",
    xaxis_title="Sessions",
    yaxis_title="Campaigns",
    width = 1100 )
fig_campaign.show()


# In[7]:


fig_product =go.Figure(data=[
    go.Bar( x=df['Pageviews'],y=df['Product Pages'], orientation='h')])
# Change the bar mode
fig_product.update_layout(barmode='stack')
fig_product.update_layout(template = 'plotly_white',
    title="Number of pageviews from different campaigns",
    xaxis_title="Pageviews",
    yaxis_title="Product page",
    height = 680,
    width = 1100)
fig_product.show()


# In[8]:


fig_orders =go.Figure(data=[
    go.Bar(name= 'Total Orders', x=df['Data'],y=df['Total Orders']),
    go.Bar(name= 'Orders from FB/IG adv',x=df['Data'],y=df['Orders from campaigns'])])
# Change the bar mode
fig_orders.update_layout(barmode='group')
fig_orders.update_layout(template = 'plotly_white',
    title="Number of orders completed daily",
    xaxis_title="Date",
    yaxis_title="Orders",
    width = 1100)
fig_orders.show()


# In[9]:


convertion_rate_tot= df['Total Orders']/df['Sessions shop (all areas, GA)']
convertion_rate_fbig= df['Orders from campaigns']/df['Paid sessions shop overall (utm)']


# In[10]:


fig_convertion = go.Figure(data=[
    go.Scatter(name='Convertion tot',x=df.Data, y= convertion_rate_tot,mode='lines'),
    go.Scatter(name='Convertion FB/IG',x=df.Data, y= convertion_rate_fbig,mode='lines')
])
# Change the bar mode
fig_convertion.update_layout(template = 'plotly_white',
    title="Convertion Rate Daily",
    xaxis_title="Date",
    yaxis_title="Convertion Rate",
    width = 1100 )
fig_convertion.show()


# In[17]:


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([
            
                    dbc.Row([
                        dbc.Col(html.H1(children='OVERVIEW BOTTEGA',
                                style={'font-size': 20})),
                        
                        dbc.Col(html.Img(src=link_logo, width=130,
                                 style = {'float': 'right','margin-top':-15}))
                            ]),
            dcc.Tabs([
                dcc.Tab(label='Traffic', children=[
                    dbc.Row([dcc.Graph(id='click', figure=fig_clicks),
                    ],style={'margin-top': 50}),
                    
                    dbc.Row([dcc.Graph(id='advspending',figure = fig_sessions)    
                    ],style={'margin-top': 50})
                    ]),
                        
                dcc.Tab(label='Campaigns', children=[
                    dbc.Row([dcc.Graph(id='campaign', figure=fig_campaign),
                    ],style={'margin-top': 50}),
                    ]),
                
                dcc.Tab(label='Product Pages', children=[
                    dbc.Row([dcc.Graph(id='product', figure=fig_product),
                    ],style={'margin-top': 50})]),
                
                dcc.Tab(label='Convertion', children=[
                    dbc.Row([dcc.Graph(id='orders', figure=fig_orders),
                    ],style={'margin-top': 50}),
                dbc.Row([dcc.Graph(id='convertion', figure=fig_convertion),
                    ])])
                
                ],style = tabs_styles)
    
],style={'color': colors['text'],'margin': 20,'font-family': 'Arial black'})



if __name__ == '__main__':
        app.run_server(debug=True,use_reloader=False)


# In[ ]:




