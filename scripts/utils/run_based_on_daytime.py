import datetime
import subprocess
import sys

def run_command_based_on_time(day_start, day_end, day_command, night_command):
    # Get the current hour
    current_hour = datetime.datetime.now().hour

    # Check if it's daytime or nighttime and execute the appropriate command
    if day_start <= current_hour < day_end:
        subprocess.run(day_command, shell=True)
    else:
        subprocess.run(night_command, shell=True)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script_name.py DAY_START_HOUR DAY_END_HOUR DAY_COMMAND NIGHT_COMMAND")
        sys.exit(1)

    day_start = int(sys.argv[1])
    day_end = int(sys.argv[2])
    day_command = sys.argv[3]
    night_command = sys.argv[4]

    run_command_based_on_time(day_start, day_end, day_command, night_command)