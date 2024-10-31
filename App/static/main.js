let aliveSecond = 0;
let heartBeatRate = 5000;
let pubnub;
let appChannel = "parksmart_pi_channel";

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
    .catch(error=>console.log(error));
    setTimeout('keepAlive()', heartBeatRate);
}

function handleClick(cb)
{
    let value;
    if (cb.id === "green_led") {
        value = "off"; // Interpret green_led selection as turning off the red_led
        // sendEvent("red_led-" + value);
    } else {
        value = cb.checked ? "on" : "off";
        // sendEvent(cb.id + "-" + value);
    }
    publishMessage({"LED" : value})
}

const setupPubNub = () => {
    pubnub = new PubNub({
        publishKey: 'pub-c-34b92735-3dad-43e4-b3a6-1b0634db6003',
        subscribeKey: 'sub-c-af85c9fa-2327-45c8-accc-1b7a929001dc',
        userId: "harjappansingh_mac",
    });

    //create a channel
    const channel = pubnub.channel(appChannel);

    //create a subscription
    const subscription = channel.subscription();

    pubnub.addListener({
        status: (s) =>{
            console.log('Status', s.category);
        },
    });

    subscription.onMessage = (messageEvent) => {
        handleMessage(messageEvent.message);
    };

    subscription.subscribe();
};

const publishMessage = async(message) => {
    const publishPayload = {
        channel : appChannel,
        message : message,
    };
    await pubnub.publish(publishPayload);
};

function handleMessage(message)
{
    console.log(message)
    if (message["Occupied"] === "Yes") {
        document.getElementById("space1_id").innerHTML = "Booked";
    } else if (message["Occupied"] === "No") {
        document.getElementById("space1_id").innerHTML = "Available";
    }
}
