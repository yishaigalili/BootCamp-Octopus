import os
import shutil
from datetime import datetime
import time

# Configuration
BACKUP_DIR = "/backup"
UTIL_NAME = "backup_util"
UTIL_CONF_PATH = f"/opt/{UTIL_NAME}/{UTIL_NAME}.conf"
FAILURE_LOG_PATH = f"{BACKUP_DIR}/failure.log"

def backup_files(files):
    # Create backup directory if not exist
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # Create backup subdirectory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_subdir = os.path.join(BACKUP_DIR, timestamp)
    os.makedirs(backup_subdir)

    for file_path in files:
        try:
            # Copy file to backup directory
            file_name = os.path.basename(file_path)
            shutil.copy2(file_path, backup_subdir)
            print(f"Successfully backed up {file_name} at {timestamp}")
        except Exception as e:
            # Log failure to failure.log
            with open(FAILURE_LOG_PATH, 'a') as f:
                f.write(f"Failed to backup {file_path} at {timestamp}: {str(e)}\n")
            print(f"Warning: Failed to backup {file_name} at {timestamp}")

def read_config():
    files_to_backup = []
    with open(UTIL_CONF_PATH, 'r') as conf_file:
        for line in conf_file:
            file_path = line.strip()
            if os.path.exists(file_path):
                files_to_backup.append(file_path)
            else:
                print(f"Warning: {file_path} does not exist. Skipping.")
    return files_to_backup

def main():
    files_to_backup = read_config()
    while True:
        backup_files(files_to_backup)
        time.sleep(3600)  # Sleep for 1 hour

if __name__ == "__main__":
    main()



