// handle assignment questions input
document.addEventListener('DOMContentLoaded', () => {
    // Function to update the hidden input field with current items
    function updateHiddenInput(hiddenInputId, items) {
        document.getElementById(hiddenInputId).value = items.join(',');
    }

    // Function to add a new item to the list
    function addItem(item, items, hiddenInputId, listContainerId, uniqueCheck = false) {
        // Check for unique item if required
        if (item && (!uniqueCheck || !items.includes(item))) {
            items.push(item);
            updateHiddenInput(hiddenInputId, items);
            createListItem(item, listContainerId, items, hiddenInputId);
        }
    }

    // Function to create and display a list item
    function createListItem(item, listContainerId, items, hiddenInputId) {
        const listContainer = document.getElementById(listContainerId);
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
        listItem.textContent = item;

        // Create remove button
        const removeBtn = createRemoveButton(item, listItem, items, hiddenInputId);
        listItem.appendChild(removeBtn);
        listContainer.appendChild(listItem);
    }

    // Function to create a remove button for a list item
    function createRemoveButton(item, listItem, items, hiddenInputId) {
        const removeBtn = document.createElement('button');
        removeBtn.className = 'btn btn-danger btn-sm ms-2';
        removeBtn.textContent = 'x';

        // Set up event listener to remove item when clicked
        removeBtn.addEventListener('click', function () {
            removeItem(item, listItem, items, hiddenInputId);
        });

        return removeBtn;
    }

    // Function to remove an item from the list and update the hidden input
    function removeItem(item, listItem, items, hiddenInputId) {
        const listContainer = listItem.parentNode;
        listContainer.removeChild(listItem);

        const index = items.indexOf(item);
        if (index !== -1) {
            items.splice(index, 1);
        }
        updateHiddenInput(hiddenInputId, items);
    }

    // Function to initialize existing items in the list on page load
    function initializeExistingItems(hiddenInputId, listContainerId, uniqueCheck) {
        const hiddenInput = document.getElementById(hiddenInputId);
        const items = hiddenInput.value ? hiddenInput.value.split(',').filter(item => item) : [];
        items.forEach(item => createListItem(item, listContainerId, items, hiddenInputId));
        return items;
    }

    // Function to set up event listener for adding new items
    function setupAddItemButton(buttonId, inputFieldId, hiddenInputId, listContainerId, uniqueCheck = false) {
        const button = document.getElementById(buttonId);
        const inputField = document.getElementById(inputFieldId);
        const items = initializeExistingItems(hiddenInputId, listContainerId, uniqueCheck);

        button.addEventListener('click', function () {
            console.log("adding questions ...");
            
            const value = inputField.value.trim();
            addItem(value, items, hiddenInputId, listContainerId, uniqueCheck);
            inputField.value = '';
        });
    }

    // Setup lists with unique check where needed (e.g., email list)
    setupAddItemButton('addStudentBtn', 'studentEmailInput', 'studentEmails', 'studentList', true);
    setupAddItemButton('addVideoBtn', 'videoUrlInput', 'video_url', 'videoList');
    setupAddItemButton('addDocxBtn', 'documentUrlInput', 'document_url', 'documentList');
});

// confirm delete lecture
function confirmDelete() {
    return confirm('Are you sure you want to delete this lecture? This action cannot be undone.');
}
























// // Initialize studentEmails array from hidden input field
// let studentEmails = document.getElementById('studentEmails').value.split(',').filter(email => email);

// // Function to update the hidden input field with current emails
// function updateHiddenInput() {
//     document.getElementById('studentEmails').value = studentEmails.join(',');
// }

// // Function to add a new student email to the list
// function addStudentEmail(email) {
//     if (email && !studentEmails.includes(email)) {
//         // Add email to studentEmails array
//         studentEmails.push(email);

//         // Update the hidden input field
//         updateHiddenInput();

//         // Display the email in the list
//         createStudentListItem(email);
//     }
// }

// // Function to create and display a list item for a student email
// function createStudentListItem(email) {
//     const studentList = document.getElementById('studentList');
//     const listItem = document.createElement('li');
//     listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
//     listItem.textContent = email;

//     // Create remove button
//     const removeBtn = createRemoveButton(email, listItem);
//     listItem.appendChild(removeBtn);
//     studentList.appendChild(listItem);
// }

// // Function to create a remove button for a student list item
// function createRemoveButton(email, listItem) {
//     const removeBtn = document.createElement('button');
//     removeBtn.className = 'btn btn-danger btn-sm ms-2';
//     removeBtn.textContent = 'x';

//     // Set up event listener to remove student when clicked
//     removeBtn.addEventListener('click', function () {
//         removeStudentEmail(email, listItem);
//     });

//     return removeBtn;
// }

// // Function to remove a student email from the list and update the hidden input
// function removeStudentEmail(email, listItem) {
//     const studentList = document.getElementById('studentList');
//     studentList.removeChild(listItem); // Remove list item from DOM

//     // Remove email from the array
//     studentEmails = studentEmails.filter(e => e !== email);
//     updateHiddenInput(); // Update the hidden input field
// }

// // Function to initialize existing student emails in the list on page load
// function initializeExistingEmails() {
//     const existingEmails = studentEmails.filter(email => email); // Filter out empty emails
//     existingEmails.forEach(email => createStudentListItem(email));
// }

// // Event listener for adding a new student email on button click
// document.getElementById('addStudentBtn').addEventListener('click', function () {
//     const studentEmailInput = document.getElementById('studentEmailInput');
//     const email = studentEmailInput.value.trim();
//     addStudentEmail(email);

//     // Clear the input field for the next student
//     studentEmailInput.value = '';
// });

// // Initialize the list with any pre-existing emails on page load
// initializeExistingEmails();


