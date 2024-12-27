const publishKey = "pub-c-34b92735-3dad-43e4-b3a6-1b0634db6003";
const subscribeKey = "sub-c-af85c9fa-2327-45c8-accc-1b7a929001dc";
const channelName = "parksmart_pi_channel";
const secretKey = "topSecret1234567"

const pubnub = new PubNub({
    publishKey: publishKey,
    subscribeKey: subscribeKey,
    uuid: 'harjappan_mac',
    cryptoModule: PubNub.CryptoModule.aesCbcCryptoModule({cipherKey:secretKey}),
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
        const msg = event.message;

        for (const key in msg) {
            // Message is parking space
            if (msg.hasOwnProperty(key) && key.startsWith('P')) { 
                const value = msg[key];
                // console.log(`${key} is`, value);

                const className = `.space${key.substring(1)}`;
                document.querySelectorAll(className).forEach(element => {
                    element.innerHTML = value;
                });

                sendDataToBackend('/save_sensor_data', { parkingSpot: key, status: value });

            } else if (key === 'vehicle_count') {
                // Message is vehicle count
                console.log("Current vehicle count:", msg[key]);
                document.querySelector('#vehicleCount').innerHTML = msg[key];
            }
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

// --- Backend Communication ---
function sendDataToBackend(endpoint, data) {
    axios.post(endpoint, data)
        .then(response => console.log(response.data.message || "Data saved successfully."))
        .catch(error => console.error("Error sending data to backend:", error.response?.data?.error || error.message));
}