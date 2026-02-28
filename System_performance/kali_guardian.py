import os
import psutil
import time
from datetime import datetime, timedelta

# ---------------- CONFIG ----------------
CPU_THRESHOLD = 80       # %
RAM_THRESHOLD = 80       # %
DISK_THRESHOLD = 85      # %
SIZE_THRESHOLD = 100*1024*1024  # 100MB
DAYS_OLD = 30
DIRS_TO_CLEAN = [
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/.cache"),
    os.path.expanduser("~/.local/share/Trash"),
    "/tmp"
]
PATCH_EXTENSIONS = ["*.patch", "*.diff"]

WATCHDOG_LOG = "system_watchdog.log"
CLEANUP_LOG = "disk_cleanup.log"
UPDATE_INTERVAL = 60  # seconds
# ----------------------------------------

def log(message, logfile):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(logfile, "a") as f:
        f.write(f"{timestamp} - {message}\n")

def get_size(bytes):
    for unit in ['B','KB','MB','GB','TB']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}"
        bytes /= 1024

def check_thresholds():
    alerts = []
    cpu = psutil.cpu_percent(interval=1)
    if cpu > CPU_THRESHOLD:
        alerts.append(f"⚠️ HIGH CPU: {cpu}%")

    memory = psutil.virtual_memory()
    if memory.percent > RAM_THRESHOLD:
        alerts.append(f"⚠️ HIGH RAM: {memory.percent}%")

    disk = psutil.disk_usage('/')
    if disk.percent > DISK_THRESHOLD:
        alerts.append(f"⚠️ HIGH DISK: {disk.percent}%")

    for alert in alerts:
        log(alert, WATCHDOG_LOG)

def automated_cleanup():
    total_deleted = 0
    for dir_path in DIRS_TO_CLEAN:
        if not os.path.exists(dir_path):
            continue
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                filepath = os.path.join(root, f)
                try:
                    filesize = os.path.getsize(filepath)
                    old = datetime.now() - datetime.fromtimestamp(os.path.getmtime(filepath)) > timedelta(days=DAYS_OLD)

                    # Patch files
                    if any(f.endswith(ext.replace('*','')) for ext in PATCH_EXTENSIONS) and old:
                        os.remove(filepath)
                        log(f"Deleted patch: {filepath} ({get_size(filesize)})", CLEANUP_LOG)
                        total_deleted += filesize

                    # Large downloads
                    elif dir_path.endswith("Downloads") and filesize >= SIZE_THRESHOLD and old:
                        os.remove(filepath)
                        log(f"Deleted download: {filepath} ({get_size(filesize)})", CLEANUP_LOG)
                        total_deleted += filesize

                    # Cache/Trash/tmp
                    elif dir_path.endswith(".cache") or dir_path.endswith("Trash") or dir_path == "/tmp":
                        if old:
                            os.remove(filepath)
                            log(f"Deleted cache/trash/tmp: {filepath} ({get_size(filesize)})", CLEANUP_LOG)
                            total_deleted += filesize
                except Exception as e:
                    log(f"Cannot delete {filepath}: {e}", CLEANUP_LOG)
    if total_deleted > 0:
        log(f"Cleanup complete. Total freed: {get_size(total_deleted)}", CLEANUP_LOG)

if __name__ == "__main__":
    while True:
        check_thresholds()
        automated_cleanup()
        time.sleep(UPDATE_INTERVAL)