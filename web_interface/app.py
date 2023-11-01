from flask import Flask, render_template, jsonify
import subprocess
import threading
import queue
import signal
from serial.tools import list_ports
from werkzeug.serving import run_simple, WSGIRequestHandler

app = Flask(__name__)

# Initialize a Queue to hold logs
log_queue = queue.Queue()

# Global process variable to hold the PIO process
process = None
# Global variable to indicate if the thread should stop
stop_thread = False

# Global dictionary to hold service statuses
service_statuses = {
    "pio_remote": "Stopped",
    "webcam_stream": "Stopped",
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/testlog")
def test_log():
    return render_template("testlog.html")


@app.route("/pioremotelog")
def pio_remote_log():
    return render_template("pioremotelog.html")


@app.route("/get_pioremotelog")
def get_pio_remote_log():
    logs = []
    try:
        while True:
            logs.append(log_queue.get_nowait())
    except queue.Empty:
        pass
    return jsonify(logs)


@app.route("/service_status")
def service_status():
    # Return the real statuses from the global service_statuses dictionary
    return jsonify(service_statuses)


@app.route("/serial_devices")
def get_serial_devices():
    devices = [
        {"device": port.device, "description": port.description}
        for port in list_ports.comports()
    ]
    return jsonify(devices)


# Function to run PIO Remote Agent
def run_pio_remote_agent():
    global process, stop_thread, service_statuses
    process = subprocess.Popen(
        ["pio", "remote", "agent", "start"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    service_statuses["pio_remote"] = "Running"
    while not stop_thread:
        output = process.stdout.readline()
        if output:
            log_queue.put(output.strip())  # Add log to queue
        else:  # No more output, break the loop
            if process.poll() is not None:
                # Check if the process ended due to an error
                if process.returncode != 0:
                    service_statuses["pio_remote"] = "Error"
                else:
                    service_statuses["pio_remote"] = "Stopped"
            break

    process.terminate()


# Function to handle SIGINT signal
def signal_handler(sig, frame):
    global stop_thread
    print("Shutting down gracefully...")
    stop_thread = True
    if process:
        process.terminate()
    exit(0)


# Handle SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Start PIO Remote Agent in a separate thread
t = threading.Thread(target=run_pio_remote_agent)
t.start()


if __name__ == "__main__":
    # # Handle SIGINT
    # signal.signal(signal.SIGINT, signal_handler)

    # # Start PIO Remote Agent in a separate thread
    # t = threading.Thread(target=run_pio_remote_agent)
    # t.start()

    # Run Flask without reloader
    run_simple("0.0.0.0", 5000, app, use_reloader=False)
