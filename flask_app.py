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


raw_data=[]


@app.route('/')
def hello():
    # name = request.args.get("name", "World")
    return render_template("main.html")


@app.route('/iss_go', methods=['GET', 'POST'])
def iss_go():
    global raw_data
    if request.method == 'POST':

        content_dict = json.loads(request.data)

        if content_dict['start_level'] != "":
            raw_data = simulation.launch_simulation(float(content_dict['start_level']), float(content_dict['min_height']),
                                                    float(content_dict['max_height']), float(content_dict['area']),
                                                    int(content_dict['start_temp']), int(content_dict['target_temp']),
                                                    int(content_dict['max_temp_error']),
                                                    int(content_dict['heater_max_power']),
                                                    float(content_dict['max_fluid_input']),
                                                    int(content_dict['input_fluid_temp']), float(content_dict['beta']),
                                                    int(content_dict['ticks_per_second']),
                                                    int(content_dict['sim_time']), content_dict['controller'])

            response = {"code": 0, "message": "img prepared"}
        else:
            response = {"code": 1, "message": "bad_value"}

    return jsonify(response)

@app.route('/get_plot', methods=['GET', 'POST'])
def get_plot():
    content_dict = json.loads(request.data)
    
    data = raw_data[str(content_dict[0]["values_to_plot"])]
    len_of_data = len(data)
    t = np.arange(0, len_of_data, 1)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    #print(content_dict)
    for plot in content_dict:
        print("ok")
        data = raw_data[str(plot["values_to_plot"])]
        plot_color= str(plot["color_for_plot"])
        ax.plot(t, data, color=plot_color)

    plt.xlabel('time')
    plt.ylabel("value")
    plt.xticks(np.arange(0, len_of_data + 1, len_of_data / 20))
    plt.grid(True)

    try:
        os.remove("static/plot.png")
    except:
        print("an exception occurred: file not exist")

    fig.set_size_inches(14, 4)
    fig.savefig('static/plot.png')
    response = {"code": 0, "message": "img prepared"}
 
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
