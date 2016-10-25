from flask import Flask, render_template, request, url_for, make_response
import numpy as np
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import StringIO
import urllib
import matplotlib.pyplot as plt
import base64


app = Flask(__name__)

def make_picture(x):
    data = np.random.randint(1,50, size=(50,x))
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1 = sns.violinplot(data=data)
    ax1 = sns.pairplot(data)
    output = StringIO.StringIO()
    plt.savefig(output, format='png')
    output.seek(0)
    return base64.b64encode(output.getvalue())


@app.route('/')
def index():
    fig = Figure()
    ax1 = fig.add_subplot(111)
    d = np.random.randint(1,40, size=(50,2))
    sns.set_style('dark')
    ax1 = sns.violinplot(data=d)
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    plt.savefig(output, format='png')
    output.seek(0)
    png_output = output.getvalue().encode('base64')
    plot_url = base64.b64encode(output.getvalue())
    return render_template('plot.html', im=plot_url)

@app.route('/thing', methods=['POST', 'GET'])
def pictures():
    
    thing_size=5
    thing = range(5)
    picture = make_picture(thing_size)
    lst = [0, 1, 2, 3, 4, 5]
    if request.method == 'POST':
        user_entry = (request.form['number'])
        picture = make_picture(int(user_entry))
        print user_entry
        return render_template('thing2.html', lst=lst, im=picture, entry=int(user_entry))
    return render_template('thing.html', lst=lst)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
