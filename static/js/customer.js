// ===== Customer Management JavaScript =====

// ===== Modal Control Functions =====
function openAddForm() {
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById('addCustomerModal').style.display = 'block';
    // Focus on first input
    setTimeout(() => {
        document.getElementById('first_name').focus();
    }, 100);
}

function closeAddForm() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('addCustomerModal').style.display = 'none';
    resetAddForm();
}

function openEditForm(customerId, firstName, lastName, email, phone, birthDate) {
    // Populate form fields
    document.getElementById('edit_customer_id').value = customerId;
    document.getElementById('edit_first_name').value = firstName;
    document.getElementById('edit_last_name').value = lastName;
    document.getElementById('edit_email').value = email;
    document.getElementById('edit_phone').value = phone || '';
    document.getElementById('edit_birth_date').value = birthDate || '';
    
    // Set form action URL
    document.getElementById('editCustomerForm').action = `/customer/edit/${customerId}`;
    
    // Show modal
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById('editCustomerModal').style.display = 'block';
    
    // Focus on first input
    setTimeout(() => {
        document.getElementById('edit_first_name').focus();
    }, 100);
}

function closeEditForm() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('editCustomerModal').style.display = 'none';
}

function openDeleteConfirm(customerId, customerName) {
    // Set customer name in confirmation text
    document.getElementById('deleteCustomerName').textContent = customerName;
    
    // Set form action URL
    document.getElementById('deleteForm').action = `/customer/delete/${customerId}`;
    
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
    document.getElementById('addCustomerModal').style.display = 'none';
    document.getElementById('editCustomerModal').style.display = 'none';
    document.getElementById('deleteModal').style.display = 'none';
}

// ===== Form Functions =====
function resetAddForm() {
    document.getElementById('addCustomerForm').reset();
}

// ===== Form Validation =====
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}
function validatePhone(phone) {
    if (!phone) return true; // Phone is optional

    const cleanedPhone = phone.replace(/[\s|]/g, '');

    const phoneRegex = /^[1-9]\d{0,15}$/;

    return !phoneRegex.test(cleanedPhone);
}


function sortTable(columnIndex) {
    const table = document.getElementById('customerTable');
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


function validateForm(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    let isValid = true;
    let errors = [];

    // Validate required fields
    const requiredFields = ['first_name', 'last_name', 'email'];
    if (formId === 'addCustomerForm') {
        requiredFields.push('password');
    }

    requiredFields.forEach(field => {
        const value = formData.get(field);
        if (!value || value.trim() === '') {
            isValid = false;
            errors.push(`${field.replace('_', ' ').toUpperCase()} is required`);
        }
    });

    // Validate email format
    const email = formData.get('email');
    if (email && !validateEmail(email)) {
        isValid = false;
        errors.push('Please enter a valid email address');
    }

    // Validate phone format
    const phone = formData.get('phone');
    if (phone && !validatePhone(phone)) {
        isValid = false;
        errors.push('Please enter a valid phone number');
    }

    // Validate password (only for add form)
    if (formId === 'addCustomerForm') {
        const password = formData.get('password');
        if (password && password.length < 6) {
            isValid = false;
            errors.push('Password must be at least 6 characters long');
        }
    }

    // Show errors if any
    if (!isValid) {
        alert('Please correct the following errors:\n\n' + errors.join('\n'));
    }

    return isValid;
}

// ===== Event Listeners =====
document.addEventListener('DOMContentLoaded', function() {
    // Add form validation on submit
    const addForm = document.getElementById('addCustomerForm');
    if (addForm) {
        addForm.addEventListener('submit', function(e) {
            if (!validateForm('addCustomerForm')) {
                e.preventDefault();
            }
        });
    }

    const editForm = document.getElementById('editCustomerForm');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            if (!validateForm('editCustomerForm')) {
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

// Clean phone number formatting (digits only, optional + at start)
const phoneInputs = document.querySelectorAll('input[type="tel"]');

phoneInputs.forEach(input => {
    input.addEventListener('input', function (e) {
        let value = e.target.value;

        // Preserve leading '+' if present
        const hasPlus = value.startsWith('+');
        value = value.replace(/[^\d]/g, '');

        // Add '+' back if it was at the beginning
        if (hasPlus) {
            value = '+' + value;
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

// Global variables for address management
let currentCustomerId = null;
let currentAddressId = null;
let customerAddresses = [];

// Dropdown Menu Functions
function toggleDropdown(customerId) {
    // Close all other dropdowns
    document.querySelectorAll('.dropdown-content').forEach(dropdown => {
        if (dropdown.id !== `dropdown-${customerId}`) {
            dropdown.style.display = 'none';
        }
    });
    
    // Toggle current dropdown
    const dropdown = document.getElementById(`dropdown-${customerId}`);
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(event) {
    if (!event.target.matches('.dropdown-toggle') && !event.target.matches('.fas.fa-ellipsis-v')) {
        document.querySelectorAll('.dropdown-content').forEach(dropdown => {
            dropdown.style.display = 'none';
        });
    }
});
// Address Modal Functions
function openAddressModal(customerId, customerName) {
    currentCustomerId = customerId;
    document.getElementById('addressCustomerName').textContent = customerName;
    document.getElementById('addressModal').style.display = 'block';
    document.getElementById('modalOverlay').style.display = 'block';
    
    // Load addresses for this customer
    loadCustomerAddresses(customerId);
    
    // Close dropdown
    closeAllDropdowns();
}

function closeAddressModal() {
    document.getElementById('addressModal').style.display = 'none';
    document.getElementById('modalOverlay').style.display = 'none';
    closeAddressForm();
    currentCustomerId = null;
}

// Load addresses for a customer
// Fixed address rendering functions
function renderAddressList() {
    const addressTableBody = document.getElementById('addressTableBody');
    const emptyState = document.getElementById('emptyAddressState');
    
    if (customerAddresses.length === 0) {
        renderEmptyAddressList();
        return;
    }
    
    // Hide empty state and show table
    emptyState.style.display = 'none';
    document.getElementById('addressTable').style.display = 'table';
    
    // Generate table rows instead of cards
    const addressRows = customerAddresses.map(address => `
        <tr>
            <td>
                <span class="address-type-badge ${address.address_type.toLowerCase()}">${address.address_type}</span>
            </td>
            <td>${address.city}</td>
            <td>${address.street_address}</td>
            <td>
                <i class="fas fa-${address.is_default ? 'star' : 'star-o'}"></i>
                ${address.is_default ? 'Yes' : 'No'}
            </td>
            <td class="actions">
                <button class="btn btn-sm btn-primary" onclick="openEditAddressForm(${address.address_id})" title="Edit Address">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="openDeleteAddressConfirm(${address.address_id})" title="Delete Address">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
    
    addressTableBody.innerHTML = addressRows;
}

function renderEmptyAddressList() {
    const addressTableBody = document.getElementById('addressTableBody');
    const emptyState = document.getElementById('emptyAddressState');
    
    // Hide table and show empty state
    document.getElementById('addressTable').style.display = 'none';
    emptyState.style.display = 'block';
    
    // Clear table body
    addressTableBody.innerHTML = '';
}

// Also update loadCustomerAddresses to handle the response properly
async function loadCustomerAddresses(customerId) {
    try {
        console.log(`Loading addresses for customer ${customerId}`); // Debug log
        const response = await fetch(`/address/customer/${customerId}`);
        
        if (response.ok) {
            customerAddresses = await response.json();
            console.log('Loaded addresses:', customerAddresses); // Debug log
            renderAddressList();
        } else {
            console.error('Failed to load addresses, status:', response.status);
            renderEmptyAddressList();
        }
    } catch (error) {
        console.error('Error loading addresses:', error);
        renderEmptyAddressList();
    }
}

// Address Form Functions
function openAddAddressForm() {
    document.getElementById('addressFormContainer').style.display = 'block';
    document.getElementById('addressFormTitle').textContent = 'Add New Address';
    document.getElementById('addressForm').reset();
    currentAddressId = null;
    
    // Set the customer ID in the hidden field
    document.getElementById('address_customer_id').value = currentCustomerId;
}

function openEditAddressForm(addressId) {
    const address = customerAddresses.find(addr => addr.address_id === addressId);
    if (!address) return;
    
    currentAddressId = addressId;
    document.getElementById('addressFormContainer').style.display = 'block';
    document.getElementById('addressFormTitle').textContent = 'Edit Address';
    
    // Populate form with address data
    document.getElementById('streetAddress').value = address.street_address || '';
    document.getElementById('city').value = address.city || '';
    document.getElementById('addressType').value = address.address_type || '';
    document.getElementById('address_customer_id').value = currentCustomerId;
}

function closeAddressForm() {
    document.getElementById('addressFormContainer').style.display = 'none';
    document.getElementById('addressForm').reset();
    currentAddressId = null;
}

function resetAddressForm() {
    document.getElementById('addressForm').reset();
    // Reset the customer ID
    document.getElementById('address_customer_id').value = currentCustomerId;
}

// Save address (create or update) - FIXED VERSION
async function saveAddress() {
    const formData = new FormData();
    formData.append('customer_id', currentCustomerId);
    formData.append('street_address', document.getElementById('streetAddress').value.trim());
    formData.append('city', document.getElementById('city').value.trim());
    formData.append('address_type', document.getElementById('addressType').value);
    
    // Validate required fields
    if (!formData.get('street_address') || !formData.get('city') || !formData.get('address_type')) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }
    
    try {
        let response;
        if (currentAddressId) {
            // Update existing address
            response = await fetch(`/address/edit/${currentAddressId}`, {
                method: 'POST',
                body: formData
            });
        } else {
            // Create new address - FIXED: Use correct route
            response = await fetch('/address/add', {
                method: 'POST',
                body: formData
            });
        }
        
        if (response.ok) {
            const result = await response.json();
            showNotification(
                currentAddressId ? 'Address updated successfully' : 'Address added successfully',
                'success'
            );
            closeAddressForm();
            await loadCustomerAddresses(currentCustomerId);
 // Reload addresses
        } else {
            const error = await response.json();
            showNotification(error.message || 'Failed to save address', 'error');
        }
    } catch (error) {
        console.error('Error saving address:', error);
        showNotification('An error occurred while saving the address', 'error');
    }
}

// Delete Address Functions
function openDeleteAddressConfirm(addressId) {
    const address = customerAddresses.find(addr => addr.address_id === addressId);
    if (!address) return;
    
    currentAddressId = addressId;
    document.getElementById('deleteAddressInfo').innerHTML = `
        <strong>${address.street_address}, ${address.city}</strong>
    `;
    document.getElementById('deleteAddressModal').style.display = 'block';
}

function closeDeleteAddressConfirm() {
    document.getElementById('deleteAddressModal').style.display = 'none';
    currentAddressId = null;
}

async function confirmDeleteAddress() {
    if (!currentAddressId) return;
    
    try {
        const response = await fetch(`/address/delete/${currentAddressId}`, {
            method: 'POST'
        });
        
        if (response.ok) {
            showNotification('Address deleted successfully', 'success');
            closeDeleteAddressConfirm();
            loadCustomerAddresses(currentCustomerId); // Reload addresses
        } else {
            const error = await response.json();
            showNotification(error.message || 'Failed to delete address', 'error');
        }
    } catch (error) {
        console.error('Error deleting address:', error);
        showNotification('An error occurred while deleting the address', 'error');
    }
}

// Notification System
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Fix the address form submission
    const addressForm = document.getElementById('addressForm');
    if (addressForm) {
        addressForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent default form submission
            console.log('Address form submitted!'); // Debug message
            saveAddress(); // Call your save function
        });
    }
});

// Utility function to format address for display
function formatAddressDisplay(address) {
    const parts = [
        address.street_address,
        address.city,
        address.address_type
    ].filter(part => part && part.trim());
    
    return parts.join(', ');
}


