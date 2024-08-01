// Función para actualizar la hora cada segundo
function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('time').textContent = timeString;
}

// Actualizar la hora inmediatamente y luego cada segundo
updateTime();
setInterval(updateTime, 1000);
