import time
import subprocess
import cv2
import numpy as np
import os

AUTOAJUST_INTERVAL = 15 * 60
MIN_BRIGHTNESS = 0.25
GAMMA_CURVE = 1/4

def is_on_battery():
    return  'on-line' not in subprocess.check_output(['acpi', '-a']).decode().strip()

def lerp(start, end, t):
    """Linearly interpolates between start and end based on a value t between 0 and 1"""
    return (1 - t) * start + t * end

def get_webcam_gamma():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    if not cap.isOpened():
        raise Exception("Could not open video device")
    ret, frame = cap.read()
    if not ret:
        raise Exception("Could not read a frame from video device")
    cap.release()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gamma = np.mean(np.power(gray/255.0, GAMMA_CURVE))
    return round(gamma, 1)

def set_brightness(brightness):
    os.system(f"pkexec xfpm-power-backlight-helper --set-brightness={brightness}")

def get_idle_time():
    output = os.popen("xprintidle").read()
    idle_time = int(output.strip())
    return idle_time / 1000


def get_max_brightness():
    output = os.popen("pkexec xfpm-power-backlight-helper --get-max-brightness").read()
    max_brightness = int(output.strip())
    return max_brightness

time.sleep(1)
prev_gamma = -1
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
                print(f'new gamma: {gamma}')
                max_brightness = get_max_brightness()
                brightness = int(lerp(int(MIN_BRIGHTNESS * max_brightness), max_brightness, gamma))
                set_brightness(brightness)
                prev_gamma = gamma
                    # print(f"Brightness set to {brightness}, gamma is {round(gamma, 2)}")
                prev_autoajust_time = now
        

    time.sleep(29)