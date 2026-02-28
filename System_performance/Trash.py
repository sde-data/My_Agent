import os
import time
from datetime import datetime, timedelta

# ---------------- CONFIG ----------------
SIZE_THRESHOLD = 100 * 1024 * 1024  # 100MB for downloads
DAYS_THRESHOLD = 30  # files older than 30 days
LOG_FILE = "disk_cleanup.log"

# Directories to clean (safe, non-system)
DIRS_TO_CLEAN = [
    os.path.expanduser("~/.cache"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/.local/share/Trash"),
    "/tmp"
]
# ----------------------------------------

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - {message}\n")

def is_old(file_path, days_threshold):
    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    return datetime.now() - file_time > timedelta(days=days_threshold)

def cleanup():
    total_deleted = 0
    print("\n=== Starting Disk Cleanup ===")
    for dir_path in DIRS_TO_CLEAN:
        if not os.path.exists(dir_path):
            continue
        print(f"\nScanning: {dir_path}")
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                try:
                    filepath = os.path.join(root, f)
                    filesize = os.path.getsize(filepath)

                    # Cache files older than threshold
                    if dir_path.endswith(".cache") or dir_path == "/tmp":
                        if is_old(filepath, DAYS_THRESHOLD):
                            os.remove(filepath)
                            print(f"Deleted cache: {filepath}")
                            log(f"Deleted cache: {filepath} ({filesize} bytes)")
                            total_deleted += filesize

                    # Downloads larger than threshold
                    elif dir_path.endswith("Downloads"):
                        if filesize >= SIZE_THRESHOLD and is_old(filepath, DAYS_THRESHOLD):
                            os.remove(filepath)
                            print(f"Deleted old download: {filepath}")
                            log(f"Deleted download: {filepath} ({filesize} bytes)")
                            total_deleted += filesize

                    # Trash files older than threshold
                    elif dir_path.endswith("Trash"):
                        if is_old(filepath, DAYS_THRESHOLD):
                            os.remove(filepath)
                            print(f"Deleted trash: {filepath}")
                            log(f"Deleted trash: {filepath} ({filesize} bytes)")
                            total_deleted += filesize

                except Exception as e:
                    print(f"Cannot delete {filepath}: {e}")
                    log(f"Cannot delete {filepath}: {e}")

    print(f"\nCleanup complete. Total freed: {total_deleted / (1024*1024):.2f} MB")
    log(f"Cleanup complete. Total freed: {total_deleted / (1024*1024):.2f} MB")

if __name__ == "__main__":
    cleanup()