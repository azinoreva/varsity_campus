// A function to toggle light and darkmode
const darkmodeToggle = document.getElementById('darkmodeToggle');
const body = document.getElementById('body');
const offcanvasExample = document.getElementById('offcanvasExample');
const hamburger = document.getElementById('hamburger');
const searchBar = document.getElementById('search-bar');
const listGroupItems = document.querySelectorAll('.list-group-item');

const currentTheme = localStorage.getItem('theme');

if (currentTheme === 'dark') {
    toggleMode();
}

function toggleMode() {
    body.classList.toggle('dark-mode');
    darkmodeToggle.classList.toggle('dark-mode');
    hamburger.classList.toggle('dark-mode');
    offcanvasExample.classList.toggle('dark-mode');

    if (searchBar) {
        searchBar.classList.toggle('dark-mode');
    }

    listGroupItems.forEach((item) => {
        item.classList.toggle('dark-mode');
    })
    
}

if (darkmodeToggle) {
    darkmodeToggle.addEventListener('click', () => {
        toggleMode();
        // Save user preference in localStorage
        const theme = darkmodeToggle.classList.contains('dark-mode') ? 'dark' : 'light';
        localStorage.setItem('theme', theme);
    })
}

// Indicates whether a file is selected or not
document.getElementById('image').addEventListener('change', function() {
    const icon = document.getElementById('attach-icon');

    if (this.files.length > 0) {
        icon.classList.toggle('file-selected');
    } else {
        icon.classList.remove('file-selected');
    }
})

// document.getElementById('message-file').addEventListener('change', function() {
//     const icon = document.getElementById('message-attach-icon');

//     if (this.files.length > 0) {
//         icon.classList.toggle('file-selected');
//     } else {
//         icon.classList.remove('file-selected');
//     }
// })
