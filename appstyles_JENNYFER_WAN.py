import os
from urllib.request import urlopen
import json

import pandas as pd 
import numpy as np

import plotly.express as px
import plotly.graph_objects as go


from dash import Dash, html, dash_table, dcc, callback, Output, Input 

##_______________________________________________________________

# Ajouter cette importation dans les importations en haut
external_stylesheets = ['https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css']

# Modifier l'initialisation de l'application pour utiliser les feuilles de style externes
app = Dash(__name__, external_stylesheets=external_stylesheets)

##_______________________________________________________________

with urlopen('https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson') as response:
    france_departments = json.load(response)

# Load merge.csv into a DataFrame
df = pd.read_csv('merged.csv', delimiter=";")

# Display the first few rows of the DataFrame to inspect the data
df.head()

##_______________________________________________________________

# Rename columns as desired
df = df.rename(columns={
    'sexe': 'Sexe',
    'preusuel': 'Prenom',
    'annais': 'Annee',
    'dpt': 'Departement',
    'nombre': 'Nombre'
})

def rename_sexe(value):
    if value == 1:
        value = "Man"
        return value
    elif value == 2:
        value = "Woman"
        return value
    else:
        return value
    
df['sexeName'] = df.Sexe.apply(rename_sexe)

# Add a zero in front of departments from 1 to 9.
df['Departement'] = df['Departement'].apply(lambda x: f"{int(x):02}")

##_______________________________________________________________

# App layout
app.layout = html.Div([
    html.Div(
        children=[html.H1("France First Name Dashboard", className="text-center font-bold text-red-600 text-3xl")],
        className="p-4 bg-gray-200 border border-black"
    ),
    html.Hr(),

    # Main grid container with a single column for the choropleth map
    html.Div(className='relative h-screen', children=[
        dcc.Graph(
            id="choropleth-map",
            style={'width': '100%', 'height': '100%'},  
            figure=px.choropleth_mapbox(
                df,
                geojson=france_departments,
                locations='Departement',
                featureidkey="properties.code",
                color='Nombre',
                color_continuous_scale="reds",
                mapbox_style="carto-positron", 
                zoom=5, 
                center={"lat": 46.603354, "lon": 1.888334},
                opacity=0.5,
                labels={'Nombre': 'Nombre de personnes'}
            ).update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        ),

        # Container for overlaid controls to the right of the choropleth map       
        html.Div(className='absolute top-0 right-0 bottom-0 flex items-center justify-center', style={'width': '30%', 'margin-right': '2%'}, children=[
            html.Div(className='bg-white shadow-md rounded-lg p-4', style={'width': '100%'}, children=[
                dcc.Input(id="input-prenom", type="text", placeholder="Enter a first name", className="border rounded px-3 py-2 mb-4"),
                html.Div(className='my-4'),
                html.Hr(),
                html.Div(className='my-4'),
                                
                dcc.Checklist(
                    id='radio-sexe',
                    options=[{'label': str(sexe), 'value': sexe} for sexe in df.sexeName.unique()],
                    value=["Homme"],
                    labelStyle={'display': 'block'}
                ),
                html.Div(className='my-4'),                
                html.Hr(),
                html.Div(className='my-4'),
                                
                dcc.RangeSlider(
                    id='range-slider-annee',
                    min=df['Annee'].min(),
                    max=df['Annee'].max(),
                    value=[df['Annee'].min(), df['Annee'].max()],
                    marks={str(year): str(year) for year in range(df['Annee'].min(), df['Annee'].max() + 1, 5)},
                    step=1,
                    className="mb-4"
                ),
                html.Div(className='my-4'),               
                html.Hr(),
                html.Div(className='my-4'),
                                
                dcc.Dropdown(
                    id='dropdown-departement',
                    options=[{'label': str(dept), 'value': dept} for dept in df['Departement'].unique()],
                    multi=True,
                    placeholder="Select Departement(s)",
                    className="border rounded px-3 py-2 mb-4"
                ),
                html.Div(className='my-4'),                
                html.Hr(),
                html.Div(className='my-4'),                
                dcc.Graph(
                    id="graph-continue",
                    figure={}
                )
            ])
        ])

    ]),
])





##_______________________________________________________________

# Add controls to build the interaction
@app.callback(
    [Output(component_id="graph-continue", component_property="figure"),
    Output(component_id="choropleth-map", component_property="figure")],
    [Input(component_id="input-prenom", component_property="value"),
     Input(component_id="radio-sexe", component_property="value"),
     Input(component_id="range-slider-annee", component_property="value"),
     Input(component_id="dropdown-departement", component_property="value")]
)

##_______________________________________________________________

def update_graph(prenom_choisi, sexe_choisi, annee_choisi, departement_choisi):
    # Filter data based on user inputs
    filtered_df = df
    
    if prenom_choisi:
        filtered_df = filtered_df[filtered_df['Prenom'] == prenom_choisi]
    
    if sexe_choisi:
        filtered_df = filtered_df[filtered_df['sexeName'].isin(sexe_choisi)]
    
    filtered_df = filtered_df[(filtered_df['Annee'] >= annee_choisi[0]) &
                              (filtered_df['Annee'] <= annee_choisi[1])]
    
    if departement_choisi:
        filtered_df = filtered_df[filtered_df['Departement'].isin(departement_choisi)]
    
    # Update graph 1 (line chart)
    grouped_df = filtered_df.groupby('Annee')['Nombre'].sum().reset_index()
    fig1 = px.line(grouped_df, x='Annee', y='Nombre', 
                   title=f'Number of people for the first name"{prenom_choisi}"',
                   labels={'Number': 'Number of people'})
    
    # Update graph 2 (choropleth map)
    dept_counts = filtered_df.groupby('Departement')['Nombre'].sum().reset_index()
    choropleth_fig = px.choropleth_mapbox(
        dept_counts,
        geojson=france_departments,
        locations='Departement',
        featureidkey="properties.code",
        color='Nombre',
        color_continuous_scale="reds",
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": 46.603354, "lon": 1.888334},
        opacity=0.5,
        labels={'Nombre': 'Nombre de prenoms'}
    ).update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                    coloraxis_colorbar=dict(x=0, len=0.5)) 
    
    return fig1, choropleth_fig
        
##_______________________________________________________________

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)