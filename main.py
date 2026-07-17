import uvicorn
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import psutil
import socket
import platform
import time
import datetime
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import subprocess
from fastapi import Request
import secrets
from dotenv import load_dotenv
import os

load_dotenv("/home/master/Panel/.env")

security = HTTPBasic()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = secrets.compare_digest(credentials.username, USERNAME)
    correct_pass = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correct_user and correct_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/main")
def index(auth: bool = Depends(check_auth)):
    return FileResponse("static/index.html")

@app.get("/")
def index():
    return RedirectResponse(url="/main")

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
    
@app.get("/info")
def info():
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)
    logs = subprocess.run(
        ["journalctl", "-n", "100", "--no-pager"],
        capture_output=True,
        text=True
    ).stdout
    return {
        "cpu": psutil.cpu_percent(interval=0.5),
        "fan" : get_fan_speed(),
        "temp": get_cpu_temp(),
        "ram": psutil.virtual_memory().percent,
        "disk" : psutil.disk_usage('/').percent,
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "kernel": platform.release(),
        "uptime": str(datetime.timedelta(seconds=uptime_seconds)),
        "myip" : requests.get("https://api.ipify.org?format=json").json()["ip"],
        "track" : "None",
        "status" : "None", 
        "progress" : 0, 
        "position" : "None",
        "length" : "None",
        "volume" : 0,
        "logs" : logs
    }

@app.post("/exec")
async def exec(request: Request):
    data = await request.json()
    print(data["command"])
    if data["command"] == "poweroff":
        subprocess.run(["poweroff"])
    elif data["command"] == "reboot":
        subprocess.run(["reboot"])
    elif data["command"] == "suspend":        
        subprocess.run(["systemctl", "suspend"])
    elif data["command"] == "lock":
        subprocess.run(["hyprlock"])
    elif data["command"] == "playpause":
        subprocess.run(['playerctl', 'play-pause'], capture_output=True, text=True)
    elif data["command"] == "next":
        subprocess.run(['playerctl', 'next'], capture_output=True, text=True)
    elif data["command"] == "prev":
        subprocess.run(['playerctl', 'previous'], capture_output=True, text=True)
    return {
        "message" : "ok"
    }


if __name__ == "__main__":
    while True:
        try:
            uvicorn.run(
                "main:app",
                host="192.168.2.101",
                port=8000,
                reload=False,
                access_log=False
            )
            break
        except Exception as e:
            print(f"{e}")
            time.sleep(3)
