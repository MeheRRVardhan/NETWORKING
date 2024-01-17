# generate_traffic.py
import requests
import time
import random
import matplotlib.pyplot as plt
from multiprocessing import Manager, Process

def plot_histogram(traffic_history, server_name):
    plt.hist(traffic_history, bins=30, color='orange', alpha=0.7)
    plt.title(f'Traffic Histogram - {server_name}')
    plt.xlabel('Packet Count')
    plt.ylabel('Frequency')
    plt.show()

def plot_scatter(transmission_history, server_name):
    plt.scatter(range(len(transmission_history)), transmission_history, color='blue', alpha=0.7)
    plt.title(f'Transmission Rate Scatter - {server_name}')
    plt.xlabel('Time (s)')
    plt.ylabel('Transmission Rate')
    plt.show()

def plot_cpu_performance(cpu_history, server_name):
    index = range(len(cpu_history))

    plt.bar(index, cpu_history, label=f"{server_name} CPU Performance", color='purple', alpha=0.7)
    plt.title(f'{server_name} CPU Performance Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('CPU Performance (%)')
    plt.legend()
    plt.show()

def plot_line_graph(memory_history, server_name):
    plt.plot(memory_history, label=f"{server_name} Memory Usage", color='green')
    plt.title(f'{server_name} Memory Usage Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Memory Usage (%)')
    plt.legend()
    plt.show()

def update_plots(traffic_history, cpu_history, memory_history, transmission_history, server_url):
    plt.clf()  # Clear the current figure

    # Plot histogram
    plt.subplot(3, 2, 1)
    plt.hist(traffic_history, bins=30, color='orange', alpha=0.7)
    plt.title(f'Traffic Histogram - {server_url}')
    plt.xlabel('Packet Count')
    plt.ylabel('Frequency')

    # Plot CPU performance
    plt.subplot(3, 2, 3)
    index = range(len(cpu_history))
    plt.bar(index, cpu_history, label=f"{server_url} CPU Performance", color='purple', alpha=0.7)
    plt.title(f'{server_url} CPU Performance Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('CPU Performance (%)')

    # Plot memory usage
    plt.subplot(3, 2, 5)
    plt.plot(memory_history, label=f"{server_url} Memory Usage", color='green')
    plt.title(f'{server_url} Memory Usage Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Memory Usage (%)')

    # Plot transmission rate scatter plot
    plt.subplot(3, 2, 2)
    plt.scatter(range(len(transmission_history)), transmission_history, color='blue', alpha=0.7)
    plt.title(f'Transmission Rate Scatter - {server_url}')
    plt.xlabel('Time (s)')
    plt.ylabel('Transmission Rate')

    plt.tight_layout()
    plt.pause(0.1)

def generate_traffic(server_url, health_list, memory_list, traffic_list, cpu_list, transmission_list):
    traffic_history = []
    health_history = []
    memory_history = []
    cpu_history = []
    transmission_history = []

    plt.ion()  # Enable interactive mode for dynamic plotting

    try:
        for _ in range(30):
            response = requests.get(server_url)
            # Simulate CPU performance (placeholder)
            cpu_performance = random.randint(0, 100)
            cpu_list[0] = cpu_performance
            # Simulate memory usage (placeholder)
            memory_usage = random.randint(50, 100)
            memory_list[0] = memory_usage
            # Simulate transmission rate (placeholder)
            transmission_rate = random.uniform(0.5, 5.0)
            transmission_list[0] = transmission_rate
            # Comment out the line below to remove the print statement
            # print(response.text)
            time.sleep(0.1)  # Introduce a delay of 0.1 seconds

            # Get health data
            health = health_list[0]

            # Append current traffic, health, and memory data to history
            traffic_history.append(len(traffic_history) + 1)
            health_history.append(health)
            memory_history.append(memory_usage)

            # Append current CPU performance to history
            cpu_history.append(cpu_performance)

            # Append current transmission rate to history
            transmission_history.append(transmission_rate)

            # Update the plots dynamically
            update_plots(traffic_history, cpu_history, memory_history, transmission_history, server_url)

            # Pause for a short duration before the next iteration
            time.sleep(0.1)

    except requests.RequestException as e:
        print(f"Error: {e}")

    plt.ioff()  # Disable interactive mode after the loop

if __name__ == "__main__":
    server_url1 = "http://localhost:5001"  # Replace with your first server URL
    server_url2 = "http://localhost:5002"  # Replace with your second server URL
    server_url3 = "http://localhost:5003"  # Replace with your third server URL

    with Manager() as manager:
        # For the first server
        health_list1 = manager.list([100])
        memory_list1 = manager.list([0])
        traffic_list1 = manager.list([0])
        cpu_list1 = manager.list([0])
        transmission_list1 = manager.list([0])

        process1 = Process(target=generate_traffic, args=(server_url1, health_list1, memory_list1, traffic_list1, cpu_list1, transmission_list1))
        process1.start()

        # For the second server
        health_list2 = manager.list([100])
        memory_list2 = manager.list([0])
        traffic_list2 = manager.list([0])
        cpu_list2 = manager.list([0])
        transmission_list2 = manager.list([0])

        process2 = Process(target=generate_traffic, args=(server_url2, health_list2, memory_list2, traffic_list2, cpu_list2, transmission_list2))
        process2.start()

        # For the third server
        health_list3 = manager.list([100])
        memory_list3 = manager.list([0])
        traffic_list3 = manager.list([0])
        cpu_list3 = manager.list([0])
        transmission_list3 = manager.list([0])

        process3 = Process(target=generate_traffic, args=(server_url3, health_list3, memory_list3, traffic_list3, cpu_list3, transmission_list3))
        process3.start()

        process1.join()
        process2.join()
        process3.join()
