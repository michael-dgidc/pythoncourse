import json
import os
import time
import subprocess
from datetime import datetime, timedelta

FILE_PATH = "memory.json"
INTERVAL = 10
RETENTION_DAYS = 10


def get_memory_usage():
    result = subprocess.check_output(
        ["wmic", "OS", "get", "FreePhysicalMemory,TotalVisibleMemorySize", "/Value"],
        text=True
    )


    data = {}
    for line in result.splitlines():
        if "=" in line:
            key, val = line.split("=")
            data[key.strip()] = int(val.strip())

    total = data.get("TotalVisibleMemorySize", 0)
    free = data.get("FreePhysicalMemory", 0)
    used = total - free
    percent = (used / total) * 100 if total else 0

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "total_kb": total,
        "free_kb": free,
        "used_kb": used,
        "percent": round(percent, 2)
    }


def load_data():
    if not os.path.exists(FILE_PATH):
        return []

    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def save_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=2)


def prune(data):
    cutoff = datetime.utcnow() - timedelta(days=RETENTION_DAYS)

    return [
        x for x in data
        if "timestamp" in x and datetime.fromisoformat(x["timestamp"]) >= cutoff
    ]


def main():
    while True:
        usage = get_memory_usage()

        data = load_data()
        data.append(usage)
        data = prune(data)

        save_data(data)

        print(f"{usage['timestamp']} -> {usage['percent']}%")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()