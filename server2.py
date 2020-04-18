import dash
import dash_core_components as dcc
import dash_html_components as html
from poliastro.examples import iss
from astropy import units as u
from dash.dependencies import Input, Output, State
from poliastro.plotting import OrbitPlotter3D
from poliastro.bodies import Earth
# import plotly.graph_objects as go
import flask


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='Welcome to poliastro'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(figure = iss.plot(use_3d = True, interactive = True), id = "Figure"),
    dcc.Interval(
        id='interval-component',
        interval=2000, # in milliseconds
        n_intervals=0
    )
])

@app.callback(Output('Figure', 'figure'), [Input('interval-component', 'n_intervals')], [State('Figure', 'figure')])
def change_figure(n_intervals, figure):
	r = iss.propagate(n_intervals*u.minute).r
	plot = OrbitPlotter3D()
	plot._attractor = Earth
	figure1 = plot._plot_position(r, 'HEY', ['rgb(31, 119, 180)'])
	figure['data'][2] = figure1.to_plotly_json()
	figure['layout']['uirevision'] = 'False'
	return figure

if __name__ == '__main__':
    app.run_server(debug=True)
