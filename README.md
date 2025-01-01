# Khanfar FM-NFM RTL-SDR Controller

A powerful GUI application for controlling RTL-SDR devices with support for both FM and NFM reception.

Developed by Khanfar Systems

## Features

- FM and NFM reception modes
- Adjustable sample rates for NFM (6k, 12.5k, 20k, 25k, 50k, 100k)
- Squelch control (0-30 dB) with default 10 dB for NFM
- PPM correction (-60 to +60)
- Gain control
- Bias-T support

## Requirements

- Windows Operating System
- Python 3.6 or higher
- RTL-SDR device
- RTL-SDR drivers and utilities
- SoX audio processor

## Installation

1. Install RTL-SDR Drivers:
   - Download and install Zadig (https://zadig.akeo.ie/)
   - Connect your RTL-SDR device
   - Run Zadig and install the WinUSB driver for your RTL-SDR

2. Install SoX:
   - Download SoX from https://sourceforge.net/projects/sox/
   - Install to the default location (C:\Program Files (x86)\sox-14-4-2\)

3. Install Python Dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Connect your RTL-SDR device
2. Open Command Prompt in the application directory
3. Run:
   ```
   python control.py
   ```

## Usage Instructions

1. Select Mode:
   - WFM: For regular FM radio broadcasts
   - NFM: For narrow-band FM communications

2. NFM Settings:
   - Default squelch: 10 dB (adjustable 0-30 dB)
   - Sample rates: Choose based on channel bandwidth
     * 12.5k for narrow channels
     * 25k for standard channels
     * Higher rates for better audio quality

3. PPM Correction:
   - Range: -60 to +60
   - Adjust if frequencies seem off
   - Positive: If received frequency is lower than expected
   - Negative: If received frequency is higher than expected

4. Gain:
   - Start with 49.6 dB
   - Reduce if receiving strong signals
   - Increase for weak signals

## Troubleshooting

1. No Device Found:
   - Check USB connection
   - Reinstall drivers using Zadig
   - Reset device using the application

2. No Audio:
   - Check Windows audio settings
   - Verify sample rate settings
   - Adjust squelch level

3. Poor Reception:
   - Adjust gain settings
   - Try different sample rates
   - Adjust PPM correction
   - Check antenna connection

## Support

For issues and support, please contact Khanfar Systems.

## License

Copyright © 2024 Khanfar Systems. All rights reserved.
