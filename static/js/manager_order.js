// Manager Orders JavaScript Functions
// Global variables for order items management
let orderItems = [];

// Initialize page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Set default date for order forms
    setDefaultDates();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Close modals when clicking outside
    initializeModalEvents();
});

// ===================== UTILITY FUNCTIONS =====================

function setDefaultDates() {
    const today = new Date().toISOString().split('T')[0];
    const orderDateInput = document.getElementById('add_order_date');
    const deliveryDateInput = document.getElementById('add_delivery_date');
    
    if (orderDateInput && !orderDateInput.value) {
        orderDateInput.value = today;
    }
    
    if (deliveryDateInput && !deliveryDateInput.value) {
        // Set delivery date to 7 days from today by default
        const deliveryDate = new Date();
        deliveryDate.setDate(deliveryDate.getDate() + 7);
        deliveryDateInput.value = deliveryDate.toISOString().split('T')[0];
    }
}

function initializeFormValidation() {
    // Add validation to quantity inputs
    const quantityInputs = document.querySelectorAll('input[type="number"]');
    quantityInputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value < 1) {
                this.setCustomValidity('Quantity must be greater than 0');
            } else {
                this.setCustomValidity('');
            }
        });
    });
}

function initializeModalEvents() {
    // Close modals when clicking outside
    window.addEventListener('click', function(event) {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'}"></i>
        ${message}
        <button class="close-alert" onclick="this.parentElement.remove()">&times;</button>
    `;
    
    // Add to flash messages container or create one
    let flashContainer = document.querySelector('.flash-messages');
    if (!flashContainer) {
        flashContainer = document.createElement('div');
        flashContainer.className = 'flash-messages';
        document.querySelector('.container').insertBefore(flashContainer, document.querySelector('.container').firstChild);
    }
    
    flashContainer.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// ===================== TABLE SORTING =====================

function sortTable(columnIndex) {
    const table = document.getElementById('ordersTable');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const header = table.querySelectorAll('th')[columnIndex];
    
    // Get current sort direction
    const currentSort = header.dataset.sortDirection || 'asc';
    const newSort = currentSort === 'asc' ? 'desc' : 'asc';
    
    // Reset all sort icons
    table.querySelectorAll('.sort-icon').forEach(icon => {
        icon.className = 'fas fa-sort sort-icon';
    });
    
    // Set new sort icon
    const sortIcon = header.querySelector('.sort-icon');
    sortIcon.className = `fas fa-sort-${newSort === 'asc' ? 'up' : 'down'} sort-icon`;
    header.dataset.sortDirection = newSort;
    
    // Sort rows
    rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();
        
        // Handle numeric sorting for ID column
        if (columnIndex === 0) {
            const aNum = parseInt(aText.replace('#', ''));
            const bNum = parseInt(bText.replace('#', ''));
            return newSort === 'asc' ? aNum - bNum : bNum - aNum;
        }
        
        // Handle date sorting
        if (columnIndex === 4 || columnIndex === 5) {
            const aDate = new Date(aText);
            const bDate = new Date(bText);
            return newSort === 'asc' ? aDate - bDate : bDate - aDate;
        }
        
        // Default string sorting
        return newSort === 'asc' ? aText.localeCompare(bText) : bText.localeCompare(aText);
    });
    
    // Reappend sorted rows
    rows.forEach(row => tbody.appendChild(row));
}

// ===================== DROPDOWN MENU =====================

function toggleMenu(button) {
    // Close all other dropdowns
    document.querySelectorAll('.dropdown-content').forEach(dropdown => {
        if (dropdown !== button.nextElementSibling) {
            dropdown.style.display = 'none';
        }
    });
    
    // Toggle current dropdown
    const dropdown = button.nextElementSibling;
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(event) {
    if (!event.target.closest('.dropdown')) {
        document.querySelectorAll('.dropdown-content').forEach(dropdown => {
            dropdown.style.display = 'none';
        });
    }
});

// ===================== ADD ORDER MODAL =====================

function openAddOrderForm() {
    // Reset form
    document.getElementById('addOrderForm').reset();
    
    // Clear order items
    orderItems = [];
    updateOrderItemsTable();
    
    // Set default dates
    setDefaultDates();
    
    // Show modal
    document.getElementById('addOrderModal').style.display = 'block';
}

function closeAddOrderForm() {
    document.getElementById('addOrderModal').style.display = 'none';
    orderItems = [];
}

// Handle add order form submission
document.getElementById('addOrderForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    // Add order items data
    formData.append('order_items', JSON.stringify(orderItems));
    
    fetch('/add_manager_order', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            closeAddOrderForm();
            location.reload(); // Refresh page to show new order
        } else {
            throw new Error('Failed to add order');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error adding order', 'error');
    });
});

// ===================== ORDER ITEMS MANAGEMENT =====================

function addOrderItem() {
    const productSelect = document.getElementById('add_product_id_for_item');
    const quantityInput = document.getElementById('add_item_quantity_for_order');
    
    const productId = productSelect.value;
    const quantity = parseInt(quantityInput.value);
    
    if (!productId || !quantity || quantity < 1) {
        showNotification('Please select a product and enter a valid quantity', 'error');
        return;
    }
    
    // Check if product already exists in order
    const existingItem = orderItems.find(item => item.product_id == productId);
    if (existingItem) {
        showNotification('Product already exists in this order', 'error');
        return;
    }
    
    // Get product name from select option
    const productName = productSelect.options[productSelect.selectedIndex].text;
    
    // Add to order items array
    orderItems.push({
        product_id: productId,
        product_name: productName,
        quantity: quantity
    });
    
    // Update table display
    updateOrderItemsTable();
    
    // Clear inputs
    productSelect.value = '';
    quantityInput.value = '';
    
    showNotification('Product added to order', 'success');
}

function updateOrderItemsTable() {
    const tableBody = document.getElementById('orderItemsTableBody');
    const emptyState = document.getElementById('orderItemsEmptyState');
    
    if (orderItems.length === 0) {
        tableBody.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    
    tableBody.innerHTML = orderItems.map((item, index) => `
        <tr>
            <td>${item.product_name}</td>
            <td>${item.quantity}</td>
            <td>
                <button type="button" class="btn-icon edit" onclick="editOrderItemInForm(${index})" title="Edit">
                    <i class="fas fa-edit"></i>
                </button>
                <button type="button" class="btn-icon delete" onclick="removeOrderItemFromForm(${index})" title="Remove">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function editOrderItemInForm(index) {
    const item = orderItems[index];
    
    // Set values in form
    document.getElementById('add_product_id_for_item').value = item.product_id;
    document.getElementById('add_item_quantity_for_order').value = item.quantity;
    
    // Remove from array (will be re-added when form is submitted)
    orderItems.splice(index, 1);
    updateOrderItemsTable();
}

function removeOrderItemFromForm(index) {
    orderItems.splice(index, 1);
    updateOrderItemsTable();
    showNotification('Product removed from order', 'success');
}

// ===================== EDIT ORDER MODAL =====================

function editOrder(orderId) {
    fetch(`/api/manager_orders/${orderId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showNotification(data.error, 'error');
                return;
            }
            
            // Populate form fields
            document.getElementById('edit_order_id').value = data.order_id;
            document.getElementById('edit_staff_id').value = data.staff_id;
            document.getElementById('edit_warehouse_id').value = data.warehouse_id;
            document.getElementById('edit_order_type').value = data.order_type;
            document.getElementById('edit_order_date').value = data.order_date;
            document.getElementById('edit_delivery_date').value = data.delivery_date;
            document.getElementById('edit_order_status').value = data.order_status;
            
            // Set form action
            document.getElementById('editOrderForm').action = `/edit_manager_order/${orderId}`;
            
            // Show modal
            document.getElementById('editOrderModal').style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error loading order details', 'error');
        });
}

function closeEditForm() {
    document.getElementById('editOrderModal').style.display = 'none';
}

// ===================== DELETE ORDER MODAL =====================

function deleteOrder(orderId) {
    // Set form action
    document.getElementById('deleteForm').action = `/delete_manager_order/${orderId}`;
    
    // Show modal
    document.getElementById('deleteModal').style.display = 'block';
}

function closeDeleteConfirm() {
    document.getElementById('deleteModal').style.display = 'none';
}

// ===================== ORDER ITEMS MODAL =====================

function viewOrderItems(orderId) {
    fetch(`/api/manager_order_items/${orderId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showNotification(data.error, 'error');
                return;
            }
            
            // Store order ID for adding new items
            document.getElementById('orderIdForItems').value = orderId;
            
            // Populate items table
            const tableBody = document.querySelector('#orderItemsModal tbody');
            if (data.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="4" class="text-center">No items found in this order</td>
                    </tr>
                `;
            } else {
                tableBody.innerHTML = data.map(item => `
                    <tr>
                        <td>${item.order_id_product_id || `${orderId}-${item.product_id}`}</td>
                        <td>${item.product_name || `Product ID: ${item.product_id}`}</td>
                        <td>${item.quantity}</td>
                        <td>
                            <button class="btn-icon edit" onclick="editOrderItem(${orderId}, ${item.product_id})" title="Edit">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn-icon delete" onclick="deleteOrderItem(${orderId}, ${item.product_id})" title="Delete">
                                <i class="fas fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                `).join('');
            }
            
            // Show modal
            document.getElementById('orderItemsModal').style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error loading order items', 'error');
        });
}

function closeOrderItemsModal() {
    document.getElementById('orderItemsModal').style.display = 'none';
}

// ===================== ADD ORDER ITEM MODAL =====================

function openAddOrderItemForm() {
    const orderId = document.getElementById('orderIdForItems').value;
    
    // Reset form
    document.getElementById('addOrderItemForm').reset();
    document.getElementById('add_item_order_id').value = orderId;
    
    // Show modal
    document.getElementById('addOrderItemModal').style.display = 'block';
}

function closeAddOrderItemForm() {
    document.getElementById('addOrderItemModal').style.display = 'none';
}

// Handle add order item form submission
document.getElementById('addOrderItemForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/add_manager_order_item', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showNotification(data.error, 'error');
        } else {
            showNotification(data.success, 'success');
            closeAddOrderItemForm();
            
            // Refresh order items table
            const orderId = document.getElementById('orderIdForItems').value;
            viewOrderItems(orderId);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error adding order item', 'error');
    });
});

// ===================== EDIT ORDER ITEM MODAL =====================

function editOrderItem(orderId, productId) {
    // Find the item data from the current table
    const rows = document.querySelectorAll('#orderItemsModal tbody tr');
    let itemData = null;
    
    rows.forEach(row => {
        const cells = row.cells;
        if (cells.length >= 3) {
            const itemId = cells[0].textContent.trim();
            if (itemId.includes(`${orderId}-${productId}`) || itemId.includes(productId)) {
                itemData = {
                    order_id: orderId,
                    product_id: productId,
                    quantity: parseInt(cells[2].textContent.trim())
                };
            }
        }
    });
    
    if (!itemData) {
        showNotification('Error loading item data', 'error');
        return;
    }
    
    // Populate form
    document.getElementById('edit_order_item_id').value = `${orderId}-${productId}`;
    document.getElementById('edit_item_order_id').value = orderId;
    document.getElementById('edit_item_product_id').value = productId;
    document.getElementById('edit_item_quantity').value = itemData.quantity;
    
    // Show modal
    document.getElementById('editOrderItemModal').style.display = 'block';
}

function closeEditOrderItemForm() {
    document.getElementById('editOrderItemModal').style.display = 'none';
}

// Handle edit order item form submission
document.getElementById('editOrderItemForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/edit_manager_order_item', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showNotification(data.error, 'error');
        } else {
            showNotification(data.success, 'success');
            closeEditOrderItemForm();
            
            // Refresh order items table
            const orderId = document.getElementById('edit_item_order_id').value;
            viewOrderItems(orderId);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error updating order item', 'error');
    });
});

// ===================== DELETE ORDER ITEM MODAL =====================

function deleteOrderItem(orderId, productId) {
    // Set form action
    document.getElementById('deleteOrderItemForm').action = `/delete_manager_order_item/${orderId}/${productId}`;
    
    // Show modal
    document.getElementById('deleteOrderItemModal').style.display = 'block';
}

function closeDeleteOrderItemConfirm() {
    document.getElementById('deleteOrderItemModal').style.display = 'none';
}

// Handle delete order item form submission
document.getElementById('deleteOrderItemForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    fetch(this.action, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showNotification(data.error, 'error');
        } else {
            showNotification(data.success, 'success');
            closeDeleteOrderItemConfirm();
            
            // Refresh order items table
            const orderId = document.getElementById('orderIdForItems').value;
            viewOrderItems(orderId);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error deleting order item', 'error');
    });
});

// ===================== SEARCH FUNCTIONALITY =====================

// Auto-submit search form on Enter key
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                this.closest('form').submit();
            }
        });
    }
});

// ===================== FORM VALIDATION =====================

function validateOrderForm(formId) {
    const form = document.getElementById(formId);
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }
    });
    
    // Validate dates
    const orderDate = form.querySelector('input[name="order_date"]');
    const deliveryDate = form.querySelector('input[name="delivery_date"]');
    
    if (orderDate && deliveryDate && orderDate.value && deliveryDate.value) {
        if (new Date(deliveryDate.value) < new Date(orderDate.value)) {
            deliveryDate.classList.add('error');
            showNotification('Delivery date cannot be before order date', 'error');
            isValid = false;
        } else {
            deliveryDate.classList.remove('error');
        }
    }
    
    return isValid;
}

// Add validation to forms
document.addEventListener('DOMContentLoaded', function() {
    const forms = ['addOrderForm', 'editOrderForm'];
    
    forms.forEach(formId => {
        const form = document.getElementById(formId);
        if (form) {
            form.addEventListener('submit', function(e) {
                if (!validateOrderForm(formId)) {
                    e.preventDefault();
                }
            });
        }
    });
});