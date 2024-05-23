# Archive Monitor

This script monitors a directory for new `.zip` or `.rar` files, extracts them using WinRAR, and then deletes the archive files after extraction.

## Requirements

- Python 3.x
- watchdog
- WinRAR

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Alm0stEthical/archive-monitor.git
   cd archive-monitor
   ```

2. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Ensure WinRAR is installed and accessible at `C:\Program Files\WinRAR\WinRAR.exe`.

## Usage
Run the script:
```sh
python archive_monitor.py
```

## Running the Script in the Background and on Startup
To run this script in the background and start it automatically on system startup, follow these steps:

### Step 1: Create a Batch File

1. Create a new file named `run_archive_monitor.bat` in the same directory as your script.
2. Add the following lines to the batch file:

```bat
@echo off
py C:\Path\To\Your\PythonScript\main.py
```

### Step 2: Create a VBScript to Run the Batch File Silently

1. Create a new file named `run_archive_monitor.vbs` in the same directory as your script.
2. Add the following lines to the VBScript file:

    ```vbscript
    Set WshShell = CreateObject("WScript.Shell")
    WshShell.Run "C:\Path\To\Your\Batch\run_archive_monitor.bat", 0, False
    ```

    - Make sure to replace `C:\Path\To\Your\Batch\run_archive_monitor.bat` with the full path to the batch file you created.

### Step 3: Add the VBScript to the Startup Folder

1. Press `Win + R` to open the Run dialog.
2. Type `shell:startup` and press Enter. This will open the Startup folder.
3. Move the `run_archive_monitor.vbs` file into the Startup folder.

### How It Works

1. **Monitor Directory**: The script monitors the `Downloads` directory of the current user for any new `.zip` or `.rar` files.
2. **Wait for File**: If a new archive file is detected, the script waits until the file is no longer in use.
3. **Extract and Delete**: The script extracts the contents of the archive file to a directory with the same name as the archive (without the extension) and then deletes the archive file.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
