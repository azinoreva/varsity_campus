document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('posts').style.display = 'block';
})
document.getElementById('show-courses').addEventListener('click', function() {
    document.getElementById('posts').style.display = 'none'; // Hide posts
    document.getElementById('courses').style.display = 'block'; // Show courses
});

document.getElementById('show-posts').addEventListener('click', function() {
    document.getElementById('courses').style.display = 'none'; // Hide courses
    document.getElementById('posts').style.display = 'block'; // Show posts
});

// Initialize the courses section to be hidden
document.getElementById('courses').style.display = 'none'; // Hide courses by default

// confirm deletion of post
function confirmDelete() {
    return confirm('Are you sure you want to delete this lecture? This action cannot be undone.');
}
