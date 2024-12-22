function toggleMenu() {
    const menu = document.getElementById('offcanvasMenu');
    menu.classList.toggle('active');
    isOpen = true;
}

function navbarDisable() {
    const menu = document.getElementById('offcanvasMenu');
    menu.classList.remove('active');
}

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        navbarDisable();
    }
});