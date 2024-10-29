let aliveSecond = 0;
let heartBeatRate = 5000;

function time()
{
    let d = new Date();
    let currentSecond = d.getTime();
    if(currentSecond - aliveSecond > heartBeatRate + 1000)
    {
        document.getElementById("connection_id").innerHTML="DEAD";
    }
    else
    {
        document.getElementById("connection_id").innerHTML="ALIVE";
    }
    setTimeout('time()', 1000);
}

function keepAlive()
{
    fetch('/keep_alive')
    .then(response=>{
        if(response.ok){
            let date = new Date();
            aliveSecond = date.getTime();
            return response.json();
        }
        throw new Error("Server offline");
    })
    .then(responseJson=>{
        if(responseJson.parking_space == 1)
        {
            document.getElementById("space1_id").innerHTML="Booked/Occupied";
        }
        else
        {
            document.getElementById("space1_id").innerHTML="Available";
        }
    })
    .catch(error=>console.log(error));
    setTimeout('keepAlive()', heartBeatRate);
}

function handleClick(cb)
{
    let value;
    if (cb.id === "green_led") {
        value = "off"; // Interpret green_led selection as turning off the red_led
        sendEvent("red_led-" + value);
    } else {
        value = cb.checked ? "on" : "off";
        sendEvent(cb.id + "-" + value);
    }
}

function sendEvent(value)
{
    fetch("/status="+value,
    {
        method:"POST",
    })
}
