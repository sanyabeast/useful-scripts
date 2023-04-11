# created by @sanyabeast, 2023, Ukraine

import subprocess
import time
import os
import yaml
from deepmerge import always_merger

# intristinct valus
DEFAULT_CONFIG = {
  "debug": False,
  "sleep_timeout": 999,
  "standard_inhibitors": [
    "audio_payback",
    "cpu_load",
    # "network_activity",
    "fullscreen_app"
  ],
  "apps": [
    # "deluge"
  ],
  "defaults": {
    "sleep_timeout": 2
  }
}

MAIN_TICK_DURATION = 29
AC_CHECK_INTERVAL = 59
AUDIO_CHECK_INTERVAL = 29

# get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# load the YAML file
with open(os.path.join(os.path.expanduser('~/.config'), 'agitated.yaml'), 'r') as file:
    CONFIG = yaml.safe_load(file)

CONFIG = always_merger.merge(DEFAULT_CONFIG, CONFIG)
IS_DEBUG = CONFIG['debug']

# access the data
print(CONFIG)

def run_command(command, *args):
    command = command.format(*args)
    try:
        result = subprocess.check_output(command, shell=True)
        return result.decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None

timer_gate_ids = {}
def timer_gate(id, timeout):
    current_time = time.monotonic()
    last_called_time = timer_gate_ids.get(id, 0)
    
    if current_time - last_called_time >= timeout:
        timer_gate_ids[id] = current_time
        return True
    else:
        return False

class Commands:
    get_inactivity_on_battery = "xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/inactivity-on-battery"
    set_inactivity_on_battery = "xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/inactivity-on-battery -s {}"
    restart_pm = "xfce4-power-manager --restart"
    suspend_system = "xfce4-session-logout --suspend"

class PowerManager:
    def __init__(self) -> None:
        if CONFIG['defaults']:
            print('starting agitated power manager in debug mode')
        else:
            print('starting agitated power manager normally')
    # inactivity timeout
    @property
    def inactivity_timeout(self):
        return int(run_command(Commands.get_inactivity_on_battery))
    @inactivity_timeout.setter
    def inactivity_timeout(self, new_value):
        if new_value == None or new_value <= 0:
            new_value = CONFIG['sleep_timeout']
        run_command(Commands.set_inactivity_on_battery, new_value)
    
    _is_power_supplied = None
    @property
    def is_power_supplied(self):
        # Run the acpi command and capture the output
        if timer_gate('ac_check', AC_CHECK_INTERVAL) or self._is_power_supplied == None:
            self._is_power_supplie = 'on-line' in subprocess.check_output(['acpi', '-a']).decode().strip()
        return self._is_power_supplied

    # audio check
    _is_audio_playing = None
    @property
    def is_audio_playing(self):
        if timer_gate('audio_check', AUDIO_CHECK_INTERVAL) or self._is_audio_playing == None:
            self._is_audio_playing = 'State: RUNNING' in  subprocess.check_output(['pactl', 'list']).decode()
        return self._is_audio_playing

    # agitation and relaxing
    is_agitated = False 
    def agitate(self):
        if not self.is_agitated:
            self.inactivity_timeout = CONFIG['sleep_timeout']
            self.is_agitated = True
    def relax(self):
        if self.is_agitated:
            self.inactivity_timeout = CONFIG['defaults']['sleep_timeout']
            self.is_agitated = False
    # rolling things back
    def reset(self):
        print('applying default settings')
        self.relax()

    def update(self):
        if timer_gate('main_tick', MAIN_TICK_DURATION):
            if IS_DEBUG or not self.is_power_supplied:
                if IS_DEBUG:
                    print('main tick')

                if 'audio_payback' in CONFIG['standard_inhibitors'] and self.is_audio_playing:
                    print('agitate due audio payback')
                    self.agitate()
                else:
                    self.relax()


power_looper = PowerManager()

while True:
    try:
        while True:
            power_looper.update()
    except KeyboardInterrupt:
        power_looper.reset()
        break
    


    