from flask import Flask, escape, request, render_template, jsonify
import numpy as np
import json
import os
import matplotlib
import simulation

matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__, static_url_path='', static_folder='static')


raw_data=[]


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/symulacja')
def symulacja():
    return render_template("symulacja.html")


@app.route('/iss_go', methods=['GET', 'POST'])
def iss_go():
    global raw_data
    if request.method == 'POST':
        content_dict = json.loads(request.data)
        print(content_dict)

        if content_dict['start_level'] != "":
            raw_data = simulation.launch_simulation(float(content_dict['start_level']),
                                                    float(content_dict['min_level']),
                                                    float(content_dict['max_level']),
                                                    float(content_dict['area']),
                                                    int(content_dict['start_temp']),
                                                    int(content_dict['target_temp']),
#                                                    int(content_dict['max_temp_error']),
                                                    int(content_dict['max_heater_power']),
                                                    int(content_dict['input_temp']),
                                                    float(content_dict['max_input']),
                                                    float(content_dict['max_output']),
#                                                    float(content_dict['start_in_valve_status']),
#                                                    float(content_dict['start_out_valve_status']),
                                                    int(content_dict['sim_time']),
                                                    content_dict['controller'],
                                                    content_dict["pid_params"])

            
            

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
        print("an exception occurred: file does not exist")

    fig.set_size_inches(14, 4)
    fig.savefig('static/plot.png')
    response = {"code": 0, "message": "img prepared"}
 
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
