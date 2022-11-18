function openMenu() {
        document.getElementById('menu').classList.toggle('show');
}

window.onclick = function (event) {
    if (!event.target.matches('#menu-button')) {
        let dropdown = document.getElementById('menu');
        if (dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    }
}