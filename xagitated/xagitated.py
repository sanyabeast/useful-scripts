# created by @sanyabeast, 2023, Ukraine

import datetime
import subprocess
import time
import os
import yaml
from deepmerge import always_merger
import psutil
import argparse
import pprint
import pyautogui

pp = pprint.PrettyPrinter(indent=4)

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='xagitated')
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
args = parser.parse_args()
IS_DEBUG = args.debug

# intristinct valus
DEFAULT_CONFIG = {
  "sleep_timeout": 999,
  "cpu_usage_treshold": 10,
  "standard_inhibitors": [
    "audio_payback",
    "cpu_usage",
    "network_activity",
    "fullscreen_app"
  ],
  "apps": [
    "deluge"
  ],
  "defaults": {
    "sleep_timeout": 2
  }
}

MAIN_TICK_DURATION = 29
AC_CHECK_INTERVAL = 51
AUDIO_CHECK_INTERVAL = 29
CPU_CHECK_INTERVAL = 15
NETWORK_CHECK_INTERVAL = 55
USER_CHECK_INTERVAL = 1
TTS_CHECK_INTERVAL = 5

# get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# load the YAML file
with open(os.path.join(os.path.expanduser('~/.config'), 'xagitated.yaml'), 'r') as file:
    CONFIG = yaml.safe_load(file)

CONFIG = always_merger.merge(DEFAULT_CONFIG, CONFIG)

def logd(*args):
    if IS_DEBUG:
        now = datetime.datetime.now().strftime('%H:%M:%S')
        print('\033[35m' + f'[xagitated] [{now}]' + '\033[0m', *args)

def run_command(command, *args):
    command = command.format(*args)
    try:
        result = subprocess.check_output(command, shell=True)
        return result.decode().strip()
    except subprocess.CalledProcessError as e:
        logd(f"Command failed: {e}")
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
    
def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

class Commands:
    get_inactivity_on_battery = "xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/inactivity-on-battery"
    set_inactivity_on_battery = "xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/inactivity-on-battery -s {}"
    restart_pm = "xfce4-power-manager --restart"
    suspend_system = "xfce4-session-logout --suspend"
    get_idle_time = "xprintidle"

class PowerManager:
    def __init__(self) -> None:
        if IS_DEBUG:
            logd('starting agitated power manager in debug mode')
        else:
            logd('starting agitated power manager normally')
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
            self._is_power_supplied = 'on-line' in subprocess.check_output(['acpi', '-a']).decode().strip()
            logd(f'ac connection state updated: {self._is_power_supplied}')
        return self._is_power_supplied

    # audio check
    _is_audio_playing = None
    @property
    def is_audio_playing(self):
        if timer_gate('audio_check', AUDIO_CHECK_INTERVAL) or self._is_audio_playing == None:
            self._is_audio_playing = 'State: RUNNING' in  subprocess.check_output(['pactl', 'list']).decode()
            logd(f'audio payback status update: {self._is_audio_playing}')
        return self._is_audio_playing

    # cpu check
    _cpu_usage = None
    @property
    def cpu_usage(self):
        if timer_gate('cpu_check', CPU_CHECK_INTERVAL) or self._cpu_usage == None:
            self._cpu_usage = cpu_usage = psutil.cpu_percent()
            logd(f'cpu usage update: {self._cpu_usage}%')
        return self._cpu_usage

    # network check
    _network_activity = None
    @property
    def network_activity(self):
        if timer_gate('network_check', NETWORK_CHECK_INTERVAL) or self._network_activity == None:
            inf = CONFIG['network_interface']
            net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
            net_in_1 = net_stat.bytes_recv
            net_out_1 = net_stat.bytes_sent
            time.sleep(1)
            net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
            net_in_2 = net_stat.bytes_recv
            net_out_2 = net_stat.bytes_sent
            net_in = round((net_in_2 - net_in_1) / 1024, 0)
            net_out = round((net_out_2 - net_out_1) / 1024, 0)
            self._network_activity = int(net_in + net_out)
            logd(f'network_activity update: {self._network_activity} kb/s')
        return self._network_activity
    
    # user check
    _user_activity = None
    @property
    def user_activity(self):
        if timer_gate('user_check', USER_CHECK_INTERVAL) or self._user_activity == None:
            self._user_activity = round(clamp(1 - (float(run_command(Commands.get_idle_time)) / 1000 / 60) / CONFIG['defaults']['sleep_timeout'], 0, 1), 2)
            logd(f'user activity update: {self._user_activity}%')
        return self._user_activity
    
    # user check
    _time_to_sleep = None
    @property
    def time_to_sleep(self):
        if timer_gate('tts_check', TTS_CHECK_INTERVAL) or self._time_to_sleep == None:
            inactivity_timeout = (CONFIG['sleep_timeout'] if self.is_agitated else CONFIG['defaults']['sleep_timeout']) * 60
            inactivity_time = float(run_command(Commands.get_idle_time)) / 1000
            self._time_to_sleep = round(inactivity_timeout - inactivity_time, 2)
            print(f'ff {inactivity_timeout}, gg {inactivity_time}')
            logd(f'tts update: {self._time_to_sleep} s')
        return self._time_to_sleep

    # activity simulation
    def simulate_activity(self):
        logd('simulating user activity')
        pyautogui.moveRel(1, 0)
        time.sleep(1/120)
        pyautogui.moveRel(-1, 0)

    # agitation and chilling
    is_agitated = False 
    def agitate(self, reason = ""):
        if not self.is_agitated:
            self.inactivity_timeout = CONFIG['sleep_timeout']
            self.is_agitated = True
            logd(f'AGITATED!. reason: "{reason}"')
    def chill(self):
        if self.is_agitated:
            self.inactivity_timeout = CONFIG['defaults']['sleep_timeout']
            self.is_agitated = False
            if (self.user_activity < 0.15):
                self.simulate_activity()
            logd(f'*CHILLED*.')
    # rolling things back
    def reset(self):
        logd('applying default settings')
        self.chill()

    def update(self):
        if timer_gate('main_tick', MAIN_TICK_DURATION):
            if IS_DEBUG or not self.is_power_supplied:
                if 'audio_payback' in CONFIG['standard_inhibitors'] and self.is_audio_playing:
                    self.agitate('audio payback')
                elif 'cpu_usage' in CONFIG['standard_inhibitors'] and self.cpu_usage >= CONFIG['cpu_usage_treshold']:
                    self.agitate(f'cpu usage ({self.cpu_usage})')
                elif 'network_activity' in CONFIG['standard_inhibitors'] and self.network_activity >= CONFIG['network_activity_treshold']:
                    self.agitate(f'network activity ({self.network_activity})')
                else:
                    self.chill()

power_looper = PowerManager()

if IS_DEBUG:
    pp.pprint(CONFIG)
    print('DEBUG MODE')

while True:
    try:
        while True:
            power_looper.update()
            time.sleep(1)
    except KeyboardInterrupt:
        power_looper.reset()
        break
    


    