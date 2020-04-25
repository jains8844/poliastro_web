from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from poliastro.examples import iss
from astropy import units as u
from dash.dependencies import Input, Output, State
from poliastro.plotting import OrbitPlotter3D
from poliastro.bodies import Earth
import dash_extendable_graph as deg
from poliastro.plotting.util import generate_sphere
from poliastro.util import norm

# import plotly.graph_objects as go
# import flask

l = iss.sample(500)

l2 = []

for i in l:
    l2.append([i.x, i.y, i.z]*u.km)

l = l2

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__)

server = app.server

app.layout = html.Div(
    children=[
        html.H1(children="Welcome to poliastro"),
        html.Div(
            children="""
        Dash: A web application framework for Python.
    """
        ),
        deg.ExtendableGraph(
            figure=iss.plot(use_3d=True, interactive=True), id="Figure"
        ),
        dcc.Interval(
            id="interval-component", interval=50, n_intervals=0  # in milliseconds
        ),
    ]
)


@app.callback(
    Output("Figure", "extendData"), [Input("interval-component", "n_intervals")]
)
def change_figure(n_intervals):
    r = l[n_intervals % 500]
    # r = [r.x, r.y, r.z] * u.km
    radius = (norm(r) - Earth.R) * 0.5
    
    d2 = dict()
    xx, yy, zz = generate_sphere(radius, r)
    d2['x'], d2['y'], d2['z'] = xx.value, yy.value, zz.value
    return [d2], [2], 20


if __name__ == "__main__":
    app.run_server(host="192.168.31.55", port=8080, debug=True)
