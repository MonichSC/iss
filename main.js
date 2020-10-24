var x = new XMLHttpRequest();


function iss_go()
{
    let l = document.getElementById("start_level").value;

    x.onreadystatechange = function(e)
    {
        if ( x.readyState == 4 )
        {
            wait_off();
        }
    };

    wait();

    let pars = "start_level=" + l;
    x.open("POST", "iss_go", true);
    x.send(pars);
}
