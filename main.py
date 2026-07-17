import uvicorn
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from bot import *
import psutil
import socket
import platform
import time
import json
import datetime
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from telegram import InputTextMessageContent,InlineQueryResultArticle, Update
from telegram.ext import InlineQueryHandler, ApplicationBuilder, CommandHandler, MessageHandler, filters, ChatMemberHandler
import subprocess
from fastapi import Request
import secrets
from dotenv import load_dotenv
import os
import pwd
from tools import*

load_dotenv("/home/master/Panel/.env")

security = HTTPBasic()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
OWNER_ID = os.getenv("OWNER_ID")

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

cpu_warn_sent = False
ram_warn_sent = False
temp_warn_sent = False

@app.get("/info")
async def info():
    
    global cpu_warn_sent, ram_warn_sent, temp_warn_sent
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)
    logs = subprocess.run(
        ["journalctl", "-n", "100", "--no-pager"],
        capture_output=True,
        text=True
    ).stdout

    sysinfo = json.loads(subprocess.run(
        ["fastfetch", "--format", "json"],
        capture_output=True,
        text=True
    ).stdout)

    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    temp = get_cpu_temp()

    res = {
        "cpu": psutil.cpu_percent(interval=0.5),
        "fan" : get_fan_speed(),
        "temp": get_cpu_temp(),
        "ram": psutil.virtual_memory().percent,
        "disk" : psutil.disk_usage('/').percent,
        "kernel": platform.release(),
        "uptime": str(datetime.timedelta(seconds=uptime_seconds)),
        "hostname": socket.gethostname(),
        "myip" : requests.get("https://api.ipify.org?format=json").json()["ip"],
        "track" : "None",
        "status" : "None",
        "shell" : pwd.getpwuid(os.getuid()).pw_shell,
        "progress" : 0, 
        "position" : "None",
        "length" : "None",
        "volume" : 0,
        "logs" : logs
    }
    
    # CPU
    if cpu >= 90 and not cpu_warn_sent:
        await bot_app.bot.send_message(
            chat_id=OWNER_ID,
            text=f"⚠️ CPU warning\n\n🖥 Server: {socket.gethostname()}\n🔥 CPU usage: {cpu}%"
        )
        cpu_warn_sent = True

    elif cpu < 85:
        cpu_warn_sent = False


    # RAM
    if ram >= 20 and not ram_warn_sent:
        await bot_app.bot.send_message(
            chat_id=OWNER_ID,
            text=f"⚠️ Memory warning\n\n🖥 Server: {socket.gethostname()}\n🧠 RAM usage: {ram}%"
        )
        ram_warn_sent = True

    elif ram < 85:
        ram_warn_sent = False


    # Температура
    if temp and temp >= 85 and not temp_warn_sent:
        await bot_app.bot.send_message(
            chat_id=OWNER_ID,
            text=f"🌡 CPU temperature warning\n\n🖥 Server: {socket.gethostname()}\n🔥 Temperature: {temp}°C"
        )
        temp_warn_sent = True

    elif temp and temp < 75:
        temp_warn_sent = False


    for item in sysinfo:
        key = item.get("type")

        if key == "OS":
            res["os"] = item["result"]["prettyName"]

        elif key == "Kernel":
            res["kernel"] = item["result"]["name"] + " " + item["result"]["release"]
            res["os"] += " " + item["result"]["architecture"]

        elif key == "Host":
            res["host"] = item["result"]["name"]


        elif key == "Memory":
            res["eram"] = format_bytes(
                item["result"]["used"],
                item["result"]["total"]
            )

        elif key == "Swap":
            used = sum(x["used"] for x in item["result"])
            total = sum(x["total"] for x in item["result"])

            res["swap"] = format_bytes(used, total)
        elif key == "Packages":
            res["packages"] = item["result"]["all"]
        elif key == "GPU":
            res["gpu"] = item["result"][0]["name"]
        elif key == "CPU":
            res["cpuname"] = item["result"]["cpu"]
        elif key == "Disk":
            total = sum(
                disk["bytes"]["total"]
                for disk in item["result"]
            )

            used = sum(
                disk["bytes"]["used"]
                for disk in item["result"]
            )

            res["diskname"] = f" {round(used / 1024**3, 2)} GB / {round(total / 1024**3, 2)} GB"
    return res

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


@app.on_event("startup")
async def startup():
    await start_bot()
    await bot_app.bot.send_message(
        chat_id = OWNER_ID,
        text = f"🟢 {socket.gethostname()} is online"
    )


@app.on_event("shutdown")
async def shutdown():
    await bot_app.bot.send_message(
        chat_id = OWNER_ID,
        text = f"🔴 {socket.gethostname()} is shutting down"
    )
    await stop_bot()

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
