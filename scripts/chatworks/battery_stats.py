import psutil

battery = psutil.sensors_battery()
plugged = battery.power_plugged
percent = battery.percent
print(f"Battery is {percent}% charged")

if plugged:
    print("The laptop is plugged in")
else:
    print("The laptop is not plugged in")