// ===== Category Management JavaScript =====

// ===== Modal Control Functions =====
function openAddForm() {
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById('addCategoryModal').style.display = 'block';
    // Focus on first input
    setTimeout(() => {
        document.getElementById('category_name').focus();
    }, 100);
}

function closeAddForm() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('addCategoryModal').style.display = 'none';
    resetAddForm();
}

function openEditForm(categoryId, categoryName, description) {
    // Populate form fields
    document.getElementById('edit_category_id').value = categoryId;
    document.getElementById('edit_category_name').value = categoryName;
    document.getElementById('edit_category_description').value = description || '';

    // Set form action URL
    document.getElementById('editCategoryForm').action = `/category/edit/${categoryId}`;

    // Show modal
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById('editCategoryModal').style.display = 'block';

    // Focus on first input
    setTimeout(() => {
        document.getElementById('edit_category_name').focus();
    }, 100);
}

function closeEditForm() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('editCategoryModal').style.display = 'none';
}

function openDeleteConfirm(categoryId, categoryName) {
    // Set category name in confirmation text
    document.getElementById('deleteCategoryName').textContent = categoryName;

    // Set form action URL
    document.getElementById('deleteForm').action = `/category/delete/${categoryId}`;

    // Show modal
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById('deleteModal').style.display = 'block';
}

function closeDeleteConfirm() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('deleteModal').style.display = 'none';
}

function closeAllModals() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('addCategoryModal').style.display = 'none';
    document.getElementById('editCategoryModal').style.display = 'none';
    document.getElementById('deleteModal').style.display = 'none';
}

// ===== Form Functions =====
function resetAddForm() {
    document.getElementById('addCategoryForm').reset();
}

// ===== Form Validation =====
function validateForm(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    let isValid = true;
    let errors = [];

    // Validate required fields
    const requiredFields = ['category_name'];
    requiredFields.forEach(field => {
        const value = formData.get(field);
        if (!value || value.trim() === '') {
            isValid = false;
            errors.push(`${field.replace('_', ' ').toUpperCase()} is required`);
        }
    });

    // Show errors if any
    if (!isValid) {
        alert('Please correct the following errors:\n\n' + errors.join('\n'));
    }

    return isValid;
}

// ===== Table Sorting Function =====
function sortTable(columnIndex) {
    const table = document.getElementById('categoryTable');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const header = table.querySelectorAll('th')[columnIndex];
    const sortIcon = header.querySelector('.sort-icon');

    // Determine sort order
    const isAscending = sortIcon.classList.contains('fa-sort-up');
    const newOrder = isAscending ? 'desc' : 'asc';

    // Reset all sort icons
    table.querySelectorAll('.sort-icon').forEach(icon => {
        icon.className = 'fas fa-sort sort-icon';
    });

    // Set new sort icon
    sortIcon.className = `fas fa-sort-${newOrder === 'asc' ? 'up' : 'down'} sort-icon`;

    // Sort rows
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();

        // Handle numeric sorting for ID column
        if (columnIndex === 0) {
            const aNum = parseInt(aValue.replace('#', ''));
            const bNum = parseInt(bValue.replace('#', ''));
            return newOrder === 'asc' ? aNum - bNum : bNum - aNum;
        }

        // Handle text sorting
        const comparison = aValue.localeCompare(bValue);
        return newOrder === 'asc' ? comparison : -comparison;
    });

    // Reorder rows in DOM
    rows.forEach(row => tbody.appendChild(row));
}

// ===== Event Listeners =====
document.addEventListener('DOMContentLoaded', function() {
    // Add form validation on submit
    const addForm = document.getElementById('addCategoryForm');
    if (addForm) {
        addForm.addEventListener('submit', function(e) {
            if (!validateForm('addCategoryForm')) {
                e.preventDefault();
            }
        });
    }

    const editForm = document.getElementById('editCategoryForm');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            if (!validateForm('editCategoryForm')) {
                e.preventDefault();
            }
        });
    }

    // Close modal when clicking outside
    const modalOverlay = document.getElementById('modalOverlay');
    if (modalOverlay) {
        modalOverlay.addEventListener('click', function(e) {
            if (e.target === this) {
                closeAllModals();
            }
        });
    }

    // Handle escape key to close modals
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });

    // Auto-hide flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });

    // Enhanced table interactions
    const tableRows = document.querySelectorAll('.data-table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.01)';
        });

        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
});

// ===== Utility Functions =====
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        ${message}
        <button class="close-alert" onclick="this.parentElement.remove()">×</button>
    `;

    // Insert at the top of the container
    const container = document.querySelector('.container');
    container.insertBefore(notification, container.firstChild);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
}