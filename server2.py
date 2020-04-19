from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from poliastro.examples import iss
from astropy import units as u
from dash.dependencies import Input, Output, State
from poliastro.plotting import OrbitPlotter3D
from poliastro.bodies import Earth
import dash_extendable_graph as deg

# import plotly.graph_objects as go
# import flask


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='Welcome to poliastro'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    deg.ExtendableGraph(figure = iss.plot(use_3d = True, interactive = True), id = "Figure"),
    dcc.Interval(
        id='interval-component',
        interval=1000, # in milliseconds
        n_intervals=0
    )
])

@app.callback(Output('Figure', 'extendData'), [Input('interval-component', 'n_intervals')])
def change_figure(n_intervals):
	r = iss.propagate(n_intervals*u.minute).r
	plot = OrbitPlotter3D()
	plot._attractor = Earth
	figure1 = plot._plot_position(r, 'HEY', ['rgb(31, 119, 180)'])
	d1 = dict(figure1.to_plotly_json())
	d2 = dict()
	d2['x'] = d1['x']
	d2['y'] = d1['y']
	d2['z'] = d1['z']
	return [d2], [2], 20

if __name__ == '__main__':
    app.run_server(debug=True)
