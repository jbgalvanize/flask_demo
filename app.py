from flask import Flask, render_template, request, url_for, make_response
import numpy as np
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import StringIO
import urllib
import matplotlib.pyplot as plt
import base64

mat =np.random.rand(100, 100)

app = Flask(__name__)

def make_picture(x, y):
    #data = np.hstack(x,y)
    data = np.random.randint(1,50, size=(50,2))
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1 = sns.violinplot(data)
    output = StringIO.StringIO()
    plt.savefig(output, format='png')
    output.seek(0)
    return base64.b64encode(output.getvalue())


@app.route('/')
def index():
    fig = Figure()
    ax1 = fig.add_subplot(111)
    d = np.random.randint(1,40, size=(50,2))
    #sns.set_style('dark')
    #xs = range(100)
    #ys = [np.random.randint(1,50) for x in xs]

    #ax1.plot(xs, ys)
    ax1 = sns.violinplot(data=d)
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    plt.savefig(output, format='png')
    output.seek(0)
    #canvas.print_png(output)
    #response = make_response(output.getvalue())
    #response.mimetype = 'image/png'
    #return response
    png_output = output.getvalue().encode('base64')
    plot_url = base64.b64encode(output.getvalue())
    #return render_template('plot.html', im=urllib.quote(png_output.rstrip('\n')),d=d)
    return render_template('plot.html', im=plot_url)

#@app.route('/thing', methods=['POST'])
@app.route('/thing', methods=['POST'])
def thing():
    
    #if request.method == 'POST':
    #user_entry = (request.form['entry'])
    #thing = range(int(user_entry))
    thing = range(5)
    ys = [np.random.randint(1,x+4) for x in thing]
    picture = make_picture(thing, ys)
    if request.method == 'POST':
        user_entry = (request.form['number'])
        thing = range(int(user_entry))
        ys = [np.random.randint(1, x+4) for x in thing]
        picture=make_picture(thing, ys)
        #return render_template('thing2.html', im=picture)
    return render_template('thing.html')
    #return render_template('thing.html', im=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
