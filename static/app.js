async function updateStats() { 
    try {
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
        document.querySelector(".valuehost").textContent = data2.host;
        document.querySelector(".valueos").textContent = data2.os;
        document.querySelector(".status").textContent = "🟢 Online";
        document.querySelector(".valuekernel").textContent = data2.kernel;
        document.querySelector(".valuepackages").textContent = data2.packages;
        document.querySelector(".valueshell").textContent = data2.shell;
        document.querySelector(".valuecpu").textContent = data2.cpuname;
        document.querySelector(".valuegpu").textContent = data2.gpu;
        document.querySelector(".valuememory").textContent = data2.eram;
        document.querySelector(".valueswap").textContent = data2.swap;
        document.querySelector(".valuedisk").textContent = data2.diskname;
        document.querySelector(".valuetime").textContent = data2.uptime;
    } catch (error) {
        // Сервер недоступен
        document.querySelector(".status").textContent = "🔴 Offline";
        console.error("Ошибка подключения:", error);
    }
}


setInterval(updateStats, 500);

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

document.querySelector(".poweroff").addEventListener("click", async () => {
    console.log("clicked");
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
