// Global variables
let currentBranchId = null;
let currentWarehouseId = null;
let warehouseToDelete = null;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize form event listeners
    initializeFormEventListeners();
});

// Initialize form event listeners
function initializeFormEventListeners() {
    // Edit branch form
    const editForm = document.getElementById('editBranchForm');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitEditForm();
        });
    }

    // Warehouse form
    const warehouseForm = document.getElementById('warehouseForm');
    if (warehouseForm) {
        warehouseForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitWarehouseForm();
        });
    }
}

// Table sorting functionality
function sortTable(columnIndex) {
    const table = document.getElementById('branchTable');
    const tbody = table.getElementsByTagName('tbody')[0];
    const rows = Array.from(tbody.getElementsByTagName('tr'));
    
    // Get sort direction
    const header = table.getElementsByTagName('th')[columnIndex];
    const icon = header.querySelector('.sort-icon');
    const isAscending = !icon.classList.contains('fa-sort-up');
    
    // Reset all sort icons
    document.querySelectorAll('.sort-icon').forEach(i => {
        i.className = 'fas fa-sort sort-icon';
    });
    
    // Set current sort icon
    icon.className = `fas fa-sort-${isAscending ? 'up' : 'down'} sort-icon`;
    
    // Sort rows
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        // Handle numeric values
        if (!isNaN(aValue) && !isNaN(bValue)) {
            return isAscending ? 
                parseInt(aValue.replace('#', '')) - parseInt(bValue.replace('#', '')) :
                parseInt(bValue.replace('#', '')) - parseInt(aValue.replace('#', ''));
        }
        
        // Handle text values
        return isAscending ? 
            aValue.localeCompare(bValue) : 
            bValue.localeCompare(aValue);
    });
    
    // Rebuild table body
    rows.forEach(row => tbody.appendChild(row));
}

// Dropdown menu functionality
function toggleDropdown(branchId) {
    // Close all other dropdowns
    document.querySelectorAll('.dropdown-content').forEach(dropdown => {
        if (dropdown.id !== `dropdown-${branchId}`) {
            dropdown.style.display = 'none';
        }
    });
    
    // Toggle current dropdown
    const dropdown = document.getElementById(`dropdown-${branchId}`);
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

// Modal management functions
function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });
    document.getElementById('modalOverlay').style.display = 'none';
}

function showModal(modalId) {
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById(modalId).style.display = 'block';
}

// Add Branch Functions
function openAddForm() {
    resetAddForm();
    showModal('addBranchModal');
}

function closeAddForm() {
    document.getElementById('addBranchModal').style.display = 'none';
    document.getElementById('modalOverlay').style.display = 'none';
}

function resetAddForm() {
    document.getElementById('addBranchForm').reset();
}

// Edit Branch Functions
function openEditForm(branchId, branchName, location, managerId, contactNumber) {
    document.getElementById('edit_branch_id').value = branchId;
    document.getElementById('edit_branch_name').value = branchName;
    document.getElementById('edit_location').value = location;
    document.getElementById('edit_manager_id').value = managerId || '';
    document.getElementById('edit_contact_number').value = contactNumber || '';
    
    // Set form action
    document.getElementById('editBranchForm').action = `/branch/edit/${branchId}`;
    
    showModal('editBranchModal');
}

function closeEditForm() {
    document.getElementById('editBranchModal').style.display = 'none';
    document.getElementById('modalOverlay').style.display = 'none';
}

function submitEditForm() {
    const form = document.getElementById('editBranchForm');
    const formData = new FormData(form);
    
    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.log('Error:', error);
        alert('An error occurred while updating the branch.');
    });
}

// Delete Branch Functions
function openDeleteConfirm(branchId, branchName) {
    document.getElementById('deleteBranchName').textContent = branchName;
    document.getElementById('deleteForm').action = `/branch/delete/${branchId}`;
    showModal('deleteModal');
}

function closeDeleteConfirm() {
    document.getElementById('deleteModal').style.display = 'none';
    document.getElementById('modalOverlay').style.display = 'none';
}

// Warehouse Management Functions
function openWarehouseModal(branchId, branchName) {
    currentBranchId = branchId;
    document.getElementById('warehouseBranchName').textContent = branchName;
    document.getElementById('warehouse_branch_id').value = branchId;
    
    showModal('warehouseModal');
    loadWarehouses(branchId);
    closeWarehouseForm();
}

function closeWarehouseModal() {
    document.getElementById('warehouseModal').style.display = 'none';
    document.getElementById('modalOverlay').style.display = 'none';
    currentBranchId = null;
}

function loadWarehouses(branchId) {
    console.log('Loading warehouses for branch:', branchId);
    
    fetch(`/branch/${branchId}/warehouses`)
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received warehouse data:', data);
            
            // Handle both direct array and object with warehouses property
            const warehouses = Array.isArray(data) ? data : (data.warehouses || []);
            displayWarehouses(warehouses);
        })
        .catch(error => {
            console.error('Error loading warehouses:', error);
            
            // Show error message to user
            const tableBody = document.getElementById('warehouseTableBody');
            const emptyState = document.getElementById('emptyWarehouseState');
            const table = document.getElementById('warehouseTable');
            
            if (tableBody && emptyState && table) {
                table.style.display = 'none';
                emptyState.style.display = 'block';
                emptyState.innerHTML = `
                    <div class="text-center">
                        <i class="fas fa-exclamation-triangle" style="font-size: 2rem; color: #dc3545;"></i>
                        <p style="margin-top: 10px;">Error loading warehouses: ${error.message}</p>
                    </div>
                `;
            }
        });
}

function displayWarehouses(warehouses) {
    console.log('Displaying warehouses:', warehouses);
    
    const tableBody = document.getElementById('warehouseTableBody');
    const emptyState = document.getElementById('emptyWarehouseState');
    const table = document.getElementById('warehouseTable');
    
    // Check if elements exist
    if (!tableBody || !emptyState || !table) {
        console.error('Required DOM elements not found:', {
            tableBody: !!tableBody,
            emptyState: !!emptyState,
            table: !!table
        });
        return;
    }
    
    if (!warehouses || warehouses.length === 0) {
        console.log('No warehouses to display');
        table.style.display = 'none';
        emptyState.style.display = 'block';
        emptyState.innerHTML = `
            <div class="text-center">
                <i class="fas fa-warehouse" style="font-size: 2rem; color: #6c757d;"></i>
                <p style="margin-top: 10px;">No warehouses found for this branch.</p>
            </div>
        `;
        return;
    }
    
    console.log(`Displaying ${warehouses.length} warehouses`);
    table.style.display = 'table';
    emptyState.style.display = 'none';
    
    tableBody.innerHTML = warehouses.map(warehouse => {
        console.log('Processing warehouse:', warehouse);
        
        // Handle different possible property names
        const warehouseId = warehouse.warehouse_id || warehouse.id;
        const location = warehouse.location || '';
        const capacity = warehouse.capacity || 0;
        
        return `
            <tr>
                <td>
                    <span class="id-badge">#${warehouseId}</span>
                </td>
                <td>
                    <span class="location-badge">
                        <i class="fas fa-map-marker-alt"></i>
                        ${location}
                    </span>
                </td>
                <td>
                    <span class="capacity-badge">
                        <i class="fas fa-cubes"></i>
                        ${capacity}
                    </span>
                </td>
                <td>
                    <div class="action-buttons">
                        <button class="btn btn-sm btn-primary" onclick="openEditWarehouseForm(${warehouseId}, '${location.replace(/'/g, "\\'")}', ${capacity})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="openDeleteWarehouseConfirm(${warehouseId}, '${location.replace(/'/g, "\\'")}', ${capacity})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

// Warehouse Form Functions
function openAddWarehouseForm() {
    resetWarehouseForm();
    document.getElementById('warehouseFormTitle').innerHTML = '<i class="fas fa-plus"></i> Add New Warehouse';
    document.getElementById('saveWarehouseButtonText').textContent = 'Save Warehouse';
    document.getElementById('warehouseFormContainer').style.display = 'block';
    currentWarehouseId = null;
}

function openEditWarehouseForm(warehouseId, location, capacity) {
    document.getElementById('warehouse_id').value = warehouseId;
    document.getElementById('warehouseLocation').value = location;
    document.getElementById('capacity').value = capacity;
    
    document.getElementById('warehouseFormTitle').innerHTML = '<i class="fas fa-edit"></i> Edit Warehouse';
    document.getElementById('saveWarehouseButtonText').textContent = 'Update Warehouse';
    document.getElementById('warehouseFormContainer').style.display = 'block';
    currentWarehouseId = warehouseId;
}

function closeWarehouseForm() {
    document.getElementById('warehouseFormContainer').style.display = 'none';
    resetWarehouseForm();
}

function resetWarehouseForm() {
    document.getElementById('warehouseForm').reset();
    document.getElementById('warehouse_id').value = '';
    document.getElementById('warehouse_branch_id').value = currentBranchId;
}

// FIXED: Better error handling and validation in submitWarehouseForm
function submitWarehouseForm() {
    const form = document.getElementById('warehouseForm');
    
    // Validate form inputs
    const location = document.getElementById('warehouseLocation').value.trim();
    const capacity = document.getElementById('capacity').value.trim();
    
    if (!location) {
        alert('Please enter a warehouse location.');
        return;
    }
    
    if (!capacity || isNaN(capacity) || parseInt(capacity) <= 0) {
        alert('Please enter a valid capacity (positive number).');
        return;
    }
    
    if (!currentBranchId) {
        alert('Error: Branch ID is missing. Please try again.');
        return;
    }
    
    const formData = new FormData(form);
    
    // Ensure all required fields are in FormData
    if (!formData.get('location')) {
        formData.set('location', location);
    }
    if (!formData.get('capacity')) {
        formData.set('capacity', capacity);
    }
    
    const url = currentWarehouseId ? 
        `/warehouse/edit/${currentWarehouseId}` : 
        `/branch/${currentBranchId}/warehouse/add`;
    
    console.log('Submitting to URL:', url);
    console.log('Form data:', Object.fromEntries(formData));
    
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest' // This helps Flask identify AJAX requests
        }
    })
    .then(response => {
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        
        // Check if response is JSON
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return response.json();
        } else {
            // If not JSON, get text and throw error
            return response.text().then(text => {
                throw new Error(`Expected JSON response but got: ${text}`);
            });
        }
    })
    .then(data => {
        console.log('Response data:', data);
        
        if (data.success) {
            closeWarehouseForm();
            loadWarehouses(currentBranchId);
            showSuccessMessage('Warehouse saved successfully');
        } else {
            // Show both error and message if available
            const errorMsg = data.error || data.message || 'Unknown error occurred';
            alert('Error: ' + errorMsg);
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        
        // More detailed error message
        let errorMessage = 'An error occurred while saving the warehouse.';
        if (error.message.includes('JSON')) {
            errorMessage += ' The server returned an unexpected response format.';
        } else if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
            errorMessage += ' Please check your internet connection.';
        }
        
        alert(errorMessage + '\n\nDetailed error: ' + error.message);
    });
}

// Delete Warehouse Functions
function openDeleteWarehouseConfirm(warehouseId, location, capacity) {
    warehouseToDelete = warehouseId;
    
    document.getElementById('deleteWarehouseInfo').innerHTML = `
        <div class="warehouse-details">
            <p><strong>ID:</strong> #${warehouseId}</p>
            <p><strong>Location:</strong> ${location}</p>
            <p><strong>Capacity:</strong> ${capacity}</p>
        </div>
    `;
    
    showModal('deleteWarehouseModal');
}

function closeDeleteWarehouseConfirm() {
    document.getElementById('deleteWarehouseModal').style.display = 'none';
    document.getElementById('modalOverlay').style.display = 'none';
    warehouseToDelete = null;
}

function confirmDeleteWarehouse() {
    if (!warehouseToDelete) return;
    
    fetch(`/warehouse/delete/${warehouseToDelete}`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return response.json();
        } else {
            return response.text().then(text => {
                throw new Error(`Expected JSON response but got: ${text}`);
            });
        }
    })
    .then(data => {
        if (data.success) {
            closeDeleteWarehouseConfirm();
            loadWarehouses(currentBranchId);
            showSuccessMessage('Warehouse deleted successfully');
        } else {
            const errorMsg = data.error || data.message || 'Unknown error occurred';
            alert('Error: ' + errorMsg);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the warehouse.\n\nDetailed error: ' + error.message);
    });
}

// Utility function to show success messages
function showSuccessMessage(message) {
    // Simple implementation - you can replace this with your preferred notification system
    alert(message);
    
    // Alternative: Create a temporary success notification
    /*
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success';
    successDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        z-index: 9999;
    `;
    successDiv.textContent = message;
    document.body.appendChild(successDiv);
    setTimeout(() => successDiv.remove(), 3000);
    */
}



// Manager dropdown functionality
function initializeManagerDropdowns() {
    // Add event listeners for manager dropdowns
    const managerDropdowns = document.querySelectorAll('select[name="manager_id"]');
    
    managerDropdowns.forEach(dropdown => {
        dropdown.addEventListener('change', function() {
            handleManagerSelection(this.value, this.id);
        });
    });
}

// Handle manager selection
function handleManagerSelection(managerId, dropdownId) {
    if (managerId) {
        console.log(`Manager selected: ${managerId} from dropdown: ${dropdownId}`);
        
        // Optional: Load additional manager details
        // loadManagerDetails(managerId);
        
        // Optional: Update UI based on selection
        // updateUIForManagerSelection(managerId, dropdownId);
    } else {
        console.log('No manager selected');
    }
}