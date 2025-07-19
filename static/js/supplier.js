// ===== Supplier Management JavaScript =====

// ===== Modal Control Functions =====
function openAddForm() {
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById('addSupplierModal').style.display = 'block';
    // Focus on first input
    setTimeout(() => {
        document.getElementById('supplier_name').focus();
    }, 100);
}

function closeAddForm() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('addSupplierModal').style.display = 'none';
    resetAddForm();
}

function openEditForm(supplierId, supplierName, phone) {
    // Populate form fields
    document.getElementById('edit_supplier_id').value = supplierId;
    document.getElementById('edit_supplier_name').value = supplierName;
    document.getElementById('edit_phone').value = phone || '';

    // Set form action URL
    document.getElementById('editSupplierForm').action = `/supplier/edit/${supplierId}`;

    // Show modal
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById('editSupplierModal').style.display = 'block';

    // Focus on first input
    setTimeout(() => {
        document.getElementById('edit_supplier_name').focus();
    }, 100);
}

function closeEditForm() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('editSupplierModal').style.display = 'none';
}

function openDeleteConfirm(supplierId, supplierName) {
    // Set supplier name in confirmation text
    document.getElementById('deleteSupplierName').textContent = supplierName;

    // Set form action URL
    document.getElementById('deleteForm').action = `/supplier/delete/${supplierId}`;

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
    document.getElementById('addSupplierModal').style.display = 'none';
    document.getElementById('editSupplierModal').style.display = 'none';
    document.getElementById('deleteModal').style.display = 'none';
}

// ===== Form Functions =====
function resetAddForm() {
    document.getElementById('addSupplierForm').reset();
}

// ===== Form Validation =====
function validatePhone(phone) {
    if (!phone) return true; // Phone is optional

    const cleanedPhone = phone.replace(/[\s|]/g, '');

    const phoneRegex = /^[1-9]\d{0,15}$/;

    return !phoneRegex.test(cleanedPhone);
}


function validateForm(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    let isValid = true;
    let errors = [];

    // Validate required fields
    const requiredFields = ['supplier_name'];
    requiredFields.forEach(field => {
        const value = formData.get(field);
        if (!value || value.trim() === '') {
            isValid = false;
            errors.push(`${field.replace('_', ' ').toUpperCase()} is required`);
        }
    });

    // Validate phone format
    const phone = formData.get('phone');
    if (phone && !validatePhone(phone)) {
        isValid = false;
        errors.push('Please enter a valid phone number');
    }

    // Show errors if any
    if (!isValid) {
        alert('Please correct the following errors:\n\n' + errors.join('\n'));
    }

    return isValid;
}


function sortTable(columnIndex) {
    const table = document.getElementById('supplierTable');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const header = table.querySelectorAll('th')[columnIndex];
    const sortIcon = header.querySelector('.sort-icon');
    if (!sortIcon) return;

    const isAscending = sortIcon.classList.contains('fa-sort-up');
    const newOrder = isAscending ? 'desc' : 'asc';

    // Reset all sort icons
    table.querySelectorAll('.sort-icon').forEach(icon => {
        icon.className = 'fas fa-sort sort-icon';
    });

    // Update current column sort icon
    sortIcon.className = `fas fa-sort-${newOrder === 'asc' ? 'up' : 'down'} sort-icon`;

    // Sort rows
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();

        const isNumeric = !isNaN(aValue) && !isNaN(bValue);

        if (columnIndex === 0 || isNumeric) {
            const aNum = parseFloat(aValue.replace('#', '')) || 0;
            const bNum = parseFloat(bValue.replace('#', '')) || 0;
            return newOrder === 'asc' ? aNum - bNum : bNum - aNum;
        }

        // Case-insensitive text sort
        const comparison = aValue.localeCompare(bValue, undefined, { sensitivity: 'base' });
        return newOrder === 'asc' ? comparison : -comparison;
    });

    // Reorder DOM
    rows.forEach(row => tbody.appendChild(row));
}


// ===== Event Listeners =====
document.addEventListener('DOMContentLoaded', function() {
    // Add form validation on submit
    const addForm = document.getElementById('addSupplierForm');
    if (addForm) {
        addForm.addEventListener('submit', function(e) {
            if (!validateForm('addSupplierForm')) {
                e.preventDefault();
            }
        });
    }

    const editForm = document.getElementById('editSupplierForm');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            if (!validateForm('editSupplierForm')) {
                e.preventDefault();
            }
        });
    }

    // Close modal when clicking outside
    document.getElementById('modalOverlay').addEventListener('click', function(e) {
        if (e.target === this) {
            closeAllModals();
        }
    });

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

    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            // Remove all non-digit characters except +
            let value = e.target.value.replace(/[^\d+]/g, '');

            // Format phone number (basic formatting)
            if (value.length > 0 && !value.startsWith('+')) {
                if (value.length <= 10) {
                    // Format as (XXX) XXX-XXXX
                    if (value.length >= 6) {
                        value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6)}`;
                    } else if (value.length >= 3) {
                        value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
                    }
                }
            }

            e.target.value = value;
        });
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
