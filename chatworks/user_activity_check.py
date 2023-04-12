import time
from Xlib import X, display

def is_user_active():
    # Create a connection to the X server
    d = display.Display()

    # Get the root window
    root = d.screen().root

    # Query the server for the current pointer location
    pointer = root.query_pointer()

    # Get the timestamp of the last pointer event
    last_activity_time = pointer.time

    # Get the current server time
    current_time = int(time.time() * 1000)

    # Calculate the time elapsed since the last pointer event
    time_since_last_activity = current_time - last_activity_time

    # Return True if the user has been active in the last 5 seconds
    return time_since_last_activity < 5000

# Create a connection to the X server
d = display.Display()

# Get the root window
root = d.screen().root

# Get the current pointer location
pointer = root.query_pointer()

# Save the initial pointer location
x, y = pointer.root_x, pointer.root_y

while True:
    # Check if the user is currently active
    if not is_user_active():
        # Move the mouse 1 pixel to the right
        x += 1
        root.warp_pointer(x, y)
        d.sync()
        
    # Wait for 5 seconds
    time.sleep(5)