import subprocess
import tkinter as tk
from tkinter import ttk
import time
import tkinter.messagebox as messagebox

# Global variable to store the rtl_fm process
rtl_fm_process = None

# Function to reset the RTL-SDR device using rtl_test
def reset_device():
    """Reset the RTL-SDR device using rtl_test"""
    try:
        # Kill any existing rtl-sdr processes
        subprocess.run("taskkill /F /IM rtl_fm.exe 2>nul", shell=True)
        subprocess.run("taskkill /F /IM rtl_test.exe 2>nul", shell=True)
        time.sleep(2)
        
        # Run rtl_test briefly to reset the device
        test_process = subprocess.Popen("rtl_test -t", shell=True)
        time.sleep(1)
        test_process.terminate()
        test_process.wait()
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Error resetting device: {e}")
        return False

# Function to start/restart rtl_fm
def start_rtl_fm():
    global rtl_fm_process

    # Stop the existing rtl_fm process if it's running
    if rtl_fm_process:
        print("Terminating existing rtl_fm process...")
        try:
            rtl_fm_process.kill()  # Forcefully terminate the process
            rtl_fm_process.wait()  # Wait for the process to terminate
        except Exception as e:
            print(f"Error terminating process: {e}")
        rtl_fm_process = None
        print("Existing rtl_fm process terminated.")
        
        # Reset device after stopping previous process
        if not reset_device():
            messagebox.showerror("Error", "Failed to reset RTL-SDR device. Please disconnect and reconnect it.")
            return

    # Get the values from the GUI
    freq = freq_entry.get()
    gain = gain_entry.get()
    modulation = modulation_var.get()
    sample_rate = sample_rate_var.get()
    ppm = ppm_entry.get() or "0"  # Default to 0 if empty
    
    # Get and validate squelch value
    try:
        squelch_val = float(squelch_entry.get())
        if squelch_val < 0:
            squelch_val = 0
        elif squelch_val > 30:
            squelch_val = 30
        
        # Format to one decimal place
        squelch_val = round(squelch_val, 1)
            
    except ValueError:
        squelch_val = 0
    
    print(f"Setting squelch level to: {squelch_val} dB")

    # Build the rtl_fm command with improved signal processing parameters
    if modulation == "nfm":
        output_rate = sample_rate
    else:
        output_rate = "48"  # Default 48k for WFM
        
    command = f"rtl_fm -d 0 -M {modulation} -f {freq}M -s {sample_rate if modulation == 'nfm' else '200'}k -g {gain} -l {squelch_val} " \
             f"-p {ppm} -A fast -r {output_rate}k -E {'none' if modulation == 'nfm' else 'deemp'} -F 0 -T | " \
             f"\"C:\\Program Files (x86)\\sox-14-4-2\\sox.exe\" -t raw -r {output_rate}k -e s -b 16 -c 1 -V1 - -t waveaudio"
    
    print(f"Starting new rtl_fm process with command: {command}")

    max_retries = 2
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Start rtl_fm in a new process
            rtl_fm_process = subprocess.Popen(command, shell=True)
            print("New rtl_fm process started.")
            time.sleep(1)  # Give it a moment to start
            
            # Check if process is still running
            if rtl_fm_process.poll() is not None:
                raise Exception("Process terminated immediately")
                
            break
        except Exception as e:
            retry_count += 1
            print(f"Attempt {retry_count}: Failed to start rtl_fm process: {e}")
            
            if retry_count < max_retries:
                print("Attempting to reset device...")
                reset_device()
                time.sleep(3)
            else:
                print("Maximum retries reached. Please disconnect and reconnect the RTL-SDR device.")
                messagebox.showerror("Error", "Failed to start RTL-SDR. Please disconnect and reconnect the device.")
                return

# Function to handle the "Scratch" button click
def scratch():
    start_rtl_fm()

# Function to handle window close event
def on_close():
    if rtl_fm_process:
        print("Terminating rtl_fm process on window close...")
        rtl_fm_process.kill()
        rtl_fm_process.wait()
    root.destroy()

def validate_squelch(value):
    if value == "":
        return True
    try:
        val = float(value)
        return 0 <= val <= 30
    except ValueError:
        return False

def increment_squelch():
    try:
        current = float(squelch_entry.get())
        if current < 30:
            new_val = min(30, current + 1)
            squelch_entry.delete(0, tk.END)
            squelch_entry.insert(0, str(new_val))
    except ValueError:
        squelch_entry.delete(0, tk.END)
        squelch_entry.insert(0, "0")

def decrement_squelch():
    try:
        current = float(squelch_entry.get())
        if current > 0:
            new_val = max(0, current - 1)
            squelch_entry.delete(0, tk.END)
            squelch_entry.insert(0, str(new_val))
    except ValueError:
        squelch_entry.delete(0, tk.END)
        squelch_entry.insert(0, "0")

# Function to validate PPM input
def validate_ppm(value):
    if value == "" or value == "-":
        return True
    try:
        val = int(value)
        return -60 <= val <= 60
    except ValueError:
        return False

# Function to increment PPM
def increment_ppm():
    try:
        current = int(ppm_entry.get())
        if current < 60:
            new_val = min(60, current + 1)
            ppm_entry.delete(0, tk.END)
            ppm_entry.insert(0, str(new_val))
    except ValueError:
        ppm_entry.delete(0, tk.END)
        ppm_entry.insert(0, "0")

# Function to decrement PPM
def decrement_ppm():
    try:
        current = int(ppm_entry.get())
        if current > -60:
            new_val = max(-60, current - 1)
            ppm_entry.delete(0, tk.END)
            ppm_entry.insert(0, str(new_val))
    except ValueError:
        ppm_entry.delete(0, tk.END)
        ppm_entry.insert(0, "0")

# Function to handle modulation change
def on_modulation_change(*args):
    if modulation_var.get() == "nfm":
        sample_rate_frame.grid()  # Show NFM sample rate options
        # Set default squelch for NFM
        squelch_entry.delete(0, tk.END)
        squelch_entry.insert(0, "10")
    else:
        sample_rate_frame.grid_remove()  # Hide for WFM mode
        # Set default squelch for WFM
        squelch_entry.delete(0, tk.END)
        squelch_entry.insert(0, "0")

# Create the main window
root = tk.Tk()
root.title("Khanfar FM-NFM")

# Sample rate selection for NFM
sample_rate_var = tk.StringVar(value="50")  # Default sample rate
sample_rate_frame = ttk.LabelFrame(root, text="NFM Sample Rate (kHz)")
sample_rate_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

sample_rate_menu = ttk.Combobox(sample_rate_frame, textvariable=sample_rate_var, 
                               values=["6", "12.5", "20", "25", "50", "100"], 
                               state="readonly", width=10)
sample_rate_menu.grid(row=0, column=0, padx=10, pady=5)

# Frequency input
freq_label = ttk.Label(root, text="Frequency (MHz):")
freq_label.grid(row=0, column=0, padx=10, pady=10)
freq_entry = ttk.Entry(root)
freq_entry.insert(0, "101.3")  # Default frequency
freq_entry.grid(row=0, column=1, padx=10, pady=10)

# Gain input
gain_label = ttk.Label(root, text="Gain (dB):")
gain_label.grid(row=1, column=0, padx=10, pady=10)
gain_entry = ttk.Entry(root)
gain_entry.insert(0, "49.6")  # Default gain
gain_entry.grid(row=1, column=1, padx=10, pady=10)

# Modulation selection
modulation_label = ttk.Label(root, text="Modulation:")
modulation_label.grid(row=2, column=0, padx=10, pady=10)
modulation_var = tk.StringVar(value="wfm")  # Default modulation
modulation_menu = ttk.Combobox(root, textvariable=modulation_var, values=["wfm", "nfm"])
modulation_menu.grid(row=2, column=1, padx=10, pady=10)
modulation_var.trace('w', on_modulation_change)  # Add trace for modulation changes

# Squelch input with validation and buttons
squelch_frame = ttk.LabelFrame(root, text="Squelch Control (0 to 30 dB)")
squelch_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Create a frame for the entry and buttons
squelch_control_frame = ttk.Frame(squelch_frame)
squelch_control_frame.grid(row=0, column=0, padx=5, pady=5)

# Squelch entry with validation
vcmd = (root.register(validate_squelch), '%P')
squelch_entry = ttk.Entry(squelch_control_frame, width=8, validate='key', validatecommand=vcmd)
squelch_entry.insert(0, "10" if modulation_var.get() == "nfm" else "0")  # Default based on mode
squelch_entry.grid(row=0, column=1, padx=2)

# Add up/down buttons
down_button = ttk.Button(squelch_control_frame, text="-", width=2, command=decrement_squelch)
down_button.grid(row=0, column=0, padx=2)

up_button = ttk.Button(squelch_control_frame, text="+", width=2, command=increment_squelch)
up_button.grid(row=0, column=2, padx=2)

ttk.Label(squelch_control_frame, text="dB").grid(row=0, column=3, padx=2)

# PPM correction frame
ppm_frame = ttk.LabelFrame(root, text="PPM Correction (-60 to +60)")
ppm_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Create a frame for PPM entry and buttons
ppm_control_frame = ttk.Frame(ppm_frame)
ppm_control_frame.grid(row=0, column=0, padx=5, pady=5)

# PPM entry with validation
vcmd_ppm = (root.register(validate_ppm), '%P')
ppm_entry = ttk.Entry(ppm_control_frame, width=8, validate='key', validatecommand=vcmd_ppm)
ppm_entry.insert(0, "0")
ppm_entry.grid(row=0, column=1, padx=2)

# Add PPM up/down buttons
ppm_down_button = ttk.Button(ppm_control_frame, text="-", width=2, command=decrement_ppm)
ppm_down_button.grid(row=0, column=0, padx=2)

ppm_up_button = ttk.Button(ppm_control_frame, text="+", width=2, command=increment_ppm)
ppm_up_button.grid(row=0, column=2, padx=2)

ttk.Label(ppm_control_frame, text="ppm").grid(row=0, column=3, padx=2)

# Scratch button
scratch_button = ttk.Button(root, text="Scratch", command=scratch)
scratch_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Handle window close event
root.protocol("WM_DELETE_WINDOW", on_close)

# Start the GUI event loop
root.mainloop()