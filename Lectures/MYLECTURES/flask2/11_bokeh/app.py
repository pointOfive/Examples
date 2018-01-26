'''This example demonstrates embedding a standalone Bokeh document
into a simple Flask application, with a basic HTML web form.
To view the example, run:
    python simple.py
in this directory, and navigate to:
Exception: Java gateway process exited before sending the driver its port number    http://localhost:5000
'''
from __future__ import print_function

import flask

import numpy as np
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = flask.Flask(__name__)

colors = {
    'Black': '#000000',
    'Red':   '#FF0000',
    'Green': '#00FF00',
    'Blue':  '#0000FF',
}

def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

# function to make chart
def create_linechart(_from, to, color):
    '''
    A function to create a sinusoidal chart.
    '''
    x = np.arange(_from, to, 0.1)
    y = np.sin(x)
    TOOLS = "resize,pan,wheel_zoom,box_zoom,reset,box_select,hover"
    p = figure(tools=TOOLS)
    # p.line(x, y)
    p.scatter(x, y, color = color)
    return p
    
# dashboard
@app.route('/dashboard')
def dashboard():
    # Grab the inputs arguments from the URL
    args = flask.request.args

    # Get all the form arguments in the url with defaults
    color = colors[getitem(args, 'color', 'Black')]
    _from = int(getitem(args, '_from', 0))
    to = int(getitem(args, 'to', 10))

    chart = create_linechart(_from, to, color)
    script, div = components(chart)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    html = flask.render_template(
        'embed.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        color=color,
        _from=_from,
        to=to
    )
    return encode_utf8(html)

@app.route("/")
def polynomial():
    """ Very simple embedding of a polynomial chart
    """

    # Grab the inputs arguments from the URL
    args = flask.request.args

    # Get all the form arguments in the url with defaults
    color = colors[getitem(args, 'color', 'Black')]
    _from = int(getitem(args, '_from', 0))
    to = int(getitem(args, 'to', 10))

    # Create a polynomial line graph with those arguments
    x = list(range(_from, to + 1))
    fig = figure(title="Polynomial")
    fig.line(x, [i ** 2 for i in x], color=color, line_width=2)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig)
    html = flask.render_template(
        'embed.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        color=color,
        _from=_from,
        to=to
    )
    return encode_utf8(html)

if __name__ == "__main__":
    print(__doc__)
    app.run()
