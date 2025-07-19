// ===== Staff Management JavaScript =====

// Position options for different staff types
const POSITION_OPTIONS = {
    worker: [
        'Sales Associate',
        'Cashier',
        'Stock Associate',
        'Customer Service Representative',
        'Warehouse Associate',
        'Maintenance Technician',
        'Security Guard',
        'Cleaner',
        'Driver',
        'Administrative Assistant'
    ],
    manager: [
        'Store Manager',
        'Assistant Manager',
        'Department Manager',
        'Operations Manager',
        'Sales Manager',
        'Regional Manager',
        'Area Manager',
        'Branch Manager',
        'Team Leader',
        'Supervisor'
    ]
};

// ===== Modal Control Functions =====
function openAddForm() {
    resetAddForm();
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById('addStaffModal').style.display = 'block';
    document.getElementById('addStaffModal').classList.add('show');
    document.getElementById('modalOverlay').classList.add('show');
    
    // Focus on first input
    setTimeout(() => {
        document.getElementById('staff_type').focus();
    }, 100);
}

function closeAddForm() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('addStaffModal').style.display = 'none';
    document.getElementById('addStaffModal').classList.remove('show');
    document.getElementById('modalOverlay').classList.remove('show');
    resetAddForm();
}

function openEditForm(staffId, staffType) {
    // Show modal first
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById('editStaffModal').style.display = 'block';
    document.getElementById('editStaffModal').classList.add('show');
    document.getElementById('modalOverlay').classList.add('show');
    
    // Set form action URL
    document.getElementById('editStaffForm').action = `/staff/edit/${staffId}`;
    
    // Show appropriate fields based on staff type
    showEditStaffTypeFields(staffType);
    
    // Populate position dropdown for edit form
    populatePositionDropdown('edit_position', staffType);
    
    // Fetch and populate staff data
    fetch(`/staff/edit-data/${staffId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showNotification('Error loading staff data: ' + data.error, 'error');
                closeEditForm();
                return;
            }
            populateEditForm(data, staffType);
            
            // Focus on first input
            setTimeout(() => {
                document.getElementById('edit_first_name').focus();
            }, 100);
        })
        .catch(error => {
            console.error('Error fetching staff data:', error);
            showNotification('Error loading staff data. Please try again.', 'error');
            closeEditForm();
        });
}

function closeEditForm() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('editStaffModal').style.display = 'none';
    document.getElementById('editStaffModal').classList.remove('show');
    document.getElementById('modalOverlay').classList.remove('show');
    
    // Reset form and hide conditional fields
    document.getElementById('editStaffForm').reset();
    document.getElementById('editWorkerFields').style.display = 'none';
    document.getElementById('editManagerFields').style.display = 'none';
    clearRequiredAttributes('editWorkerFields');
    clearRequiredAttributes('editManagerFields');
}

function openDeleteConfirm(staffId, staffName) {
    // Set staff name in confirmation text
    document.getElementById('deleteStaffName').textContent = staffName;
    
    // Set form action URL
    document.getElementById('deleteForm').action = `/staff/delete/${staffId}`;
    
    // Show modal
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById('deleteModal').style.display = 'block';
    document.getElementById('deleteModal').classList.add('show');
    document.getElementById('modalOverlay').classList.add('show');
}

function closeDeleteConfirm() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('deleteModal').style.display = 'none';
    document.getElementById('deleteModal').classList.remove('show');
    document.getElementById('modalOverlay').classList.remove('show');
}

function viewStaffDetails(staffId) {
    const modal = document.getElementById('staffDetailsModal');
    const overlay = document.getElementById('modalOverlay');
    const content = document.getElementById('staffDetailsContent');
    
    // Show modal
    modal.style.display = 'block';
    overlay.style.display = 'block';
    modal.classList.add('show');
    overlay.classList.add('show');
    
    // Show loading message
    content.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
    
    // Fetch staff details
    fetch(`/staff/details/${staffId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                content.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                return;
            }
            
            // Build details HTML
            let detailsHTML = `
                <div class="staff-details">
                    <div class="detail-row">
                        <label>Staff ID:</label>
                        <span>#${data.staff_id}</span>
                    </div>
                    <div class="detail-row">
                        <label>Name:</label>
                        <span>${data.first_name} ${data.last_name}</span>
                    </div>
                    <div class="detail-row">
                        <label>Position:</label>
                        <span>${data.position}</span>
                    </div>
                    <div class="detail-row">
                        <label>Type:</label>
                        <span class="staff-type-badge ${data.staff_type}">${data.staff_type}</span>
                    </div>
                    <div class="detail-row">
                        <label>Salary:</label>
                        <span>$${parseFloat(data.salary).toFixed(2)}</span>
                    </div>
                    <div class="detail-row">
                        <label>Email:</label>
                        <span>${data.email}</span>
                    </div>
                    <div class="detail-row">
                        <label>Phone:</label>
                        <span>${data.phone}</span>
                    </div>
            `;
            
            // Add type-specific details
            if (data.staff_type === 'worker') {
                if (data.branch_name) {
                    detailsHTML += `
                        <div class="detail-row">
                            <label>Branch:</label>
                            <span>${data.branch_name}</span>
                        </div>
                    `;
                }
                if (data.birth_date) {
                    detailsHTML += `
                        <div class="detail-row">
                            <label>Birth Date:</label>
                            <span>${data.birth_date}</span>
                        </div>
                    `;
                }
            } else if (data.staff_type === 'manager') {
                if (data.since) {
                    detailsHTML += `
                        <div class="detail-row">
                            <label>Manager Since:</label>
                            <span>${data.since}</span>
                        </div>
                    `;
                }
            }
            
            detailsHTML += '</div>';
            content.innerHTML = detailsHTML;
        })
        .catch(error => {
            console.error('Error fetching staff details:', error);
            content.innerHTML = '<div class="error">Error loading staff details. Please try again.</div>';
        });
}

function closeDetailsModal() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('staffDetailsModal').style.display = 'none';
    document.getElementById('staffDetailsModal').classList.remove('show');
    document.getElementById('modalOverlay').classList.remove('show');
}

function closeAllModals() {
    closeAddForm();
    closeEditForm();
    closeDeleteConfirm();
    closeDetailsModal();
}

// ===== Position Management Functions =====
function populatePositionDropdown(selectId, staffType) {
    const select = document.getElementById(selectId);
    if (!select || !staffType || !POSITION_OPTIONS[staffType]) {
        return;
    }
    
    // Clear existing options
    select.innerHTML = '<option value="">Select Position</option>';
    
    // Add positions based on staff type
    POSITION_OPTIONS[staffType].forEach(position => {
        const option = document.createElement('option');
        option.value = position;
        option.textContent = position;
        select.appendChild(option);
    });
    
    // Add "Other" option to allow custom positions
    const otherOption = document.createElement('option');
    otherOption.value = 'other';
    otherOption.textContent = 'Other (Custom Position)';
    select.appendChild(otherOption);
}

function handlePositionChange(selectElement, inputId) {
    const customInput = document.getElementById(inputId);
    if (selectElement.value === 'other') {
        // Show custom input for "Other" option
        if (customInput) {
            customInput.style.display = 'block';
            customInput.required = true;
            customInput.focus();
        }
    } else {
        // Hide custom input and use selected value
        if (customInput) {
            customInput.style.display = 'none';
            customInput.required = false;
            customInput.value = '';
        }
    }
}

// ===== Staff Type Management =====
// Add this to your toggleStaffTypeFields function after line 130
function toggleStaffTypeFields() {
    const staffType = document.getElementById('staff_type').value;
    const workerFields = document.getElementById('workerFields');
    const managerFields = document.getElementById('managerFields');
    
    // Hide both sections initially
    workerFields.style.display = 'none';
    managerFields.style.display = 'none';
    
    // Clear required attributes from all conditional fields
    clearRequiredAttributes('workerFields');
    clearRequiredAttributes('managerFields');
    
    // Populate position dropdown based on staff type
    populatePositionDropdown('position', staffType);
    
    // Show and set required attributes based on selected type
    if (staffType === 'worker') {
        workerFields.style.display = 'block';
        setRequiredAttributes('workerFields');
        
        // DEBUG: Check if branch_id is properly set as required
        const branchSelect = document.getElementById('branch_id');
        console.log('Branch select element:', branchSelect);
        console.log('Branch select required:', branchSelect.hasAttribute('required'));
        console.log('Branch select value:', branchSelect.value);
    } else if (staffType === 'manager') {
        managerFields.style.display = 'block';
        setRequiredAttributes('managerFields');
    }
}

function showEditStaffTypeFields(staffType) {
    const editWorkerFields = document.getElementById('editWorkerFields');
    const editManagerFields = document.getElementById('editManagerFields');
    
    // Hide both sections initially
    editWorkerFields.style.display = 'none';
    editManagerFields.style.display = 'none';
    
    // Clear required attributes from all conditional fields
    clearRequiredAttributes('editWorkerFields');
    clearRequiredAttributes('editManagerFields');
    
    // Show and set required attributes based on staff type
    if (staffType === 'worker') {
        editWorkerFields.style.display = 'block';
        setRequiredAttributes('editWorkerFields');
    } else if (staffType === 'manager') {
        editManagerFields.style.display = 'block';
        setRequiredAttributes('editManagerFields');
    }
}

// ===== Helper Functions for Field Management =====
function setRequiredAttributes(containerId) {
    const container = document.getElementById(containerId);
    const inputs = container.querySelectorAll('input[type="text"], input[type="date"], input[type="number"], select');
    
    inputs.forEach(input => {
        if (input.name === 'branch_id' || input.name === 'birth_date' || input.name === 'since') {
            input.setAttribute('required', 'required');
        }
    });
}

function clearRequiredAttributes(containerId) {
    const container = document.getElementById(containerId);
    const inputs = container.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        input.removeAttribute('required');
        input.value = '';
    });
}

// ===== Staff Type Filter =====
function filterStaffType(type) {
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('staff_type', type);
    currentUrl.searchParams.delete('search');
    window.location.href = currentUrl.toString();
}

// ===== Form Functions =====
function resetAddForm() {
    const form = document.getElementById('addStaffForm');
    form.reset();
    
    // Hide conditional fields
    document.getElementById('workerFields').style.display = 'none';
    document.getElementById('managerFields').style.display = 'none';
    
    // Clear all required attributes
    clearRequiredAttributes('workerFields');
    clearRequiredAttributes('managerFields');
    
    // Reset position dropdown
    const positionSelect = document.getElementById('position');
    if (positionSelect) {
        positionSelect.innerHTML = '<option value="">Select Staff Type First</option>';
    }
    
    // Hide custom position input
    const customPositionInput = document.getElementById('custom_position');
    if (customPositionInput) {
        customPositionInput.style.display = 'none';
        customPositionInput.required = false;
        customPositionInput.value = '';
    }
}

function populateEditForm(staffData, staffType) {
    // Populate common fields
    document.getElementById('edit_staff_id').value = staffData.staff_id;
    document.getElementById('edit_first_name').value = staffData.first_name;
    document.getElementById('edit_last_name').value = staffData.last_name;
    document.getElementById('edit_salary').value = staffData.salary;
    document.getElementById('edit_email').value = staffData.email;
    document.getElementById('edit_phone').value = staffData.phone;
    
    // Handle position selection
    const positionSelect = document.getElementById('edit_position');
    const customPositionInput = document.getElementById('edit_custom_position');
    
    if (positionSelect && staffData.position) {
        // Check if the position exists in predefined options
        const positionExists = Array.from(positionSelect.options).some(option => option.value === staffData.position);
        
        if (positionExists) {
            positionSelect.value = staffData.position;
        } else {
            // Position is custom, select "Other" and show custom input
            positionSelect.value = 'other';
            if (customPositionInput) {
                customPositionInput.style.display = 'block';
                customPositionInput.required = true;
                customPositionInput.value = staffData.position;
            }
        }
    }
    
    // Populate type-specific fields
    if (staffType === 'worker') {
        if (staffData.branch_id) {
            document.getElementById('edit_branch_id').value = staffData.branch_id;
        }
        if (staffData.birth_date) {
            document.getElementById('edit_birth_date').value = staffData.birth_date;
        }
    } else if (staffType === 'manager') {
        if (staffData.since) {
            document.getElementById('edit_since').value = staffData.since;
        }
    }
}

// ===== Form Validation =====
function validateStaffForm(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    let isValid = true;
    let errors = [];
    
    // Common required fields
    const commonRequiredFields = ['first_name', 'last_name', 'salary', 'email', 'phone'];
    
    // Add staff type for add form
    if (formId === 'addStaffForm') {
        commonRequiredFields.push('staff_type');
    }
    
    // Validate common fields
    commonRequiredFields.forEach(field => {
        const value = formData.get(field);
        if (!value || value.trim() === '') {
            isValid = false;
            errors.push(`${field.replace('_', ' ').toUpperCase()} is required`);
        }
    });
    
    // Validate position
    const position = formData.get('position');
    const customPosition = formData.get('custom_position');
    
    if (!position || position.trim() === '') {
        if (!customPosition || customPosition.trim() === '') {
            isValid = false;
            errors.push('POSITION is required');
        }
    }
    
    // Validate type-specific fields for add form
    if (formId === 'addStaffForm') {
        const staffType = formData.get('staff_type');
        if (staffType === 'worker') {
            const workerFields = ['branch_id', 'birth_date'];
            workerFields.forEach(field => {
                const value = formData.get(field);
                if (!value || value.trim() === '') {
                    isValid = false;
                    errors.push(`${field.replace('_', ' ').toUpperCase()} is required for workers`);
                }
            });
        } else if (staffType === 'manager') {
            const managerFields = ['since'];
            managerFields.forEach(field => {
                const value = formData.get(field);
                if (!value || value.trim() === '') {
                    isValid = false;
                    errors.push(`${field.replace('_', ' ').toUpperCase()} is required for managers`);
                }
            });
        }
    }
    
    // Validate email format
    const email = formData.get('email');
    if (email && !isValidEmail(email)) {
        isValid = false;
        errors.push('Please enter a valid email address');
    }
    
    // Validate salary is positive
    const salary = formData.get('salary');
    if (salary && (isNaN(salary) || parseFloat(salary) <= 0)) {
        isValid = false;
        errors.push('Salary must be a positive number');
    }
    
    // Validate phone format
    const phone = formData.get('phone');
    if (phone && !isValidPhone(phone)) {
        isValid = false;
        errors.push('Please enter a valid phone number');
    }
    
    // Display errors if any
    if (!isValid) {
        showNotification(errors.join('<br>'), 'error');
    }
    
    return isValid;
}

// ===== Form Submission Handler =====
function handleFormSubmission(form) {
    const positionSelect = form.querySelector('select[name="position"]');
    const customPositionInput = form.querySelector('input[name="custom_position"]');
    
    if (positionSelect && customPositionInput) {
        if (positionSelect.value === 'other' && customPositionInput.value.trim()) {
            // Use custom position value
            positionSelect.value = customPositionInput.value.trim();
        }
    }
}

// ===== Validation Helper Functions =====
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPhone(phone) {
    const phoneRegex = /^[\d\s\-\+\(\)]{10,}$/;
    return phoneRegex.test(phone);
}

// ===== Table Sorting =====
let sortDirection = {};

function sortTable(columnIndex) {
    const table = document.getElementById('staffTable');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    // Determine sort direction
    const currentDirection = sortDirection[columnIndex] || 'asc';
    const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
    sortDirection[columnIndex] = newDirection;
    
    // Update sort icons
    updateSortIcons(columnIndex, newDirection);
    
    // Sort rows
    rows.sort((a, b) => {
        let aVal = getCellValue(a, columnIndex);
        let bVal = getCellValue(b, columnIndex);
        
        // Handle numeric values (salary)
        if (columnIndex === 4) {
            aVal = parseFloat(aVal.replace(/[$,]/g, '')) || 0;
            bVal = parseFloat(bVal.replace(/[$,]/g, '')) || 0;
        }
        
        if (newDirection === 'asc') {
            return aVal > bVal ? 1 : -1;
        } else {
            return aVal < bVal ? 1 : -1;
        }
    });
    
    // Re-append sorted rows
    rows.forEach(row => tbody.appendChild(row));
}

function getCellValue(row, columnIndex) {
    const cell = row.cells[columnIndex];
    return cell.textContent.trim() || cell.innerText.trim() || '';
}

function updateSortIcons(activeColumn, direction) {
    const sortIcons = document.querySelectorAll('.sort-icon');
    
    sortIcons.forEach((icon, index) => {
        icon.className = 'fas fa-sort sort-icon';
        
        if (index === activeColumn) {
            icon.className = direction === 'asc' 
                ? 'fas fa-sort-up sort-icon active' 
                : 'fas fa-sort-down sort-icon active';
        }
    });
}

// ===== Search Functionality =====
function initializeSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performLiveSearch(this.value);
            }, 300);
        });
    }
}

function performLiveSearch(query) {
    const rows = document.querySelectorAll('#staffTable tbody tr');
    const searchTerm = query.toLowerCase();
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// ===== Notification System =====
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notif => notif.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification alert-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
        <button class="close-alert" onclick="this.parentElement.remove()">×</button>
    `;
    
    // Add to page
    document.body.insertBefore(notification, document.body.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success': return 'check-circle';
        case 'error': return 'exclamation-triangle';
        case 'warning': return 'exclamation-circle';
        default: return 'info-circle';
    }
}

// ===== Event Listeners =====
document.addEventListener('DOMContentLoaded', function() {
    // Hide conditional fields initially
    const workerFields = document.getElementById('workerFields');
    const managerFields = document.getElementById('managerFields');
    const editWorkerFields = document.getElementById('editWorkerFields');
    const editManagerFields = document.getElementById('editManagerFields');
    
    if (workerFields) workerFields.style.display = 'none';
    if (managerFields) managerFields.style.display = 'none';
    if (editWorkerFields) editWorkerFields.style.display = 'none';
    if (editManagerFields) editManagerFields.style.display = 'none';
    
    // Modal overlay click to close
    const overlay = document.getElementById('modalOverlay');
    if (overlay) {
        overlay.addEventListener('click', function(e) {
            if (e.target === this) {
                closeAllModals();
            }
        });
    }
    
    // Escape key to close modals
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
    
    // Form submission validation
  // Replace your existing form submission validation with this:
const addForm = document.getElementById('addStaffForm');
if (addForm) {
    addForm.addEventListener('submit', function(e) {
        const staffType = document.getElementById('staff_type').value;
        const branchId = document.getElementById('branch_id').value;
        
        // Explicit check for worker branch_id
        if (staffType === 'worker' && (!branchId || branchId.trim() === '')) {
            e.preventDefault();
            showNotification('Branch ID is required for workers', 'error');
            document.getElementById('branch_id').focus();
            return false;
        }
        
        handleFormSubmission(this);
        if (!validateStaffForm('addStaffForm')) {
            e.preventDefault();
        }
    });
}
    
    const editForm = document.getElementById('editStaffForm');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            handleFormSubmission(this);
            if (!validateStaffForm('editStaffForm')) {
                e.preventDefault();
            }
        });
    }
    
    // Auto-hide flash messages
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            if (message.parentNode) {
                message.style.opacity = '0';
                setTimeout(() => message.remove(), 300);
            }
        }, 5000);
    });
    
    // Initialize search functionality
    initializeSearch();
});

// ===== Keyboard Shortcuts =====
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + N to add new staff
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        openAddForm();
    }
    
    // Ctrl/Cmd + F to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        const searchInput = document.querySelector('input[name="search"]');
        if (searchInput) {
            e.preventDefault();
            searchInput.focus();
        }
    }
});

// ===== Utility Functions =====
function formatSalary(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatPhone(phone) {
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.length === 10) {
        return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
    }
    return phone;
}