let studentEmails = [];

document.getElementById('addStudentBtn').addEventListener('click', function () {
    const studentEmailInput = document.getElementById('studentEmailInput');
    const email = studentEmailInput.value.trim();

    if (email && !studentEmails.includes(email)) {
        
        studentEmails.push(email)

        // Create list item for visual feedback
        const studentList = document.getElementById('studentList');
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
        listItem.textContent = email;

        // Add remove button to each student entry
        const removeBtn = document.createElement('button');
        removeBtn.className = 'btn btn-danger btn-sm ms-2';
        removeBtn.textContent = 'x';
        listItem.appendChild(removeBtn);
        studentList.appendChild(listItem);

        // Create or update the hidden input field to store the emails
        let hiddenInput = document.getElementById('studentEmail');

        // Update the hidden input value
        document.getElementById('studentEmails').value = studentEmails;

        // Clear the input field for the next student
        studentEmailInput.value = '';

        // Remove button functionality
        removeBtn.addEventListener('click', function () {
            studentList.removeChild(listItem);
            // Remove the email from the hidden input value
            const updatedEmails = currentEmails.filter(e => e !== email);
            document.getElementById('studentEmail').value = JSON.stringify({ "emails": studentEmails });
        });
    }
});
