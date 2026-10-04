# PC Health Dashboard Desktop Application

A modern, beginner-friendly desktop application built with **Python**, **CustomTkinter**, and **psutil**. It displays real-time health metrics and hardware diagnostics in clean card-based panels.

---

## Features

- **CPU Information**: Real-time CPU usage percentage (with color-coded progress bar) and total/physical core counts.
- **RAM Information**: Live memory usage percentage, used RAM, available RAM, and total installed memory (in GB).
- **Disk Information**: Root drive storage usage percentage, used space, free space, and total drive capacity (in GB).
- **Battery Information**: Battery charge percentage, power state (Charging, Plugged In, or Discharging). Gracefully handles desktop PCs with no battery by displaying *"Battery not available"* without errors.
- **System Overview**: Computer name / hostname, operating system, and installed Python version.
- **Refresh Action**: Prominent Refresh button to instantly update all telemetry data, with an "Updated at" timestamp.
- **Error Resilient**: All metrics are wrapped in safe exception handlers to prevent crashes if a hardware sensor is inaccessible.

---

## Project Structure

```text
PC Health Dashboard desktop application/
│
├── main.py              # Main desktop application code (CustomTkinter GUI + psutil)
├── requirements.txt     # Python dependencies (psutil, customtkinter)
└── README.md            # Setup, execution, and build guide
```

---

## 1. Setup & Installation (Inside Virtual Environment)

Open **PowerShell** or **Command Prompt** in this project folder:

### Step 1: Create a Virtual Environment (`.venv`)
```powershell
python -m venv .venv
```

### Step 2: Activate the Virtual Environment
- **On Windows (PowerShell)**:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  *(If PowerShell displays an ExecutionPolicy warning, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

- **On Windows (Command Prompt)**:
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

### Step 3: Install Required Packages
```powershell
pip install psutil customtkinter
```
*(Or install via `pip install -r requirements.txt`)*

---

## 2. Running the Application

Make sure your `.venv` is activated, then run:

```powershell
python main.py
```

The desktop dashboard window will open with dark mode cards and live statistics! Click the **🔄 Refresh** button anytime to update metrics.

---

## 3. Creating a Standalone Windows Executable (.exe) with PyInstaller

You can bundle this application into a standalone `.exe` file that runs on any compatible Windows PC without needing Python installed.

### Step 1: Install PyInstaller in the `.venv`
```powershell
pip install pyinstaller
```

### Step 2: Build the `.exe`
Run the following command:

```powershell
pyinstaller --noconfirm --onefile --windowed --collect-all customtkinter main.py
```

> **Flag Explanation**:
> - `--onefile`: Packages the entire application and its dependencies into a single `.exe` file.
> - `--windowed`: Suppresses the background command prompt console so it launches cleanly as a standard Windows desktop application.
> - `--collect-all customtkinter`: Ensures CustomTkinter's dark/light themes and font assets are bundled inside the executable.
> - `--noconfirm`: Automatically replaces any existing build files.

### Step 3: Run the Executable
Once the build finishes:
1. Open the `dist` folder created in your project directory:
   ```powershell
   explorer .\dist
   ```
2. Double-click **`main.exe`**.
3. The dashboard will launch immediately as a native desktop application!
