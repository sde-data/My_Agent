import psutil
import time
from datetime import datetime

# Function to format bytes
def get_size(bytes):
    for unit in ['B','KB','MB','GB','TB']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}"
        bytes /= 1024

# Function to log messages
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("system_watchdog.log", "a") as f:
        f.write(f"{timestamp} - {message}\n")

# System Monitor function
def system_monitor():
    print("="*60)
    print("SYSTEM WATCHDOG MONITOR")
    print("="*60)

    # CPU
    cpu = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu}%")
    if cpu > 80:
        alert = f"⚠️ HIGH CPU Usage: {cpu}%"
        print(alert)
        log(alert)

    # RAM
    memory = psutil.virtual_memory()
    print(f"RAM Usage: {memory.percent}% ({get_size(memory.used)}/{get_size(memory.total)})")
    if memory.percent > 80:
        alert = f"⚠️ HIGH RAM Usage: {memory.percent}%"
        print(alert)
        log(alert)

    # Disk
    disk = psutil.disk_usage('/')
    print(f"Disk Usage: {disk.percent}%")
    if disk.percent > 85:
        alert = f"⚠️ HIGH Disk Usage: {disk.percent}%"
        print(alert)
        log(alert)

    # Top 5 Processes by Memory
    print("\nTop 5 Processes by Memory:")
    processes_mem = sorted(psutil.process_iter(['pid','name','memory_percent','cpu_percent','create_time']),
                       key=lambda p: p.info['memory_percent'],
                       reverse=True)[:5]
    for proc in processes_mem:
        uptime = datetime.now() - datetime.fromtimestamp(proc.info['create_time'])
        print(f"PID: {proc.info['pid']} | Name: {proc.info['name']} | "
              f"Memory: {proc.info['memory_percent']:.2f}% | CPU: {proc.info['cpu_percent']:.2f}% | "
              f"Uptime: {str(uptime).split('.')[0]}")
        log(f"Process: {proc.info['name']} PID:{proc.info['pid']} Mem:{proc.info['memory_percent']:.2f}% CPU:{proc.info['cpu_percent']:.2f}% Uptime:{str(uptime).split('.')[0]}")

    # Top 5 Processes by CPU
    print("\nTop 5 Processes by CPU:")
    processes_cpu = sorted(psutil.process_iter(['pid','name','cpu_percent','memory_percent','create_time']),
                       key=lambda p: p.info['cpu_percent'],
                       reverse=True)[:5]
    for proc in processes_cpu:
        uptime = datetime.now() - datetime.fromtimestamp(proc.info['create_time'])
        print(f"PID: {proc.info['pid']} | Name: {proc.info['name']} | "
              f"CPU: {proc.info['cpu_percent']:.2f}% | Memory: {proc.info['memory_percent']:.2f}% | "
              f"Uptime: {str(uptime).split('.')[0]}")
        log(f"Process CPU: {proc.info['name']} PID:{proc.info['pid']} CPU:{proc.info['cpu_percent']:.2f}% Mem:{proc.info['memory_percent']:.2f}% Uptime:{str(uptime).split('.')[0]}")

    # Active Network Connections
    connections = psutil.net_connections()
    print(f"\nActive Network Connections: {len(connections)}")
    log(f"Active Network Connections: {len(connections)}")

    print("="*60, "\n")


if __name__ == "__main__":
    while True:
        system_monitor()
        time.sleep(10)  # update every 10 seconds