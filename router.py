# router.py
from flask import Flask, jsonify, request, render_template
import requests
import random

app = Flask(__name__)

servers = {
    "server1": {"url": "http://localhost:5001", "status": "healthy"},
    "server2": {"url": "http://localhost:5002", "status": "healthy"},
    "server3": {"url": "http://localhost:5003", "status": "healthy"},
}

def route_request():
    # Simple load balancing: choose a random server
    available_servers = [server for server in servers if servers[server]["status"] == "healthy"]
    if not available_servers:
        return None  # No healthy servers available
    return random.choice(available_servers)

@app.route('/')
def index():
    server = route_request()
    if server:
        server_url = servers[server]["url"]
        try:
            response = requests.get(f"{server_url}/")
            return f"Response from {server}: {response.text}"
        except requests.RequestException:
            # Mark server as unhealthy if the request fails
            servers[server]["status"] = "unhealthy"
            return jsonify({"error": f"Server {server} is unhealthy"})
    else:
        return jsonify({"error": "No healthy servers available"})

@app.route('/server_health')
def server_health():
    return render_template('server_health.html', servers=servers)

@app.route('/traffic_metrics')
def traffic_metrics():
    return render_template('traffic_metrics.html')

if __name__ == "__main__":
    app.run(port=5000)
