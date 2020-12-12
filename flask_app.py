from flask import Flask, escape, request, render_template, jsonify
import numpy as np
import multi_container
import json
import os
import matplotlib

import simulation

matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__, static_url_path='', static_folder='static')


@app.route('/')
def hello():
    # name = request.args.get("name", "World")
    return render_template("main.html")


@app.route('/iss_go', methods=['GET', 'POST'])
def iss_go():
    if request.method == 'POST':

        content_dict = json.loads(request.data)

        if content_dict['start_level']!= "":
            raw_data = simulation.launch_simulation(int(content_dict['start_level']))
            data = raw_data['height']
            t = np.arange(0, len(data), 1)
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.plot(t, data, color='tab:blue')

            try:
                os.remove("static/plot.png")
            except:
                print("an exception occurred: file not exist")

            fig.savefig('static/plot.png')
            response = {"code": 0,"message": "img prepared"}
        else:
            response = {"code": 1, "message": "bad_value"}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)