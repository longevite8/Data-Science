# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

def compute_data_selected_all_site(df):
    success_all_launch_data = df[df['class'] == 1]
    return success_all_launch_data
def compute_data_selected_site(df, site):
    selected_site_launch_data = df[df['Launch Site'] == site]
    selected_site_launch_data['Number Launch'] = 1
    return selected_site_launch_data
def compute_data_all_site_range(df, range_value):
    all_site_range_data = df[df['Payload Mass (kg)'].between(range_value[0],range_value[1])]
    return all_site_range_data
def compute_data_site_range(df, site, range_value):
    site_filter_data = df[df['Launch Site'] == site]
    site_range_data = site_filter_data[site_filter_data['Payload Mass (kg)'].between(range_value[0],range_value[1])]
    return site_range_data

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                    ],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable = True
                                ),  
                                
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={
                                        2500: '2500',
                                        5000: '5000',
                                        7500: '7500',
                                        10000: '10000'
                                    },
                                    value=[min_payload,max_payload]
                                    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( [Output(component_id='success-pie-chart', component_property='figure'),
                Output(component_id='success-payload-scatter-chart', component_property='figure')],
               [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')]
             )

def get_graph(selected_site, selected_range):
    value_site = ''.join(selected_site)
    
    if value_site == 'ALL':
        # Pie chart
        all_success_launch = compute_data_selected_all_site(spacex_df)
        pie_fig = px.pie(all_success_launch, values='class', names='Launch Site', title='Total Success Launches By Site')
        # Scatter plot
        site_range_data = compute_data_all_site_range(spacex_df, selected_range)
        text_title_line = 'Correlation between Payload and Success for all Sites'
        scatter_fig = px.scatter(site_range_data, x="Payload Mass (kg)", y="class", color='Booster Version Category', title=text_title_line)
    else:
        # Pie chart
        launch_site_data = compute_data_selected_site(spacex_df, value_site)
        text_title = 'Total Success Launches for Site ' + value_site
        pie_fig = px.pie(launch_site_data, values='Number Launch', names='class', title=text_title)
        # Scatter plot
        site_range_data = compute_data_site_range(spacex_df, selected_site, selected_range)
        text_title_line = 'Correlation between Payload and Success for Site ' + value_site
        scatter_fig = px.scatter(site_range_data, x="Payload Mass (kg)", y="class", color='Booster Version Category',title=text_title_line)
          
    return [pie_fig,scatter_fig]
    
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
