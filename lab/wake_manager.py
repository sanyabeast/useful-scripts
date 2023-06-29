
import dbus

session_bus = dbus.SessionBus()
pm_proxy = session_bus.get_object('org.xfce.PowerManager',
                                  '/org/xfce/PowerManager')
pm_interface = dbus.Interface(pm_proxy,
                              'org.xfce.Power.Manager')

# Отримати поточний таймер засинання
current_sleep_time = pm_interface.GetDisplaySleepTime()

print(current_sleep_time)