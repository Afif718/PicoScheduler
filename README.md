# PicoScheduler

> **Offline Device Task Scheduler for Raspberry Pi Pico W**

A lightweight, fully offline task scheduler for controlling devices using the Raspberry Pi Pico W. Designed for smart home, lab, and IoT projects, PicoScheduler allows you to schedule tasks, control GPIO devices, and manage everything entirely offline with persistent data storage.

<img width="508" height="436" alt="image" src="https://github.com/user-attachments/assets/2c194198-8053-4f75-8f45-f5d5997e177b" />
<img width="401" height="436" alt="image" src="https://github.com/user-attachments/assets/a3e790b4-123b-4823-b4ff-383d9e6f84b1" />
<img width="306" height="440" alt="image" src="https://github.com/user-attachments/assets/9e4fbe12-5790-41f4-b925-773df019d524" />
<img width="413" height="441" alt="image" src="https://github.com/user-attachments/assets/201f9fb6-e92e-4c94-9cc6-12051a3f5504" />


---

## ✨ Features

- **🔌 Offline Scheduling**: Runs entirely on the Pico W without Wi-Fi or external servers
- **💾 Persistent Storage**: All tasks and device configurations stored in JSON files, retained across power cycles
- **🌐 Web Interface**: Lightweight HTML interface served directly by the Pico W
- **🎛️ Device Control**: Easy GPIO control for LEDs, relays, and custom circuits
- **📅 Task Management**: Add, delete, and monitor scheduled tasks
- **⚡ Automatic Switching**: Devices turn on/off automatically based on schedule
- **🔧 Dynamic Devices**: Add new GPIO devices without modifying code
- **⏰ Built-in RTC**: Uses Pico W's real-time clock for reliable offline time tracking

---

## 🎯 Why Raspberry Pi Pico W?

- **Built-in RTC**: Unlike ESP32, the Pico W has a real-time clock peripheral for offline scheduling
- **Cost-effective**: Low-cost microcontroller with multiple GPIOs
- **Offline Operation**: Perfect for environments without network access
- **Ease of Use**: Simple Python programming with MicroPython
- **Reliable**: No dependency on Wi-Fi or cloud services

---

## 🚀 Use Cases

- **🏠 Smart Home Automation**: Control lights, fans, or appliances automatically
- **🔬 Lab Experiments**: Schedule power for sensors, heaters, or pumps
- **🌱 Plant Irrigation**: Water plants on daily or one-time schedules without internet
- **🤖 IoT Prototyping**: Build offline IoT devices with persistent task management
- **📚 Educational Projects**: Demonstrate scheduling and automation concepts

---

## 📂 File Structure

```
PicoScheduler/
│
├── main.py          # Main MicroPython script for web server and scheduling
├── tasks.json       # Stored scheduled tasks (auto-created)
├── devices.json     # Stored devices (auto-created)
├── README.md        # Project documentation
└── LICENSE          # License file
```

---

## 🛠️ Setup Instructions

### 1. Flash MicroPython

1. Download the latest MicroPython firmware for Pico W from [micropython.org](https://micropython.org/download/RPI_PICO_W/)
2. Hold the BOOTSEL button on your Pico W and connect it to your computer via USB
3. Drag and drop the `.uf2` firmware file to the RPI-RP2 drive
4. The Pico W will reboot and appear as a USB serial device

### 2. Upload Files

1. Use Thonny IDE or `ampy` to upload `main.py` to your Pico W
2. `tasks.json` and `devices.json` will be created automatically on first run

### 3. Configure and Run

1. Power on the Pico W
2. Connect to the Pico W's Wi-Fi access point:
   - **SSID**: `PicoW_Scheduler`
   - **Password**: `12345678`
3. Open a browser and navigate to `http://192.168.4.1`
4. Start adding devices and scheduling tasks!

---

## 🖥️ Web Interface Features

### Current Time Display
Shows the Pico W's internal RTC time in real-time.

### Task Management
- **Task Table**: View all scheduled tasks with start/end times and recurrence settings
- **Add Task**: Create new tasks with start time, end time, and recurrence options (once or daily)
- **Delete Task**: Remove individual tasks with a single click

### Device Management
- **Device List**: View all registered GPIO devices
- **Add Device**: Add new GPIO devices dynamically by specifying name and pin number
- **Delete Device**: Remove user-added devices (and their associated tasks)

---

## 📊 Data Persistence

All data is automatically saved to JSON files:

- **tasks.json**: Stores all scheduled tasks
- **devices.json**: Stores all device configurations

Files are updated immediately when tasks or devices are added/deleted, ensuring no data loss during power outages.

---

## 🔌 Hardware Setup Example

```
Raspberry Pi Pico W
│
├── GPIO 15 ──────> LED (via 220Ω resistor) ──> GND
├── GPIO 14 ──────> Relay Module IN ──> Control Device
└── GND ──────────> Common Ground
```

---

## 📝 Usage Example

1. **Add a Device**:
   - Name: `Bedroom Light`
   - GPIO Pin: `15`

2. **Schedule a Task**:
   - Device: `Bedroom Light`
   - Start Time: `18:00`
   - End Time: `22:00`
   - Recurrence: `Daily`

3. The light will automatically turn on at 6 PM and off at 10 PM every day!

---

## ⚠️ Important Notes

- The built-in RTC requires the Pico W to remain powered. For time persistence across power cycles, consider adding a battery-backed external RTC module (e.g., DS3231)
- Fully offline—no Wi-Fi or cloud dependency required for operation
- All changes are immediately written to JSON files for persistence
- Access point mode allows direct connection without requiring a router

---

## 🔮 Future Improvements

- [ ] Battery-backed RTC support for absolute time persistence
- [ ] Task import/export via USB
- [ ] Notification system using buzzer or LED indicators
- [ ] Support for advanced recurrence rules (weekly, monthly patterns)
- [ ] Web interface styling improvements
- [ ] Task logging and history
- [ ] Support for analog sensors and conditional triggers

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [MicroPython](https://micropython.org/)
- Designed for the [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)

---

## 📧 Contact

For questions, suggestions, or feedback, please open an issue on GitHub.

---

**⭐ If you find this project useful, please consider giving it a star!**
