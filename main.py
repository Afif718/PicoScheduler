import network
import socket
import time
import ujson as json
import machine
from machine import Pin

# -----------------------------
# Configuration
# -----------------------------
TASK_FILE = "tasks.json"
DEVICE_FILE = "devices.json"
TIME_FILE = "time.json"
AP_SSID = "PicoW_Scheduler"
AP_PASSWORD = "12345678"

ALLOWED_GPIO = [0, 1, 2, 3, 4, 5, 12, 13, 14, 15]

led = Pin("LED", Pin.OUT)
REAL_DEVICE_NAME = "Pi LED"

# -------------------------------
# Load or initialize tasks/devices
# -------------------------------
def load_json_file(filename, default):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        with open(filename, "w") as f:
            json.dump(default, f)
        return default

tasks = load_json_file(TASK_FILE, [])
devices = load_json_file(DEVICE_FILE, [{"name": REAL_DEVICE_NAME, "gpio": "LED"}])

# -----------------------------
# Initialize device pins
# -----------------------------
device_pins = {}
for d in devices:
    gpio = d["gpio"]
    try:
        device_pins[d["name"]] = led if gpio == "LED" else Pin(int(gpio), Pin.OUT)
    except:
        print("Failed to initialize device:", d)

DEVICE_ACTION = {d["name"]: f"{d['name']} ON" for d in devices}

# -----------------------------
# Restore persisted time
# -----------------------------
def restore_persisted_time():
    try:
        with open(TIME_FILE, "r") as f:
            data = json.load(f)
        if isinstance(data, list) and len(data) >= 7:
            dt = (data[0], data[1], data[2], data[3], data[4], data[5], data[6], 0)
            try:
                rtc = machine.RTC()
                rtc.datetime(dt)
                print("Restored persisted time:", dt)
            except Exception as e:
                print("RTC restore failed:", e)
    except:
        pass

restore_persisted_time()

# -----------------------------
# Wi-Fi AP Setup
# -----------------------------
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD)
print("AP active. Connect to Wi-Fi:", AP_SSID)

# -----------------------------
# URL decode helper
# -----------------------------
def url_decode(s):
    s = s.replace("+", " ")
    parts = s.split("%")
    result = parts[0]
    for p in parts[1:]:
        try:
            hex_val = p[:2]
            rest = p[2:]
            result += chr(int(hex_val, 16)) + rest
        except:
            result += "%" + p
    return result

def parse_post(data):
    try:
        s = data.decode().split("\r\n\r\n", 1)[1]
        parts = {}
        for kv in s.split("&"):
            if "=" in kv:
                k, v = kv.split("=", 1)
                parts[k] = url_decode(v)
        return parts
    except:
        return {}

# -----------------------------
# Time helpers
# -----------------------------
def is_time_between(start, end, now):
    sh, sm = map(int, start.split(":"))
    eh, em = map(int, end.split(":"))
    nh, nm = map(int, now.split(":"))
    return (sh*60 + sm) <= (nh*60 + nm) < (eh*60 + em)

# -----------------------------
# HTML helpers
# -----------------------------
def status_table(current_time):
    html = "<table style='font-size:12px; width:100%;'><tr><th>Device</th><th>Action</th><th>Start</th><th>End</th><th>Recurrence</th><th>Del</th></tr>"
    for i, t in enumerate(tasks):
        device = t.get("device", "")
        start_time = t.get("start_time", "")
        end_time = t.get("end_time", "")
        recurrence = t.get("recurrence", "")
        action = DEVICE_ACTION.get(device, "ON")
        expired = current_time >= end_time
        row_class = " class='expired'" if expired else ""
        html += f"<tr{row_class}><td>{device}</td><td>{action}</td><td>{start_time}</td><td>{end_time}</td><td>{recurrence}</td>"
        html += f"<td><form action='/delete' method='POST'><input type='hidden' name='index' value='{i}'><button type='submit'>X</button></form></td></tr>"
    html += "</table>"
    return html

def gpio_options_html():
    used = [str(d.get("gpio")) for d in devices if d.get("gpio") and str(d.get("gpio")) != "LED"]
    html = ""
    for g in ALLOWED_GPIO:
        if str(g) not in used:
            html += f"<option value='{g}'>{g}</option>"
    return html

def web_page(current_time):
    html = f"""<html><head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pico W Scheduler</title>
    <style>
    body {{ font-family: Arial, sans-serif; margin:0; padding:18px; display:flex; flex-direction:column; align-items:center; background:#f4f4f4; }}
    h2 {{ margin-top:12px; font-size:20px; color:#333; }}
    .container {{ width:100%; max-width:350px; background:#ffffff; padding:25px; border-radius:12px; box-shadow:0 0 12px rgba(0,0,0,0.12); border-top:6px solid #e84d00; margin-top:14px; }}
    p {{ font-size:14px; margin:0 0 14px 0; color:#222; }}
    form {{ display:flex; flex-direction:column; gap:14px; margin-top:6px; margin-bottom:14px; }}
    label {{ font-size:13px; font-weight:600; color:#333; }}
    input[type=time], select, input[type=text] {{ padding:8px; font-size:14px; border-radius:8px; border:1px solid #ccc; }}
    input[type=submit], button {{ padding:8px; font-size:14px; background:#e84d00; color:white; border:none; border-radius:8px; cursor:pointer; }}
    table {{ width:100%; border-collapse:collapse; margin-top:14px; font-size:12px; }}
    th {{ background:#e84d00; color:white; padding:6px; }}
    td {{ padding:6px; border:1px solid #eee; text-align:center; }}
    .expired {{ background:#ddd; color:#777; }}
    .hidden {{ display:none; }}
    .footer {{ margin-top:10px; font-size:12px; color:#666; text-align:center; }}
    @media (max-width:600px) {{ body {{ padding:14px; }} .container {{ max-width:300px; padding:18px; }} table, th, td {{ font-size:10px; }} }}
    </style>
    </head><body>
    <h2>Device Scheduler</h2>
    <div class="container">
      <p><b>Current Time: {current_time}</b></p>

      <button onclick="document.getElementById('new_device_form').classList.toggle('hidden')">Create New Device</button>
      <form id="new_device_form" class="hidden" action='/newdevice' method='POST'>
        <label>Device Name:</label>
        <input type='text' name='name' required>
        <label>GPIO Pin:</label>
        <select name='gpio' required>{gpio_options_html()}</select>
        <input type='submit' value='Add Device'>
      </form>

      <form action='/' method='POST'>
        <label>Device:</label>
        <select name='device' required>
"""
    # Only allow unscheduled devices
    scheduled_devices = [t.get("device") for t in tasks]
    for d in devices:
        if d["name"] not in scheduled_devices:
            html += f"<option value='{d['name']}'>{d['name']}</option>"

    html += """
        </select>
        <label>Start Time:</label>
        <input type='time' name='start' required>
        <label>End Time:</label>
        <input type='time' name='end' required>
        <label>Recurrence:</label>
        <select name='recurrence'>
          <option value='once'>Once</option>
          <option value='daily'>Daily</option>
        </select>
        <input type='submit' value='Add Task'>
      </form>

      <h3>Devices:</h3>
"""
    for d in devices:
        if d["name"] != REAL_DEVICE_NAME:
            html += f"<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;'>"
            html += f"<span>{d['name']} (GPIO {d['gpio']})</span>"
            html += f"<form style='margin:0;' action='/deletedevice' method='POST'>"
            html += f"<input type='hidden' name='name' value='{d['name']}'><button type='submit'>Delete</button></form></div>"

    html += f"""
      <h3>Scheduled Tasks:</h3>
      <div id="task_table">{status_table(current_time)}</div>
    </div>

    <div class='footer'>Developed by M. H. A. Afif</div>

    <script>
    window.onload = function() {{
        try {{
            const now = new Date();
            fetch(`/settime?hh=${{now.getHours()}}&mm=${{now.getMinutes()}}`);
        }} catch(e){{}}
    }};
    function updateTable() {{
        fetch("/status").then(response => response.text()).then(html => {{
            document.getElementById("task_table").innerHTML = html;
        }});
    }}
    setInterval(updateTable, 5000);
    </script>
    </body></html>
"""
    return html

# -----------------------------
# Web server
# -----------------------------
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
s.settimeout(0.5)
print("Web server running on 0.0.0.0:80")

last_check = 0

while True:
    now_ms = time.ticks_ms()
    if now_ms - last_check >= 1000:
        last_check = now_ms
        now = time.localtime()
        current_time = "{:02d}:{:02d}".format(now[3], now[4])

        for task in tasks[:]:
            device_name = task.get("device", "")
            start_time = task.get("start_time", "")
            end_time = task.get("end_time", "")
            recurrence = task.get("recurrence", "")

            pin = device_pins.get(device_name)
            if pin:
                pin.value(1 if is_time_between(start_time, end_time, current_time) else 0)

            if recurrence == "once" and current_time >= end_time:
                try:
                    tasks.remove(task)
                    with open(TASK_FILE, "w") as f:
                        json.dump(tasks, f)
                    print(f"[{current_time}] One-time task removed: {task}")
                except:
                    pass

    try:
        conn, addr = s.accept()
        request = conn.recv(4096)
        if not request:
            conn.close()
            continue

        try:
            request_line = request.split(b'\r\n')[0].decode()
            path = request_line.split(" ")[1]
        except:
            path = "/"

        if request.startswith(b"GET") and path.startswith("/settime"):
            try:
                hh = int(path.split("hh=")[1].split("&")[0])
                mm = int(path.split("mm=")[1].split("&")[0])
                lt = list(time.localtime())
                rtc_tuple = (lt[0], lt[1], lt[2], lt[6], hh, mm, 0, 0)
                rtc = machine.RTC()
                rtc.datetime(rtc_tuple)
                with open(TIME_FILE, "w") as tf:
                    json.dump(list(rtc_tuple), tf)
                conn.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK')
            except:
                conn.send(b'HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nFAIL')
            conn.close()
            continue

        if request.startswith(b"GET") and b"/status" in request:
            response = status_table(current_time)
            conn.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + response.encode())
            conn.close()
            continue

        if request.startswith(b"POST"):
            form = parse_post(request)

            # Delete task
            if path == "/delete" and "index" in form:
                try:
                    idx = int(form["index"])
                    if 0 <= idx < len(tasks):
                        removed = tasks.pop(idx)
                        pin = device_pins.get(removed.get("device"))
                        if pin: pin.value(0)
                        with open(TASK_FILE, "w") as f:
                            json.dump(tasks, f)
                        print(f"[{current_time}] Task deleted: {removed}")
                except:
                    pass
                conn.send(b'HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n')
                conn.close()
                continue

            # Delete device
            elif path == "/deletedevice" and "name" in form:
                device_name = form["name"]
                if device_name != REAL_DEVICE_NAME:
                    pin = device_pins.get(device_name)
                    if pin: pin.value(0)
                    tasks[:] = [t for t in tasks if t.get("device") != device_name]
                    devices[:] = [d for d in devices if d["name"] != device_name]
                    device_pins.pop(device_name, None)
                    DEVICE_ACTION.pop(device_name, None)
                    with open(TASK_FILE, "w") as f: json.dump(tasks, f)
                    with open(DEVICE_FILE, "w") as f: json.dump(devices, f)
                    print(f"[{current_time}] Device deleted: {device_name}")
                conn.send(b'HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n')
                conn.close()
                continue

            # New device
            elif path == "/newdevice" and all(k in form for k in ("name", "gpio")):
                device_name, gpio_pin = form["name"], form["gpio"]
                if all(d["name"] != device_name and str(d.get("gpio")) != gpio_pin for d in devices):
                    devices.append({"name": device_name, "gpio": gpio_pin})
                    with open(DEVICE_FILE, "w") as f: json.dump(devices, f)
                    DEVICE_ACTION[device_name] = f"{device_name} ON"
                    try: device_pins[device_name] = Pin(int(gpio_pin), Pin.OUT)
                    except: print(f"Failed to create pin for {device_name}")
                    print(f"[{current_time}] New device added: {device_name} GPIO {gpio_pin}")
                conn.send(b'HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n')
                conn.close()
                continue

            # Add task
            elif all(k in form for k in ("device", "start", "end", "recurrence")):
                device_name, new_start, new_end = form["device"], form["start"], form["end"]
                if any(t["device"] == device_name for t in tasks):
                    print(f"[{current_time}] Device already has a task: {device_name}")
                else:
                    tasks.append({
                        "device": device_name,
                        "start_time": new_start,
                        "end_time": new_end,
                        "recurrence": form.get("recurrence", "once")
                    })
                    with open(TASK_FILE, "w") as f: json.dump(tasks, f)
                    print(f"[{current_time}] Task added: {device_name} {new_start}-{new_end}")
                conn.send(b'HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n')
                conn.close()
                continue

        # Default response
        response = web_page(current_time)
        conn.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + response.encode())
        conn.close()
    except Exception as e:
        pass

