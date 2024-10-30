// handle assignment questions and answer
document.addEventListener('DOMContentLoaded', () => {
    // Function to update the hidden input field with current items
    function updateHiddenInput(hiddenInputId, items) {
        document.getElementById(hiddenInputId).value = items.join(',');
    }

    // Function to add a new item to the list
    function addItem(item, items, hiddenInputId, listContainerId) {
        if (item && !items.includes(item)) { // Ensure item is not empty and not already in the list
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
        const listContainer = listItem.parentNode; // Get the parent (list container)
        listContainer.removeChild(listItem); // Remove list item from DOM

        // Remove item from the array
        const index = items.indexOf(item);
        if (index !== -1) {
            items.splice(index, 1);
        }
        updateHiddenInput(hiddenInputId, items); // Update the hidden input field
    }

    // Function to initialize existing items in the list on page load
    function initializeExistingItems(items, listContainerId) {
        items.forEach(item => createListItem(item, listContainerId, items));
    }

    // Function to set up event listener for adding new items
    function setupAddItemButton(buttonId, inputFieldId, hiddenInputId, listContainerId) {
        const button = document.getElementById(buttonId);
        const inputField = document.getElementById(inputFieldId);
        const hiddenInput = document.getElementById(hiddenInputId);
        const listContainer = document.getElementById(listContainerId);

        // Only proceed if all required elements exist
        if (!button || !inputField || !hiddenInput || !listContainer) {
            console.warn(`One or more elements are missing: ${buttonId}, ${inputFieldId}, ${hiddenInputId}, ${listContainerId}`);
            return;
        }

        // Initialize items only on button click
        button.addEventListener('click', function () {
            console.log("I got here"); // This will now only log when the button is clicked
            
            // Initialize the item list when the button is clicked for the first time
            let items = hiddenInput.value ? hiddenInput.value.split(',').filter(item => item) : [];

            const value = inputField.value.trim();

            // Add item and clear input field
            addItem(value, items, hiddenInputId, listContainerId);
            inputField.value = ''; // Clear the input field for the next item
        });
    }

    // Usage Example: Set up the student emails list
    setupAddItemButton('addQuestionBtn', 'questionsInput', 'questions', 'questionList');
    setupAddItemButton('answerBtn', 'answerInput', 'answer', 'answerList');
});