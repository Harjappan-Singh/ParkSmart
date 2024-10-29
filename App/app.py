from flask import Flask, render_template
import json

alive = 0
data = {}

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/keep_alive")
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data["keep_alive"] = keep_alive_count
    parsed_json = json.dumps(data)
    return str(parsed_json)


@app.route("/status=<name>-<action>", methods=["POST"])
def event(name, action):
    global data
    if name == "red_led":
        if action == "on":
            data["LED"] = True
        elif action == "off":
            data["LED"] = False
    return str("ok")

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 50000, debug = True)