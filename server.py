from flask import Flask, render_template, request, session, redirect, url_for, Response
import json
import poliastro
from astropy import units as u
from io import BytesIO
from matplotlib import pyplot as plt
import plotly

from poliastro.bodies import Earth, Mars, Sun
from poliastro.twobody import Orbit
import base64
app = Flask(__name__)
app.debug=True

@app.route('/', methods=['GET'])
def main():
    return render_template("main.html")

@app.route('/orbit', methods=['GET', 'POST'])
def orbit():
    if(request.method=='GET'):
        return redirect(url_for('main'))
    data = json.loads(request.data)
    print(data)
    r = list(map(float, [data['r_x'], data['r_y'], data['r_z']])) * u.km
    v = list(map(float, [data['v_x'], data['v_y'], data['v_z']])) * u.km / u.s
    plot_3d = False
    interactive = False
    if(data.get('plot_3d')):
        plot_3d = True
    if(data.get('interactive')):
        interactive = True
    ss = Orbit.from_vectors(Earth, r, v)
    if(interactive == True):
        a = ss.plot(use_3d=plot_3d, interactive=True)
        b = a.to_json()
        resp = Response(b)
        # print(len(text))
        resp.headers['Content-Type'] = 'application/json'
        return resp
    ss.plot()
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue()).decode()
    resp = Response(figdata_png)
    resp.headers['Content-Type'] = 'image/png'
    resp.headers['Content-Transfer-Encoding'] = 'base64'
    return resp

if (__name__ == '__main__'):
    app.run()
    