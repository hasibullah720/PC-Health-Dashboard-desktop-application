"""
=============================================================================
PC Health Dashboard - Desktop Application
=============================================================================
A beginner-friendly desktop application built with Python and CustomTkinter
to monitor vital computer statistics (CPU, RAM, Disk, Battery, and System Info)
using the 'psutil' library.
=============================================================================
"""

import os
import platform
import time
import customtkinter as ctk
import psutil

# ---------------------------------------------------------------------------
# Global App Configuration
# ---------------------------------------------------------------------------
# Set modern theme and dark color mode
ctk.set_appearance_mode("Dark")           # Options: "System", "Light", "Dark"
ctk.set_default_color_theme("blue")       # Options: "blue", "green", "dark-blue"


def bytes_to_gb(num_bytes: float) -> str:
    """
    Helper function to convert raw byte values into human-readable Gigabytes (GB).
    1 Gigabyte (GB) = 1024 * 1024 * 1024 bytes.
    """
    gb = num_bytes / (1024 ** 3)
    return f"{gb:.2f} GB"


class PCHealthDashboard(ctk.CTk):
    """
    Main application window class inheriting from CustomTkinter's CTk window.
    Organizes the user interface into card panels and handles data updates.
    """

    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("PC Health Dashboard")
        self.geometry("780x680")
        self.minsize(720, 620)

        # Pre-seed psutil CPU percent reading so interval=None gives an accurate reading
        psutil.cpu_percent(interval=None)

        # Build UI components
        self.create_header()
        self.create_metric_cards()
        self.create_system_info_panel()

        # Load initial values
        self.refresh_metrics()

    # -----------------------------------------------------------------------
    # UI Layout Construction
    # -----------------------------------------------------------------------
    def create_header(self):
        """Creates the top header with title, subtitle, and Refresh button."""
        header_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        # Title & Subtitle container (Left)
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(side="left", fill="y")

        title_label = ctk.CTkLabel(
            title_container,
            text="PC Health Dashboard",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            title_container,
            text="Real-time hardware monitoring & system overview",
            font=ctk.CTkFont(size=12),
            text_color="gray70"
        )
        subtitle_label.pack(anchor="w")

        # Refresh Button container (Right)
        action_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        action_container.pack(side="right", fill="y")

        self.refresh_btn = ctk.CTkButton(
            action_container,
            text="🔄 Refresh",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=120,
            height=38,
            command=self.refresh_metrics
        )
        self.refresh_btn.pack(side="top", pady=(0, 2))

        self.status_label = ctk.CTkLabel(
            action_container,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color="gray60"
        )
        self.status_label.pack(side="top", anchor="e")

    def create_metric_cards(self):
        """Creates a 2x2 grid containing CPU, RAM, Disk, and Battery cards."""
        cards_container = ctk.CTkFrame(self, fg_color="transparent")
        cards_container.pack(fill="both", expand=True, padx=20, pady=5)

        # Configure equal-width columns
        cards_container.grid_columnconfigure(0, weight=1, uniform="group1")
        cards_container.grid_columnconfigure(1, weight=1, uniform="group1")
        cards_container.grid_rowconfigure(0, weight=1)
        cards_container.grid_rowconfigure(1, weight=1)

        # 1. CPU Card
        self.cpu_card = ctk.CTkFrame(cards_container, corner_radius=12)
        self.cpu_card.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        self.setup_cpu_card(self.cpu_card)

        # 2. RAM Card
        self.ram_card = ctk.CTkFrame(cards_container, corner_radius=12)
        self.ram_card.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")
        self.setup_ram_card(self.ram_card)

        # 3. Disk Card
        self.disk_card = ctk.CTkFrame(cards_container, corner_radius=12)
        self.disk_card.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")
        self.setup_disk_card(self.disk_card)

        # 4. Battery Card
        self.battery_card = ctk.CTkFrame(cards_container, corner_radius=12)
        self.battery_card.grid(row=1, column=1, padx=8, pady=8, sticky="nsew")
        self.setup_battery_card(self.battery_card)

    def setup_cpu_card(self, parent):
        """Sets up CPU panel elements."""
        title = ctk.CTkLabel(parent, text="💻 Processor (CPU)", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(anchor="w", padx=15, pady=(12, 4))

        self.cpu_percent_label = ctk.CTkLabel(
            parent,
            text="Usage: 0.0%",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#38bdf8"
        )
        self.cpu_percent_label.pack(anchor="w", padx=15, pady=(2, 6))

        self.cpu_progress = ctk.CTkProgressBar(parent, height=12, corner_radius=6)
        self.cpu_progress.pack(fill="x", padx=15, pady=(0, 10))
        self.cpu_progress.set(0)

        # Cores information
        self.cpu_cores_label = ctk.CTkLabel(
            parent,
            text="Cores: Detecting...",
            font=ctk.CTkFont(size=13),
            text_color="gray85"
        )
        self.cpu_cores_label.pack(anchor="w", padx=15, pady=2)

    def setup_ram_card(self, parent):
        """Sets up RAM (Memory) panel elements."""
        title = ctk.CTkLabel(parent, text="🧠 Memory (RAM)", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(anchor="w", padx=15, pady=(12, 4))

        self.ram_percent_label = ctk.CTkLabel(
            parent,
            text="Usage: 0.0%",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#a78bfa"
        )
        self.ram_percent_label.pack(anchor="w", padx=15, pady=(2, 6))

        self.ram_progress = ctk.CTkProgressBar(parent, height=12, corner_radius=6)
        self.ram_progress.pack(fill="x", padx=15, pady=(0, 10))
        self.ram_progress.set(0)

        self.ram_used_label = ctk.CTkLabel(parent, text="Used RAM: 0.00 GB", font=ctk.CTkFont(size=13))
        self.ram_used_label.pack(anchor="w", padx=15, pady=1)

        self.ram_avail_label = ctk.CTkLabel(parent, text="Available RAM: 0.00 GB", font=ctk.CTkFont(size=13))
        self.ram_avail_label.pack(anchor="w", padx=15, pady=1)

        self.ram_total_label = ctk.CTkLabel(parent, text="Total RAM: 0.00 GB", font=ctk.CTkFont(size=13), text_color="gray70")
        self.ram_total_label.pack(anchor="w", padx=15, pady=1)

    def setup_disk_card(self, parent):
        """Sets up Disk Space panel elements."""
        title = ctk.CTkLabel(parent, text="💾 Storage (Disk)", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(anchor="w", padx=15, pady=(12, 4))

        self.disk_percent_label = ctk.CTkLabel(
            parent,
            text="Usage: 0.0%",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#34d399"
        )
        self.disk_percent_label.pack(anchor="w", padx=15, pady=(2, 6))

        self.disk_progress = ctk.CTkProgressBar(parent, height=12, corner_radius=6)
        self.disk_progress.pack(fill="x", padx=15, pady=(0, 10))
        self.disk_progress.set(0)

        self.disk_used_label = ctk.CTkLabel(parent, text="Used Space: 0.00 GB", font=ctk.CTkFont(size=13))
        self.disk_used_label.pack(anchor="w", padx=15, pady=1)

        self.disk_free_label = ctk.CTkLabel(parent, text="Free Space: 0.00 GB", font=ctk.CTkFont(size=13))
        self.disk_free_label.pack(anchor="w", padx=15, pady=1)

        self.disk_total_label = ctk.CTkLabel(parent, text="Total Space: 0.00 GB", font=ctk.CTkFont(size=13), text_color="gray70")
        self.disk_total_label.pack(anchor="w", padx=15, pady=1)

    def setup_battery_card(self, parent):
        """Sets up Battery panel elements."""
        title = ctk.CTkLabel(parent, text="🔋 Battery Status", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(anchor="w", padx=15, pady=(12, 4))

        self.battery_percent_label = ctk.CTkLabel(
            parent,
            text="Percentage: --%",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#facc15"
        )
        self.battery_percent_label.pack(anchor="w", padx=15, pady=(2, 6))

        self.battery_progress = ctk.CTkProgressBar(parent, height=12, corner_radius=6)
        self.battery_progress.pack(fill="x", padx=15, pady=(0, 10))
        self.battery_progress.set(0)

        self.battery_status_label = ctk.CTkLabel(
            parent,
            text="Power State: Checking...",
            font=ctk.CTkFont(size=13)
        )
        self.battery_status_label.pack(anchor="w", padx=15, pady=1)

        self.battery_note_label = ctk.CTkLabel(
            parent,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray70"
        )
        self.battery_note_label.pack(anchor="w", padx=15, pady=1)

    def create_system_info_panel(self):
        """Creates the bottom panel displaying Computer, OS, and Python details."""
        system_card = ctk.CTkFrame(self, corner_radius=12)
        system_card.pack(fill="x", padx=20, pady=(5, 15))

        title = ctk.CTkLabel(
            system_card,
            text="⚙️ Basic System Information",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        title.pack(anchor="w", padx=15, pady=(10, 4))

        details_container = ctk.CTkFrame(system_card, fg_color="transparent")
        details_container.pack(fill="x", padx=15, pady=(0, 10))
        details_container.grid_columnconfigure((0, 1, 2), weight=1)

        # Hostname / Computer Name
        hostname = platform.node() or "Unknown"
        self.host_label = ctk.CTkLabel(
            details_container,
            text=f"Computer: {hostname}",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        self.host_label.grid(row=0, column=0, sticky="w", pady=2)

        # Operating System
        os_info = f"{platform.system()} {platform.release()}"
        self.os_label = ctk.CTkLabel(
            details_container,
            text=f"OS: {os_info}",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        self.os_label.grid(row=0, column=1, sticky="w", pady=2)

        # Python Version
        py_version = platform.python_version()
        self.py_label = ctk.CTkLabel(
            details_container,
            text=f"Python: v{py_version}",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        self.py_label.grid(row=0, column=2, sticky="w", pady=2)

    # -----------------------------------------------------------------------
    # Hardware Metrics Fetching & Updating
    # -----------------------------------------------------------------------
    def refresh_metrics(self):
        """
        Gathers system telemetry using psutil and updates all GUI cards.
        Handles errors gracefully to ensure continuous, reliable operation.
        """
        self.status_label.configure(text="Updating...", text_color="#38bdf8")
        self.update_idletasks()

        # 1. Update CPU
        try:
            # interval=None calculates CPU utilization non-blockingly since the last check
            cpu_pct = psutil.cpu_percent(interval=None)
            logical_cores = psutil.cpu_count(logical=True) or 0
            physical_cores = psutil.cpu_count(logical=False) or logical_cores

            self.cpu_percent_label.configure(text=f"Usage: {cpu_pct:.1f}%")
            self.cpu_progress.set(min(max(cpu_pct / 100.0, 0.0), 1.0))
            self.cpu_cores_label.configure(
                text=f"Cores: {logical_cores} Total ({physical_cores} Physical)"
            )
        except Exception as e:
            self.cpu_percent_label.configure(text="Usage: Error")
            self.cpu_cores_label.configure(text=f"Cores info unavailable ({e})")

        # 2. Update RAM
        try:
            ram = psutil.virtual_memory()
            self.ram_percent_label.configure(text=f"Usage: {ram.percent:.1f}%")
            self.ram_progress.set(min(max(ram.percent / 100.0, 0.0), 1.0))
            self.ram_used_label.configure(text=f"Used RAM: {bytes_to_gb(ram.used)}")
            self.ram_avail_label.configure(text=f"Available RAM: {bytes_to_gb(ram.available)}")
            self.ram_total_label.configure(text=f"Total RAM: {bytes_to_gb(ram.total)}")
        except Exception as e:
            self.ram_percent_label.configure(text="Usage: Error")
            self.ram_used_label.configure(text=f"RAM error: {e}")

        # 3. Update Disk (Root system drive)
        try:
            # Resolve system root directory ('C:\\' on Windows or '/' on Unix)
            root_path = os.path.abspath(os.sep)
            disk = psutil.disk_usage(root_path)

            self.disk_percent_label.configure(text=f"Usage: {disk.percent:.1f}%")
            self.disk_progress.set(min(max(disk.percent / 100.0, 0.0), 1.0))
            self.disk_used_label.configure(text=f"Used Space: {bytes_to_gb(disk.used)}")
            self.disk_free_label.configure(text=f"Free Space: {bytes_to_gb(disk.free)}")
            self.disk_total_label.configure(text=f"Total Space: {bytes_to_gb(disk.total)} ({root_path})")
        except Exception as e:
            self.disk_percent_label.configure(text="Usage: Error")
            self.disk_used_label.configure(text=f"Disk error: {e}")

        # 4. Update Battery
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                # Desktop PC or machine without battery
                self.battery_percent_label.configure(text="Battery not available", font=ctk.CTkFont(size=18, weight="bold"))
                self.battery_progress.set(0.0)
                self.battery_status_label.configure(text="Power Source: Desktop / AC Power")
                self.battery_note_label.configure(text="No battery detected on this device.")
            else:
                pct = battery.percent
                is_plugged = battery.power_plugged
                self.battery_percent_label.configure(text=f"Level: {pct:.0f}%", font=ctk.CTkFont(size=22, weight="bold"))
                self.battery_progress.set(min(max(pct / 100.0, 0.0), 1.0))

                if is_plugged:
                    if pct >= 99:
                        status_str = "Plugged In (Fully Charged)"
                    else:
                        status_str = "Charging (AC Connected)"
                else:
                    status_str = "Discharging (On Battery)"

                self.battery_status_label.configure(text=f"Power State: {status_str}")
                self.battery_note_label.configure(text="Battery operating normally.")
        except Exception as e:
            self.battery_percent_label.configure(text="Battery not available")
            self.battery_progress.set(0.0)
            self.battery_status_label.configure(text=f"Battery check failed: {e}")

        # Update refresh timestamp
        current_time = time.strftime("%I:%M:%S %p")
        self.status_label.configure(text=f"Updated at {current_time}", text_color="gray60")


# ---------------------------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = PCHealthDashboard()
    app.mainloop()
