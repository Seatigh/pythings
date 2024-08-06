function playCry(pokemonId) {
    const cryUrl = `https://pokeapi.co/media/sounds/cry/${pokemonId}.ogg`;  // URL actualizada para el grito
    const audio = new Audio(cryUrl);
    audio.play();
}

// Función para actualizar la hora en tiempo real
function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    document.getElementById('time').textContent = `${hours}:${minutes}:${seconds}`;
}

// Actualizar el reloj cada segundo
setInterval(updateClock, 1000);
updateClock();  // Llamar una vez para que el reloj se muestre inmediatamente
