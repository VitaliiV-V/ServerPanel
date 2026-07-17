async function updateStats() { 

    const response2 = await fetch("http://192.168.2.101:8000/info");
    const data2 = await response2.json();
    document.querySelector(".cpuval").textContent = data2.cpu + "%";
    document.querySelector(".cpubar2").style.width = data2.cpu + "%";
    document.querySelector(".ramval").textContent = data2.ram + "%";
    document.querySelector(".rambar2").style.width = data2.ram + "%";
    document.querySelector(".diskval").textContent = data2.disk + "%";
    document.querySelector(".diskbar2").style.width = data2.disk + "%";
    document.querySelector(".tempval").textContent = data2.temp + "°C";
    document.querySelector(".fanval").textContent = data2.fan + " RPM";
    document.querySelector(".tempbar2").style.width = data2.temp + "%";
    document.querySelector(".fanbar2").style.width = 50 + "%";
    document.querySelector(".logs").value = data2.logs;
    document.querySelector(".valueip").textContent = data2.myip;
    document.querySelector(".valuehost").textContent = data2.hostname;
    document.querySelector(".valueos").textContent = data2.os;
    document.querySelector(".valuekernel").textContent = data2.kernel;
    document.querySelector(".valuepackages").textContent = data2.packages;
    document.querySelector(".valueshell").textContent = data2.shell;
    document.querySelector(".valuecpu").textContent = data2.cpuname;
    document.querySelector(".valuegpu").textContent = data2.gpu;

    document.querySelector(".valuedisk").textContent = data2.diskname;
    document.querySelector(".valuetime").textContent = data2.uptime;
    document.querySelector(".trackname").textContent = data2.track;
    document.querySelector(".position").textContent = data2.position;
    document.querySelector(".length").textContent = data2.length;
    document.querySelector(".vol").textContent = data2.volume + '%';

    if(data2.status == "Playing\n") {
        document.querySelector(".btn-play").innerHTML =
          '<i class="fas fa-pause" style="font-size: 40px; padding-right: 5px;"></i>';   } else {
        document.querySelector(".btn-play").innerHTML =
          '<i class="fas fa-play" style="font-size: 40px;"></i>';
    }
    const slider = document.querySelector(".slider");

    slider.value = data2.progress;

    const volume = document.querySelector(".volume");

    volume.value = data2.volume;


}


setInterval(updateStats, 500);

document.querySelector(".volume").addEventListener("change", function () {
  console.log("Финальное значение:", slider.value);
});

document.querySelector(".reboot").addEventListener("click", async () => {

    const ok = confirm("Are you sure you want to reboot your computer?");
    if (!ok) return;

    const response = await fetch("http://192.168.2.101:8000/exec", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "command": "reboot",
        })
    })
});


document.querySelector(".suspend").addEventListener("click", async () => {

    const ok = confirm("Are you sure you want to suspend your computer?");
    if (!ok) return;

    const response = await fetch("http://192.168.2.101:8000/exec", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "command": "suspend",
        })
    })
});

document.querySelector(".poweroff").addEventListener("click", async () => {
    const ok = confirm("Are you sure you want to turn off your computer?");

    if (!ok) return;

    const response = await fetch("http://192.168.2.101:8000/exec", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "command": "poweroff",
        })
    })

});

document.querySelector(".lock").addEventListener("click", async () => {

    const ok = confirm("Are you sure you want to lock your computer?");
    if (!ok) return;

    const response = await fetch("http://192.168.2.101:8000/exec", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "command": "lock",
        })
    })
});



document.querySelector(".btn-play").addEventListener("click", async () => {
    const response = await fetch("http://192.168.2.101:8000/exec", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "command": "playpause",
        })
    })
});

document.querySelector(".btn-next").addEventListener("click", async () => {
    const response = await fetch("http://192.168.2.101:8000/exec", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "command": "next",
        })
    })
});

document.querySelector(".btn-prev").addEventListener("click", async () => {
    const response = await fetch("http://192.168.2.101:8000/exec", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "command": "previous",
        })
    })
});


function toggleTheme() {
    document.body.classList.toggle("dark");

    const icon = document.getElementById("themeIcon");
    const isDark = document.body.classList.contains("dark");

    if (isDark) {
        icon.classList.remove("fa-moon");
        icon.classList.add("fa-sun");
    } else {
        icon.classList.remove("fa-sun");
        icon.classList.add("fa-moon");
    }

    localStorage.setItem(
        "theme",
        document.body.classList.contains("dark") ? "dark" : "light"
    );
}

window.onload = () => {
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark");
    }
};
