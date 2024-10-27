import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('spacex_launch_dash.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("SpaceX Launch Dashboard", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    dcc.Graph(id='success-pie-chart'),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[0, 10000],
        marks={i: str(i) for i in range(0, 10001, 1000)}
    ),
    dcc.Graph(id='success-payload-scatter'),
])

# Callback for the pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(selected_site):
    if selected_site == 'ALL':
        filtered_df = df
    else:
        filtered_df = df[df['Launch Site'] == selected_site]

    success_counts = filtered_df['class'].value_counts()

    fig = px.pie(
        values=success_counts,
        names=success_counts.index,
        title=f'Success Count for {selected_site}' if selected_site != 'ALL' else 'Total Success Count for All Sites'
    )
    
    return fig

# Callback for the scatter plot
@app.callback(
    Output('success-payload-scatter', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def update_scatter(selected_site, selected_payload):
    # Filter the data based on the selected payload range
    filtered_df = df[(df['Payload Mass (kg)'] >= selected_payload[0]) &
                     (df['Payload Mass (kg)'] <= selected_payload[1])]
    
    # If a specific site is selected, filter by that site as well
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    print(filtered_df.shape)  # Check how many rows are returned

    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs. Success by Booster Version',
        labels={'class': 'Success (1) / Failure (0)'}
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
