#!/usr/bin/python3

import subprocess
import re
import time

def process_suricata_output(output, log_file):
    # Regular expression to capture Suricata alerts
    alert_pattern = r"\*\*\*\s+\[\d+:\d+:\d+\]\s+(.*?)\s+\*\*\*"

    # Extract alerts using the regular expression
    alerts = re.findall(alert_pattern, output)

    # Process each alert and write it to the log file
    with open(log_file, "a") as f:
        for alert in alerts:
            f.write(f"Alert: {alert}\n")

# Replace '/etc/suricata' with the actual path to Suricata configuration
suricata_config = "/etc/suricata/suricata.yaml"
interface = "eth0"  # Replace with the network interface you want Suricata to monitor
log_file = "/var/log/suricata/fast.log"  # Replace with the path to your log file

# Command to run Suricata and capture its output
command = ["/usr/bin/suricata", "--af-packet=eth0", "-c", suricata_config, "-i", interface]

while True:
    try:
        # Start Suricata as a subprocess with buffered output
        process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

        # Process the output of Suricata in real-time
        for line in process.stdout:
            process_suricata_output(line, log_file)

    except KeyboardInterrupt:
        # Terminate Suricata if the script is interrupted
        process.terminate()

    # Sleep for 45 seconds before checking again
    time.sleep(45)
