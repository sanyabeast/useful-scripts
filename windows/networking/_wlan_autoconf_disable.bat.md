Disable Wi-Fi Autoconfiguration Script (Windows)

This batch script disables the automatic configuration of your Windows Wi-Fi adapter. This can be useful if you want to prevent your computer from automatically connecting to nearby networks or configuring network settings.

**How it Works**

1. Run the script by double-clicking on `wlan_autoconf_disable.bat` and follow the prompts.
2. The script will check for administrative permissions and request them if necessary.
3. Once granted, the script will use the Windows command-line utility `netsh` to disable Wi-Fi autoconfiguration.

**Prerequisites**

* This script is designed for Windows operating systems only.
* You must have administrative privileges on your computer to run this script successfully.