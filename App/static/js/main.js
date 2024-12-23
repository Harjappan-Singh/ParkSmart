const publishKey = "pub-c-34b92735-3dad-43e4-b3a6-1b0634db6003";
const subscribeKey = "sub-c-af85c9fa-2327-45c8-accc-1b7a929001dc";
const channelName = "parksmart_pi_channel";

const pubnub = new PubNub({
    publishKey: publishKey,
    subscribeKey: subscribeKey,
    uuid: 'harjappan_mac',
});

// --- Initialization Functions ---
function initApp() {
    subscribeToChannel();
    initializeToggleListeners();
}

document.addEventListener("DOMContentLoaded", initApp);

// --- PubNub Communication ---
function subscribeToChannel() {
    console.log("Subscribing to channel:", channelName, "with UUID:", pubnub.getUUID());
    pubnub.subscribe({ channels: [channelName] });
    pubnub.addListener({
        message: handleIncomingMessage,
        status: handlePubNubStatus,
    });
}

function publishMessage(message, callback) {
    try {
        console.log("Message:", message);

        pubnub.publish({ channel: channelName, message: message }, (status, response) => {
            if (status.error) {
                console.error("Error publishing message:", status);
            } else {
                console.log("Message sent successfully:", response);
            }
            if (callback) callback(status, response);
        });
    } catch (error) {
        console.error("Error in publishMessage:", error);
    }
}

function handleIncomingMessage(event) {
     try {
        // console.log("Received message:", event.message);

        const msg = event.message;

        if (msg.P1 !== undefined) {
            console.log("P1 is", msg.P1);
            document.querySelectorAll('.space1').forEach(element => {
                element.innerHTML = msg.P1;
            });
        } else if (msg.vehicle_count !== undefined) {
            console.log("Current vehicle count:", msg.vehicle_count);
            document.querySelector('#vehicleCount').innerHTML = msg.vehicle_count
        } else {
            console.log("Unknown message format:", msg);
        }
    } catch (error) {
        console.error("Error handling incoming message:", error);
     }
}


function handlePubNubStatus(statusEvent) {
    if (statusEvent.category === "PNConnectedCategory") {
        console.log("Successfully connected to PubNub channel.");
    } else {
        console.warn("PubNub connection status:", statusEvent);
    }
}

// --- Event Listeners ---
function setupToggleListener(toggleId, key) {
    const toggle = document.getElementById(toggleId);
    if (!toggle) return;

    toggle.addEventListener("change", () => {
        const toggleState = toggle.checked ? "on" : "off";
        const message = { [key]: toggleState };
        publishMessage(message);
    });
}

function initializeToggleListeners() {
    setupToggleListener("parkSmartMonitorToggle", "parkSmartMonitor");
    setupToggleListener("redLedToggle", "redLed");
    setupToggleListener("greenLedToggle", "greenLed");
}
