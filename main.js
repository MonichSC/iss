var x = new XMLHttpRequest();


// --------------------------------------------------------------------------
// Show wait animation
// --------------------------------------------------------------------------
function wait()
{
    if ( !document.getElementById("wait") )
    {
        let w = document.createElement("div");
        w.id = "wait";
        w.className = "wt";     // see silgy.css
        w.style.display = "block";
        document.body.appendChild(w);
    }
    else
        document.getElementById("wait").style.display = "block";
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
    let p = document.createElement("p");
    if ( t ) p.innerHTML = t;
    document.body.appendChild(p);
    return p;
}


// --------------------------------------------------------------------------
// Run
// --------------------------------------------------------------------------
function iss_go()
{
    let l = document.getElementById("start_level").value;

    x.onreadystatechange = function(e)
    {
        if ( x.readyState == 4 )
        {
            wait_off();

            if ( x.responseText.length > 0 )
            {
                let r = JSON.parse(x.responseText);

                if ( r.code != 0 )  // error -- show message
                {
                    p(r.message);
                }
                else    // ok
                {
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

    let pars = "start_level=" + l;
    x.open("POST", "iss_go", true);
    x.send(pars);
}
