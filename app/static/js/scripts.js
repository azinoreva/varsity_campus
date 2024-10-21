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