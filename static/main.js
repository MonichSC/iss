var x = new XMLHttpRequest();


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
function wait_off() {
    document.getElementById("wait").style.display = "none";
}


// --------------------------------------------------------------------------
// Append a paragraph to the page
// --------------------------------------------------------------------------
function p(t) {
    if (!document.getElementById("status")) {
        let p = document.createElement("p");
        p.id = ("status")
        if (t) p.innerHTML = "message: " + t;
        document.body.appendChild(p);
    }
    else {
        document.getElementById("status").innerHTML = "message: " + t
    }

}
// --------------------------------------------------------------------------
// Run
// --------------------------------------------------------------------------
function iss_go() {

    let parameters = new Array();
    for (let step = 1; step <= 14; step++) {
        parameters.push(document.getElementById("par-"+step).value);
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
                    const par_box = document.querySelector(".parameters-box")
                    console.log(par_box)
                    for (let el of par_box.querySelectorAll(".parameters-row span"))
                    {
                        el.style.display = "none";
                    }
                        par_box.querySelector("button").style.display = "none";
                        par_box.querySelector(".title").style.fontSize= "23px";
                        par_box.style.flexDirection = "row";
                        p("iss_go OK");

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
    x.send(JSON.stringify({ 
        "start_level": parameters[0], "min_height": parameters[1], "max_height": parameters[2], "area": parameters[3],
        "start_temp": parameters[4], "target_temp": parameters[5], "max_temp_error": parameters[6], "heater_max_power": parameters[7], "max_fluid_input": parameters[8],
        "input_fluid_temp": parameters[9], "beta": parameters[10], "ticks_per_second": parameters[11], "sim_time": parameters[12], "controller": parameters[13]
}));

    console.log("wyslano");
}

const get_plot = () =>{

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
                    p("iss_go OK");
                    var d = new Date();
                    document.getElementById("plot").src = "/plot.png?ver=" + d.getTime();
                    document.getElementById("chart_par").style.display = "block";
                }
            }
            else    // empty
            {
                p("Błąd iss_go -- pusta odpowiedź");
            }
        }
    };


    wait();
    const plots = document.querySelector(".plot-parameters").querySelectorAll("li")
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


const add_plot = () => {

    const parameters_list = document.querySelector(".plot-parameters")
    console.log(parameters_list)
    const newLi = document.querySelector('.plot-parameters .parameters-row').cloneNode(true);
    newLi.querySelector(".nr").innerHTML = `<p>ID</p>${parameters_list.children.length+1}` 
    parameters_list.appendChild(newLi)
}

window.addEventListener("DOMContentLoaded", (e)=>{
    document.querySelector("#sim_start").addEventListener("click", iss_go);
    document.querySelector("#plot_start").addEventListener("click", get_plot);
    document.querySelector("#add_plot").addEventListener("click", add_plot);
    document.querySelector(".parameters-box").addEventListener("click", event=>{
        for (let el of event.target.querySelectorAll(".parameters-row span"))
        {
            el.style.display = "block";
        }
        event.target.querySelector(".title").style.fontSize= "20px";
        event.target.querySelector(".title").style.marginBottom= "5px";
        event.target.style.flexDirection = "column";
        event.target.querySelector("button").style.display = "block";

    })
})


