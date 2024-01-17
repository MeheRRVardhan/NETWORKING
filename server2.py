# server2.py
from flask import Flask, render_template, request
import requests
import random
from multiprocessing import Manager, Process
import time

app = Flask(__name__)

health_reports = []  # Store previous health reports

def generate_traffic(server_url, health_list, memory_list, packet_size):
    traffic_history = []
    health_history = []
    memory_history = []

    while True:
        # Simulate traffic to the Flask app
        try:
            for _ in range(packet_size):
                requests.get(server_url)
        except requests.RequestException as e:
            print(f"Error: {e}")

        # Get health data
        health = health_list[0]

        # Simulate memory usage (placeholder)
        memory_usage = random.randint(50, 100)
        memory_list[0] = memory_usage

        # Append current traffic, health, and memory data to history
        traffic_history.append(len(traffic_history) + 1)
        health_history.append(health)
        memory_history.append(memory_usage)

        # Save health report for display in server2.html
        health_reports.append((len(traffic_history), health))

        # Pause for a short duration before the next iteration
        time.sleep(0.1)

@app.route('/')
def index():
    return render_template('server2.html', health_reports=health_reports)

@app.route('/traffic_generator', methods=['GET', 'POST'])
def traffic_generator():
    if request.method == 'POST':
        packet_size = int(request.form['packet_size'])
        # Assuming packet_size is the same for all servers in this example
        return render_template('traffic_generator.html', packet_size=packet_size)
    return render_template('traffic_generator.html', packet_size=30)  # Default packet size

if __name__ == "__main__":
    server_url = "http://localhost:5002"
    with Manager() as manager:
        health_list = manager.list([100])
        memory_list = manager.list([0])

        # Change the packet_size parameter as needed
        process = Process(target=generate_traffic, args=(server_url, health_list, memory_list, 30))
        process.start()
        app.run(port=5002)
