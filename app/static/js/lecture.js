// Initialize studentEmails array from hidden input field
let studentEmails = document.getElementById('studentEmails').value.split(',').filter(email => email);

// Function to update the hidden input field with current emails
function updateHiddenInput() {
    document.getElementById('studentEmails').value = studentEmails.join(',');
}

// Function to add a new student email to the list
function addStudentEmail(email) {
    if (email && !studentEmails.includes(email)) {
        // Add email to studentEmails array
        studentEmails.push(email);

        // Update the hidden input field
        updateHiddenInput();

        // Display the email in the list
        createStudentListItem(email);
    }
}

// Function to create and display a list item for a student email
function createStudentListItem(email) {
    const studentList = document.getElementById('studentList');
    const listItem = document.createElement('li');
    listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
    listItem.textContent = email;

    // Create remove button
    const removeBtn = createRemoveButton(email, listItem);
    listItem.appendChild(removeBtn);
    studentList.appendChild(listItem);
}

// Function to create a remove button for a student list item
function createRemoveButton(email, listItem) {
    const removeBtn = document.createElement('button');
    removeBtn.className = 'btn btn-danger btn-sm ms-2';
    removeBtn.textContent = 'x';

    // Set up event listener to remove student when clicked
    removeBtn.addEventListener('click', function () {
        removeStudentEmail(email, listItem);
    });

    return removeBtn;
}

// Function to remove a student email from the list and update the hidden input
function removeStudentEmail(email, listItem) {
    const studentList = document.getElementById('studentList');
    studentList.removeChild(listItem); // Remove list item from DOM

    // Remove email from the array
    studentEmails = studentEmails.filter(e => e !== email);
    updateHiddenInput(); // Update the hidden input field
}

// Function to initialize existing student emails in the list on page load
function initializeExistingEmails() {
    const existingEmails = studentEmails.filter(email => email); // Filter out empty emails
    existingEmails.forEach(email => createStudentListItem(email));
}

// Event listener for adding a new student email on button click
document.getElementById('addStudentBtn').addEventListener('click', function () {
    const studentEmailInput = document.getElementById('studentEmailInput');
    const email = studentEmailInput.value.trim();
    addStudentEmail(email);

    // Clear the input field for the next student
    studentEmailInput.value = '';
});

// Initialize the list with any pre-existing emails on page load
initializeExistingEmails();




document.getElementById('deleteLectureBtn').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent default link behavior

    console.log("it got to this point");
    
    const lectureId = this.getAttribute('data-lecture-id'); // Retrieve lecture ID from data attribute
    console.log(lectureId);
    

    // Display confirmation prompt
    const confirmation = confirm('Are you sure you want to delete this lecture? This action cannot be undone.');

    if (confirmation) {
        // If confirmed, proceed with deletion
        fetch(`/lectures/delete/${lectureId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => {
            if (response.ok) {
                alert('Lecture deleted successfully');
                window.location.href = '/lectures/view_lectures/'; // Redirect to view lectures page
            } else {
                alert('Failed to delete lecture');
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('An error occurred while trying to delete the lecture.');
        });
    }
});