# PicoScheduler

**Offline Device Task Scheduler for Raspberry Pi Pico W**

PicoScheduler is a fully offline automation system built for the Raspberry Pi Pico W. It enables you to control GPIO devices and schedule tasks through a simple web interface—all without requiring internet connectivity, external servers, or a router. The system stores all tasks, device configurations, and persisted time in JSON files, ensuring your setup survives reboots.

## Features

- **Fully Offline Operation** — Functions independently without internet, router, or cloud services
- **Browser-Based Interface** — The Pico W creates a Wi-Fi Access Point for direct browser control
- **Persistent Storage** — Tasks, devices, and RTC time are stored in JSON files and survive power loss
- **GPIO Device Control** — Compatible with LEDs, relays, pumps, motors, and other GPIO-controlled devices
- **Single Task per Device** — Prevents multiple overlapping tasks for the same device
- **Flexible Task Management** — Create and delete one-time or daily recurring schedules
- **Dynamic Device Creation** — Add new devices directly from the UI without code modifications
- **Automatic Time Synchronization** — Receives local time from your browser on connection
- **Internal Time Tracking** — Maintains accurate time using MicroPython's internal timer after initial sync

<img width="234" height="442" alt="image" src="https://github.com/user-attachments/assets/58bcbc6e-dc4c-48c7-9e9a-764de01724d5" />
<img width="401" height="442" alt="image" src="https://github.com/user-attachments/assets/a3e790b4-123b-4823-b4ff-383d9e6f84b1" />
<img width="250" height="442" alt="image" src="https://github.com/user-attachments/assets/e2c6ece3-47d1-4c02-8991-b003bade35e2" />
<img width="250" height="250" alt="image" src="https://github.com/user-attachments/assets/9c222f1f-ce7b-46d3-9bef-88cc4ab3c36c" />

## Time Management System

The Raspberry Pi Pico W does not include a hardware Real-Time Clock (RTC). PicoScheduler addresses this through a hybrid approach:

1. When you open the web interface, your browser transmits the current local time to the Pico
2. The Pico sets its internal clock based on this synchronized time
3. After synchronization, the Pico maintains time offline using MicroPython's millisecond timer (`utime.ticks_ms()`)
4. In the event of power loss, the Pico resets to 00:00 until you reconnect to the interface
5. The Pico persists the last set time in `time.json` so it can restore the RTC on next boot

This design eliminates the need for internet connectivity, NTP servers, or external RTC hardware.

## Why Choose PicoScheduler?

- Immediate offline functionality
- No network infrastructure required
- Persistent device, task, and time storage
- Built on MicroPython for easy customization
- Ideal for automation in remote locations, agricultural applications, laboratory equipment, and offline IoT projects

## Use Cases

- Home automation (lighting, ventilation, relay control)
- Agricultural irrigation and grow room automation
- Laboratory equipment timing and control
- Offline IoT automation projects
- Educational and student projects
- Timed relay-based systems

## Project Structure

```
PicoScheduler/
│
├── main.py          # Web server, scheduler, and GPIO control logic
├── tasks.json       # Auto-generated persistent task storage
├── devices.json     # Auto-generated persistent device storage
├── time.json        # Auto-generated RTC persistence storage
├── README.md        
└── LICENSE
```

## Setup Instructions

### 1. Flash MicroPython Firmware

Download the latest MicroPython firmware for Pico W and flash it using BOOTSEL mode.

### 2. Upload Project Files

Upload `main.py` to your Pico W using Thonny or your preferred method. The `tasks.json`, `devices.json`, and `time.json` files will be generated automatically on first run.

### 3. Run the System

1. Power up the Pico W
2. Connect to the Access Point:
   - **SSID:** `PicoW_Scheduler`
   - **Password:** `12345678`
3. Open your browser and navigate to: `http://192.168.4.1`
4. Your browser will automatically send the current time to the Pico
5. The system is now fully operational offline

## Web Interface Overview

### Time Display
Displays the synchronized local time provided by your browser.

### Task Management
- Create new scheduled tasks (one task per device enforced)
- Delete existing tasks
- Configure one-time or daily recurring schedules

### Device Management
- Add devices by specifying name and GPIO pin
- Control relays and LEDs directly
- Remove user-added devices

## Data Persistence

All data is stored locally on the Pico W:

- `tasks.json` — Stores all scheduled tasks
- `devices.json` — Stores all device configurations
- `time.json` — Stores last synchronized time for RTC restoration

Files are updated immediately upon any changes, ensuring data integrity even in the event of unexpected power loss.

## Hardware Example

```
Pico W
│
├── GPIO 15 → LED/Relay
└── GND
```

## Example Automation Workflow

1. Add device: "Bedroom Lamp" on GPIO 15
2. Create schedule: Turn ON at 18:00, Turn OFF at 22:00
3. System runs indefinitely offline after initial time synchronization

## Important Notes

- Time tracking resets to 00:00 after power loss until the next interface connection
- After reconnection, the Pico restores accurate time from `time.json` and maintains it offline
- Device configurations and task data remain saved regardless of power loss

## Future Development Roadmap

- Hardware RTC module support
- Enhanced UI design
- Weekly and monthly scheduling options
- Sensor integration and conditional automation
- Task execution logging
- Backup and restore utilities

## Contributing

Contributions are welcome. Please submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License.

## Acknowledgments

- MicroPython
- Raspberry Pi Foundation

## Support

If you find this project useful, please consider starring the repository on GitHub.
