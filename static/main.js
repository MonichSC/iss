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
    x.open("POST", "/iss_go", true);
    x.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    x.send(JSON.stringify({ 
        "start_level": parameters[0], "min_height": parameters[1], "max_height": parameters[2], "area": parameters[3],
        "start_temp": parameters[4], "target_temp": parameters[5], "max_temp_error": parameters[6], "heater_max_power": parameters[7], "max_fluid_input": parameters[8],
        "input_fluid_temp": parameters[9], "beta": parameters[10], "ticks_per_second": parameters[11], "sim_time": parameters[12], "controller": parameters[13]
}));

    console.log("wyslano");
}



