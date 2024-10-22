// $(document).ready(function() {
//     console.log("Document ready!");
//     // Additional JS functionalities can go here
// });

// A function to toggle the open on hambuger and nav
const hamburger = document.getElementById('hamburger');
const navbar = document.getElementById('navbar');

hamburger.addEventListener('click', () => {
    navbar.classList.toggle('open');
});

// A function to toggle light and darkmode
const darkmodeToggle = document.getElementById('darkmodeToggle');
const body = document.getElementById('body');
const listGroupItem = document.getElementById('list-group-item');

const currentTheme = localStorage.getItem('theme');

if (currentTheme === 'dark') {
    toggleMode();
}

function toggleMode() {
    body.classList.toggle('dark-mode');
    darkmodeToggle.classList.toggle('dark-mode');
    hamburger.classList.toggle('dark-mode');
    navbar.classList.toggle('dark-mode');

    if (listGroupItem !== null) {
        listGroupItem.classList.toggle('dark-mode');
    }
}

darkmodeToggle.addEventListener('click', () => {
    toggleMode();
    // Save user preference in localStorage
    const theme = darkmodeToggle.classList.contains('dark-mode') ? 'dark' : 'light';
    localStorage.setItem('theme', theme);
})
