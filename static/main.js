var x = new XMLHttpRequest();
let simulation_prepared = false;

// --------------------------------------------------------------------------
// Show wait animation
// --------------------------------------------------------------------------
function wait() {
    if (!document.getElementById("wait")) {
        let w = document.createElement("div");
        w.id = "wait";
        w.classList.add("wt");     // see silgy.css
        w.style.display = "block";
        w.style.backgroundImage = "url('img/wait.gif')";
        document.body.appendChild(w);

    }
    else { document.getElementById("wait").style.display = "block"; }
    document.getElementById("chart_par").style.display = "none";
}


// --------------------------------------------------------------------------
// Turn the spinning wheel off
// --------------------------------------------------------------------------
function wait_off()
{
    document.getElementById("wait").style.display = "none";
}


// --------------------------------------------------------------------------
// Append a paragraph to the page
// --------------------------------------------------------------------------
function p(t)
{
    if (!document.getElementById("status"))
    {
        let p = document.createElement("p");
        p.id = ("status")
        if (t) p.innerHTML = "message: " + t;
        document.body.appendChild(p);
    }
    else
    {
        document.getElementById("status").innerHTML = "message: " + t;
    }
}


// --------------------------------------------------------------------------
// Run
// --------------------------------------------------------------------------
function iss_go()
{
    let pidPAR = null;

    let parameters = new Array();

    for (let step = 1; step <= 16; step++)
    {
        parameters.push(document.getElementById("par-"+step).value);
    }

    const pid_parameters = document.getElementById("pid_parameters");

    let selected_controller = document.getElementById("par-16").value;

    console.log("selected_controller: " + selected_controller);

    if (selected_controller == "pid")
    {
        pidPAR = 
        {
            "input": {
                    "p": parseFloat(pid_parameters.querySelector("#par-i_p").value),
                    "i": parseFloat(pid_parameters.querySelector("#par-i_i").value), 
                    "d": parseFloat(pid_parameters.querySelector("#par-i_d").value)},
            "output":   {
                    "p": parseFloat(pid_parameters.querySelector("#par-o_p").value),
                    "i": parseFloat(pid_parameters.querySelector("#par-o_i").value), 
                    "d": parseFloat(pid_parameters.querySelector("#par-o_d").value)},
            "temperature": 
            {
                    "p": parseFloat(pid_parameters.querySelector("#par-t_i").value),
                    "i": parseFloat(pid_parameters.querySelector("#par-t_p").value), 
                    "d": parseFloat(pid_parameters.querySelector("#par-t_d").value)
            }
        }
    }

    x.onreadystatechange = function (e) {
        if (x.readyState == 4) {
            wait_off();

            if (x.responseText.length > 0) {
                let r = JSON.parse(x.responseText);

                if (r.code != 0)   // error -- show message
                {
                    p(r.message);
                }
                else    // ok
                {
                        simulation_prepared = true;
                        document.getElementById("sim_ready_msg").style.display = "";
                        document.getElementById("plot").style.display = "";
                }
            }
            else    // empty
            {
                p("Błąd iss_go -- pusta odpowiedź");
            }
        }
    };

    wait();

    x.open("POST", "/iss_go", true);

    x.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    x.send(JSON.stringify({"start_level": parameters[0],
                            "min_level": parameters[1],
                            "max_level": parameters[2],
                            "area": parameters[3],
                            "start_temp": parameters[4],
                            "target_temp": parameters[5],
                            "max_temp_error": parameters[6],
                            "max_heater_power": parameters[7],
                            "input_temp": parameters[8],
                            "max_input": parameters[9],
                            "max_output": parameters[10],
                            "start_in_valve_status": parameters[11],
                            "start_out_valve_status": parameters[12],
                            "beta": parameters[13],
                            "sim_time": parameters[14],
                            "controller": parameters[15],
                            "pid_parameters": pidPAR}));

    console.log("wyslano");
}


// --------------------------------------------------------------------------
// change of controller
// --------------------------------------------------------------------------
function callback_change_controller(e){
    if(e.target.value == "pid")
    {
        document.getElementById("pid_parameters").style.display = "flex";
    }
    else
    {
        document.getElementById("pid_parameters").style.display = "none";
    }
}


// --------------------------------------------------------------------------
//  generate and show plot
// --------------------------------------------------------------------------
function get_plot()
{
    if (!simulation_prepared)
    {
        alert("Aby wygenerować wykres należy przeprowadzić symulację");
        return;
    }
    
    x.onreadystatechange = function (e) {
        if (x.readyState == 4) {
            wait_off();

            if (x.responseText.length > 0) {
                let r = JSON.parse(x.responseText);

                if (r.code != 0)   // error -- show message
                {
                    p(r.message);
                }
                else    // ok
                {
                    var d = new Date();
                    document.getElementById("plot-img").src = "/plot.png?ver=" + d.getTime();
                    document.getElementById("chart_par").style.display = "block";    
                }
            }
            else    // empty
            {
                p("Błąd get_plot -- pusta odpowiedź");
            }
        }
    };

    wait();
    array=[];
   let i = 1;
   while (plot_parameter = document.getElementById("plot-parameters-"+i))
   {
      const plot_color = plot_parameter.querySelector("#plot_colors").value
      const plot_values = plot_parameter.querySelector("#plot_values").value
      array.push({"values_to_plot": plot_values, "color_for_plot": plot_color})
      i++;
   }
  
    x.open("POST", "/get_plot", true);
    x.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    data = JSON.stringify(array);
    x.send(data);
    console.log("plot_start");
}

// --------------------------------------------------------------------------
//  add new values to plot
// --------------------------------------------------------------------------
function add_plot () {

    const parameters_list = document.getElementById("plot-parameters-box");
    const new_row = document.getElementById('plot-parameters-1').cloneNode(true);
    new_row.id = `plot-parameters-${parameters_list.childNodes.length-1}`
    parameters_list.appendChild(new_row)
    document.querySelector("#remove_plot").style.display = "block";
}


// --------------------------------------------------------------------------
//  remove values for plot
// --------------------------------------------------------------------------
function remove_plot(){
    const parameters_list = document.getElementById("plot-parameters-box");
    parameters_list.removeChild(parameters_list.childNodes[parameters_list.childNodes.length-1]);
    console.log(parameters_list.childNodes.length);
    if(parameters_list.childNodes.length < 4)
    {
        document.querySelector("#remove_plot").style.display = "none";
    }
}


window.addEventListener("DOMContentLoaded", (e)=>{

    document.querySelector("#remove_plot").style.display = "none";

    // nasłuchiwanie zdarzeń od buttons
    document.querySelector("#sim_start").addEventListener("click", iss_go);
    document.querySelector("#plot_start").addEventListener("click", get_plot);
    document.querySelector("#add_plot").addEventListener("click", add_plot);
    document.querySelector("#remove_plot").addEventListener("click", remove_plot);

    // nasłuchiwanie na zdarzenie zmiany controlera
    document.getElementById("par-14").addEventListener("change", callback_change_controller)
})


