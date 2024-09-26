// Function to confirm delete action
function confirmDelete(event, itemType) {
    if (!confirm(`Are you sure you want to delete this ${itemType}?`)) {
        event.preventDefault();
    }
}

// Function to toggle post content visibility
function toggleContent(postId) {
    const content = document.getElementById(`post-content-${postId}`);
    const button = document.getElementById(`toggle-button-${postId}`);
    if (content.style.display === 'none') {
        content.style.display = 'block';
        button.textContent = 'Hide Content';
    } else {
        content.style.display = 'none';
        button.textContent = 'Show Content';
    }
}

// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add event listeners when the DOM is loaded
document.addEventListener('DOMContentLoaded', (event) => {
    // Add delete confirmation to delete buttons
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', (e) => confirmDelete(e, 'item'));
    });

    // Initialize tooltips (Bootstrap feature)
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
});

function toggleContent(postId) {
    const content = document.getElementById(`post-content-${postId}`);
    const button = document.getElementById(`toggle-button-${postId}`);
    if (content.style.maxHeight) {
        content.style.maxHeight = null;
        button.textContent = 'Show Full Content';
    } else {
        content.style.maxHeight = content.scrollHeight + "px";
        button.textContent = 'Hide Content';
    }
}