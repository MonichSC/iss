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

    for (let step = 1; step <= 14; step++)
    {
        parameters.push(document.getElementById("par-"+step).value);
    }

    const pid_parameters = document.getElementById("pid_parameters");

    let selected_controller = document.getElementById("par-14").value;

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
//                    const par_box = document.getElementById("parameters-box")
//                    for (let el of par_box.querySelectorAll(".parameters-row"))
//                    {
//                        el.style.display = "none";
//                    }
//                        par_box.querySelector("button").style.display = "none";
//                        par_box.querySelector(".title").style.fontSize= "23px";
//                        par_box.style.flexDirection = "row";
                        simulation_prepared = true;
                        show_plot_parameters();
//                        p("iss_go OK");
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
    x.send(JSON.stringify({"start_level": parameters[0], "min_height": parameters[1], "max_height": parameters[2], "area": parameters[3],
        "start_temp": parameters[4], "target_temp": parameters[5], "max_temp_error": parameters[6], "heater_max_power": parameters[7], "max_fluid_input": parameters[8],
        "input_fluid_temp": parameters[9], "beta": parameters[10], "ticks_per_second": parameters[11], "sim_time": parameters[12], "controller": parameters[13], "pid_parameters": pidPAR}));

    console.log("wyslano");
}


const hide_plot_parameters = ()=> 
{
    const par_box = document.getElementById("plot-parameters")
                    par_box.style.display = "none";
                    par_box.parentElement.querySelectorAll("button").forEach(el => {
                        el.style.display = "none"; 
                    });
//                        par_box.parentElement.querySelector(".title").style.fontSize= "23px";
//                        par_box.parentElement.style.flexDirection = "row";
}

const show_plot_parameters = ()=> {
    const par_box = document.getElementById("plot-parameters-1")
    par_box.style.display = "block";
    par_box.parentElement.querySelectorAll("button").forEach(el => {

        if(!(el.id == "remove_plot"))
        {
            el.style.display = "block";
        }
        else
        {
            if(par_box.childNodes.length > 3)
            {
                document.querySelector("#remove_plot").style.display = "block";
            }
        }
    });
/*    par_box.parentElement.querySelector(".title").style.fontSize= "20px";
    par_box.parentElement.querySelector(".title").style.marginBottom= "5px";
    par_box.parentElement.style.flexDirection = "column";*/
}



const get_plot = () =>{
    if(simulation_prepared)
    {
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
                    p("get_plot OK");
                    var d = new Date();
                    document.getElementById("plot").src = "/plot.png?ver=" + d.getTime();
                    document.getElementById("chart_par").style.display = "block";

//                    hide_plot_parameters();
                        p("get_plot OK");        
                }
            }
            else    // empty
            {
                p("Błąd get_plot -- pusta odpowiedź");
            }
        }
    };


    wait();
    const plots = document.getElementById("plot-parameters").querySelectorAll("li")
    console.log(plots)
    array=[]
    plots.forEach(el => {
        const plot_color = el.querySelector("#plot_colors").value
        const plot_values = el.querySelector("#plot_values").value
        array.push({"values_to_plot": plot_values, "color_for_plot": plot_color})
    });

    x.open("POST", "/get_plot", true);
    x.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    data= JSON.stringify(array)

    console.log(data)

    x.send(data);
    console.log("plot_start");
}
else{alert("Aby wygenerować wykres należy przeprowadzić symulację")}
}

const add_plot = () => {
    const parameters_list = document.getElementById("plot-parameters")
/*    const newLi = document.getElementById('plot-parameters parameters-row').cloneNode(true);
    newLi.querySelector(".nr").innerHTML = `<p>ID</p>${parameters_list.children.length+1}` 
    parameters_list.appendChild(newLi)
    
    document.querySelector("#remove_plot").style.display = "block";*/
    
}

const remove_plot = () => {
    const parameters_list = document.querySelector(".plot-parameters")
    parameters_list.removeChild(parameters_list.childNodes[parameters_list.childNodes.length-1]);
    console.log(parameters_list.childNodes.length);
    if(parameters_list.childNodes.length< 4)
    {
        document.querySelector("#remove_plot").style.display = "none";
    }
}

window.addEventListener("DOMContentLoaded", (e)=>{

//    hide_plot_parameters();
    document.querySelector("#remove_plot").style.display = "none";

    document.querySelector("#sim_start").addEventListener("click", iss_go);
    document.querySelector("#plot_start").addEventListener("click", get_plot);
    document.querySelector("#add_plot").addEventListener("click", add_plot);
    document.querySelector("#remove_plot").addEventListener("click", remove_plot);

/*    document.querySelector(".parameters-box").addEventListener("click", event=>{
        for (let el of event.target.querySelectorAll(".parameters-row"))
        {
            el.style.display = "flex";
        }

        if( document.getElementById("par-14").value == "pid")
        {
            document.getElementById("pid_parameters").style.display = "flex";
        }
        else
        {
            document.getElementById("pid_parameters").style.display = "none";
        }

        event.target.querySelector(".title").style.fontSize= "20px";
        event.target.querySelector(".title").style.marginBottom= "5px";
        event.target.style.flexDirection = "column";
        event.target.querySelector("button").style.display = "block";
//        hide_plot_parameters();
    })*/

//    document.querySelectorAll(".parameters-box")[1].addEventListener("click", show_plot_parameters)

/*    document.getElementById("par-14").addEventListener("change", e=>{
        if(e.target.value == "pid")
        {
            document.getElementById("pid_parameters").style.display = "flex";
        }
        else
        {
            document.getElementById("pid_parameters").style.display = "none";
        }
    })*/
})


