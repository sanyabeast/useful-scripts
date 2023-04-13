import time
import subprocess
import cv2
import numpy as np
import os

AUTOAJUST_INTERVAL = 15 * 60
MIN_BRIGHTNESS = 0.25
GAMMA_CURVE = 1/3

def is_on_battery():
    return  'on-line' not in subprocess.check_output(['acpi', '-a']).decode().strip()

def lerp(start, end, t):
    """Linearly interpolates between start and end based on a value t between 0 and 1"""
    return (1 - t) * start + t * end

def get_webcam_gamma(step=16):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open video device")
    ret, frame = cap.read()
    if not ret:
        raise Exception("Could not read a frame from video device")
    cap.release()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Downsample the image by a factor of 2
    gray = cv2.resize(gray, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    # Process only every 'step' pixel
    gray = gray[::step, ::step]
    gamma = np.mean(np.power(gray/255.0, GAMMA_CURVE))
    return round(gamma, 1)

def set_brightness(brightness):
    os.system(f"pkexec xfpm-power-backlight-helper --set-brightness={brightness}")

def get_brightness():
    output = os.popen("pkexec xfpm-power-backlight-helper --get-brightness").read()
    brightness = int(output.strip())
    return brightness

def get_max_brightness():
    output = os.popen("pkexec xfpm-power-backlight-helper --get-max-brightness").read()
    max_brightness = int(output.strip())
    return max_brightness

def get_idle_time():
    output = os.popen("xprintidle").read()
    idle_time = int(output.strip())
    return idle_time / 1000

time.sleep(1)
prev_autoajust_time = 0
idle_update_done = False
while True:
    if (is_on_battery()):
        now = time.time()
        needs_update = now - prev_autoajust_time > AUTOAJUST_INTERVAL
        if (get_idle_time() > 59):
            if not idle_update_done:
                idle_update_done = True
                needs_update = True
        else:
            idle_update_done = False

        if needs_update:
                gamma = get_webcam_gamma()
                max_brightness = get_max_brightness()
                new_brightness = int(lerp(int(MIN_BRIGHTNESS * max_brightness), max_brightness, gamma))
                current_brightness = get_brightness()
                
                if (new_brightness < current_brightness):
                    set_brightness(new_brightness)

                prev_autoajust_time = now

    time.sleep(29)