import psutil

def get_cpu_temp():
    temps = psutil.sensors_temperatures()

    for chip, entries in temps.items():
        for e in entries:
            # отбрасываем отключённые датчики
            if e.current is not None and 0 < e.current < 120:
                return e.current

    return None

def get_fan_speed():
    try:
        with open("/sys/class/hwmon/hwmon0/fan1_input") as f:
            return int(f.read().strip())
    except:
        return None

def format_bytes(used, total):
    units = ["B", "KB", "MB", "GB", "TB"]

    def convert(value):
        size = float(value)
        for unit in units:
            if size < 1024:
                return f"{round(size, 2)} {unit}"
            size /= 1024
        return f"{round(size, 2)} PB"

    return f"{convert(used)} / {convert(total)}"