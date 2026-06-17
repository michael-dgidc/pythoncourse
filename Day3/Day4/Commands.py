# Import statements
import json
# Used for reading and writing JSON files

import os
# Used for checking file existence

import time
# Used for delay between memory checks

from datetime import datetime, timedelta
# Used for timestamps and retention logic

import psutil
# Used to access system performance information (cross-platform)


# File path and configuration variables
FILE_PATH = "memory.json"
# JSON file where memory data is stored

INTERVAL = 10
# Time (in seconds) between memory checks

RETENTION_DAYS = 10
# How many days of history to keep


# Function to get memory usage using psutil
def get_memory_usage():
    # Gets current virtual memory statistics from the system
    mem = psutil.virtual_memory()

    total = mem.total // 1024
    # Total physical memory in KB

    free = mem.available // 1024
    # Available memory in KB

    used = mem.used // 1024
    # Used memory in KB

    percent = mem.percent
    # Percentage of memory used (already calculated by psutil)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        # Current UTC timestamp in ISO format

        "total_kb": total,
        # Total system memory

        "free_kb": free,
        # Available memory

        "used_kb": used,
        # Used memory

        "percent": round(percent, 2)
        # Memory usage percentage rounded to 2 decimal places
    }


# Function to load existing data from JSON file
def load_data():
    # Checks if file exists before trying to read it
    if not os.path.exists(FILE_PATH):
        return []

    try:
        # Opens file and loads JSON content
        with open(FILE_PATH, "r") as f:
            return json.load(f)

    except json.JSONDecodeError:
        # Handles corrupted or invalid JSON files
        return []


# Function to save data back to JSON file
def save_data(data):
    # Writes the full dataset to file in readable format
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=2)


# Function to remove old records beyond retention period
def prune(data):
    # Calculates cutoff date (old data limit)
    cutoff = datetime.utcnow() - timedelta(days=RETENTION_DAYS)

    cleaned = []
    # New list for valid (recent) records

    for x in data:
        # Loop through all stored records

        try:
            # Convert timestamp string back to datetime
            if datetime.fromisoformat(x["timestamp"]) >= cutoff:
                cleaned.append(x)
                # Keep record if it is within retention period

        except:
            # Skip records with invalid timestamps
            pass

    return cleaned


# Main program loop
def main():
    while True:
        # Continuously run memory monitoring

        usage = get_memory_usage()
        # Get current memory snapshot

        data = load_data()
        # Load previous history

        data.append(usage)
        # Add new snapshot

        data = prune(data)
        # Remove old data beyond retention period

        save_data(data)
        # Save updated dataset

        print(f"{usage['timestamp']} -> {usage['percent']}%")
        # Display current memory usage

        time.sleep(INTERVAL)
        # Wait before next measurement


# Entry point of program
if __name__ == "__main__":
    main()
    # Starts the monitoring process