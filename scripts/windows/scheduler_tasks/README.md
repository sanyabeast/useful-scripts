# Windows Task Scheduler XML Templates

This directory contains XML task definition files for Windows Task Scheduler that can be used to automatically run scripts on system events.

## Available Tasks

- **OnStartup.xml** - Runs a script when the system starts up (boot trigger)
- **OnSleep.xml** - Runs a script when the system goes to sleep (Event ID 506)
- **OnWake.xml** - Runs a script when the system wakes up (Event ID 507)

## ⚠️ Important: Script Path Configuration Required

**Before using these task definitions, you MUST modify the script paths to match your actual file locations.**

Each XML file contains hardcoded paths in the `<Arguments>` section that need to be updated:

```xml
<Arguments>-ExecutionPolicy Bypass -File "C:\OS\Scripts\Scheduler\logg.ps1" [event_type]</Arguments>
```

### What you need to change:

1. **Script Path**: Replace `"C:\OS\Scripts\Scheduler\logg.ps1"` with the actual path to your PowerShell script
2. **User ID**: Update the `<UserId>` in the `<Principal>` section to match your Windows user SID
3. **Author**: Optionally update the `<Author>` field with your name

### How to find your User SID:
Run this command in PowerShell:
```powershell
whoami /user
```

## Usage

1. Modify the script paths and user information in the XML files
2. Import the task using Task Scheduler GUI or command line:
   ```cmd
   schtasks /create /xml "path\to\OnStartup.xml" /tn "OnStartup"
   ```
3. Verify the task was created successfully in Task Scheduler

## Notes

- All tasks are configured to run with highest privileges
- Tasks will not stop if the system is running on battery
- Multiple instances of the same task are ignored (won't run simultaneously)
- Tasks have a 72-hour execution time limit
