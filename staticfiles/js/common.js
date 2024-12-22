const menuToggle = document.getElementById('menu-toggle');
const dropdown = document.getElementById('dropdown');

menuToggle.addEventListener('click', () => {
    dropdown.classList.toggle('hidden');
});