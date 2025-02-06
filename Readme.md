# STM32 + HM-10 BLE Communication with Python Interface

This repository demonstrates how to establish communication between an STM32 Nucleo board and a Python application over BLE using the HM-10 BLE module. The STM32 sends data over BLE, while the Python script receives and processes this data using the `bleak` library.

## Table of Contents

- [Project Overview](#project-overview)
- [STM32 Firmware Details](#stm32-firmware-details)
- [Python Application](#python-application)
- [Requirements](#requirements)
- [How to Use](#how-to-use)
- [Example Output](#example-output)
- [Troubleshooting](#troubleshooting)
- [Author](#author)

## Project Overview
The project is divided into two main components:
1. **STM32 Firmware** <br>
The STM32 Nucleo board is programmed to send "Hello from STM32" periodically via BLE. It uses UART with DMA for efficient communication with the HM-10 BLE module. The firmware also checks for BLE connection status and processes received data.
2. **Python Application (stm.py)** <br>
A Python script using the bleak library to scan for the BLE device (HM-10), connect to it, and receive data. The received data is printed on the console in real-time.


## STM32 Firmware Details
The STM32 firmware is written in C using the HAL library.
It performs the following tasks:

- Initializes UART with DMA for efficient communication.
- Sends periodic messages to the HM-10 BLE module.
- Listens for BLE connection status (OK+CONN / OK+LOST) and updates the connection status.
- Echoes received data over USART2 for debugging.

### Key Functions in main.c:
- Process_Received_Data: Processes incoming data to check for connection status.
- BLE_Check_Connection: Sends "HELLO" periodically to verify BLE connection status.
- Send_Data_Over_BLE: Sends custom messages over BLE.
- DMA and UART Callbacks: Handles DMA-based reception and restarts the process in case of errors.

## Python Application (stm.py)
The Python script scans for the STM32 BLE device and connects to it using the bleak library. It then subscribes to notifications and prints incoming data to the console.

### Main Features:
- Device Scanning and Connection: Scans for devices named "stm32".
- Notification Subscription: Listens for incoming data from the HM-10 BLE module.
- Retry Mechanism: Retries scanning and connecting multiple times before exiting.
- Real-Time Data Display: Displays received data as UTF-8 decoded strings.
### Python Script Breakdown:
- scan_for_device(): Scans for BLE devices and returns the STM32 device if found.
- on_data_received(): Callback function that handles incoming data.
- main(): Establishes the connection and starts listening for data.

## Requirements
### STM32 Firmware
- STM32 Nucleo board (e.g., NUCLEO-F401RE)
- HM-10 BLE module
- STM32CubeMX / STM32CubeIDE
- UART with DMA configured
### Python Script
- Python 3.7+
- `bleak` library for BLE communication 

Install the `bleak` library via pip:
```cpp
pip install bleak
```
## How to Use
### STM32 Firmware
1. Open the STM32 project in STM32CubeIDE.
2. Compile and flash the firmware to the STM32 Nucleo board.
3. Ensure that the HM-10 BLE module is properly connected to the STM32 UART pins.
### Python Application
1. Connect the STM32 Nucleo board to a power source.
2. Run the Python script:
```cpp
python stm.py
```
3. The script will scan for the STM32 BLE device and connect to it.
4. Once connected, incoming data from the STM32 will be displayed in the console.

## Example Output
### STM32 UART Output (Debugging)
```cpp
Received: OK+CONN
BLE connected!
Sent: Hello from STM32
```
### Python Console Output
```cpp
Scanning for BLE devices... (Attempt 1/3)
Found STM32 device: STM32_HM10 (00:1B:44:11:3A:B7)
Connecting to STM32_HM10 (00:1B:44:11:3A:B7)...
Connected to STM32_HM10 (00:1B:44:11:3A:B7)
Data received from 18: Hello from STM32
```

##  Troubleshooting
- **No BLE device found:** Ensure the HM-10 is powered and properly connected to the STM32.
- **Connection fails repeatedly:** Check BLE range and ensure no other device is connected to the HM-10.
- **Data not received:** Verify UART and DMA configuration on the STM32

## Author 
Sakshi Mishra
