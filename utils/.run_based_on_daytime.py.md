
**Run Command Based on Daytime**
=============================

A Python script that runs a command based on the current time of day.

**Usage**

1. Run the script from the command line: `python run_based_on_daytime.py DAY_START_HOUR DAY_END_HOUR DAY_COMMAND NIGHT_COMMAND`
2. The script will execute one of two commands depending on whether it's daytime or nighttime:
	* If the current hour is between `DAY_START_HOUR` and `DAY_END_HOUR`, the `DAY_COMMAND` will be executed.
	* Otherwise, the `NIGHT_COMMAND` will be executed.

**Example**

Suppose you want to run a command during daylight hours (6am-8pm) and another command at night. You can use this script like so:

```
python run_based_on_daytime.py 6 20 "command1.sh" "command2.sh"
```

In this example, the `DAY_COMMAND` would be `"command1.sh"` and the `NIGHT_COMMAND` would be `"command2.sh"`.

**Note**

* The script assumes that the current hour is in a 24-hour format (e.g. 0-23).
* You can adjust the `day_start` and `day_end` variables to change the daylight hours.
* Make sure to enclose your commands in quotes if they contain spaces or special characters.