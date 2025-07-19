// ===== Customer Order Management JavaScript =====

// ===== Global Variables =====
let orderItems = []; // Store order items temporarily
let allProducts = []; // Store all products for dropdowns

// ===== Modal Functions =====
function openAddOrderForm() {
    document.getElementById('addOrderModal').style.display = 'block';
    document.body.style.overflow = 'hidden';

    // Set default date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('add_order_date').value = today;

    // Clear address dropdown
    const addressSelect = document.getElementById('add_address_id');
    addressSelect.innerHTML = '<option value="">-- Select an address --</option>';

    // Clear order items
    orderItems = [];
    updateOrderItemsTable();
    updateTotalAmount();

    // Load products for order items
    loadProducts();
}

function closeAddOrderForm() {
    document.getElementById('addOrderModal').style.display = 'none';
    document.body.style.overflow = 'auto';

    // Clear form
    document.getElementById('addOrderForm').reset();

    // Reset address dropdown
    const addressSelect = document.getElementById('add_address_id');
    addressSelect.innerHTML = '<option value="">-- Select an address --</option>';

    // Clear order items
    orderItems = [];
    updateOrderItemsTable();
}

async function editOrder(orderId) {
    try {
        // Fetch order data
        const response = await fetch(`/api/orders/${orderId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch order data');
        }

        const order = await response.json();

        // Show modal first
        document.getElementById('editOrderModal').style.display = 'block';
        document.body.style.overflow = 'hidden';

        // Set form action
        document.getElementById('editOrderForm').action = `/edit_order/${orderId}`;

        // Populate form fields
        document.getElementById('edit_order_id').value = orderId;
        document.getElementById('edit_customer_id').value = order.customer_id;
        document.getElementById('edit_order_date').value = order.order_date;
        document.getElementById('edit_status').value = order.status;
        document.getElementById('edit_totalAmount').value = order.totalAmount;
        document.getElementById('edit_payment_method').value = order.payment_method;

        // Load addresses for the selected customer, then set the address
        await loadAddressesForCustomer(order.customer_id, 'edit');

        // Set the address after addresses are loaded
        setTimeout(() => {
            document.getElementById('edit_address_id').value = order.address_id;
        }, 100);

    } catch (error) {
        console.error('Error loading order data:', error);
        showNotification('Error loading order data. Please try again.', 'error');
    }
}

function closeEditForm() {
    document.getElementById('editOrderModal').style.display = 'none';
    document.body.style.overflow = 'auto';

    // Clear form
    document.getElementById('editOrderForm').reset();

    // Reset address dropdown
    const addressSelect = document.getElementById('edit_address_id');
    addressSelect.innerHTML = '<option value="">-- Select an address --</option>';
}

function deleteOrder(orderId) {
    document.getElementById('deleteModal').style.display = 'block';
    document.body.style.overflow = 'hidden';

    // Set form action for delete
    document.getElementById('deleteForm').action = `/delete_order/${orderId}`;
}

function closeDeleteConfirm() {
    document.getElementById('deleteModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

// ===== Order Items Functions =====
async function viewOrderItems(orderId) {
    try {
        // Show modal
        document.getElementById('orderItemsModal').style.display = 'block';
        document.body.style.overflow = 'hidden';
        document.getElementById('orderIdForItems').value = orderId;

        // Fetch order items
        const response = await fetch(`/api/orders/${orderId}/items`);
        if (!response.ok) {
            throw new Error('Failed to fetch order items');
        }

        const items = await response.json();
        console.log("Fetched order items:", items);
        populateOrderItemsModal(items);

    } catch (error) {
        console.error('Error loading order items:', error);
        showNotification('Error loading order items. Please try again.', 'error');
        closeOrderItemsModal();
    }
}

// FIXED: Consistent function for populating order items modal
function populateOrderItemsModal(items) {
    const tbody = document.querySelector('#orderItemsModal tbody');
    tbody.innerHTML = '';

    if (items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center">No items found for this order</td></tr>';
        return;
    }

    items.forEach(item => {
        // FIXED: Handle both possible field names for order item ID
        const orderItemId = item.order_item_id || item.Order_Item_id;
        const orderId = item.order_id || document.getElementById('orderIdForItems').value;

        if (!orderItemId) {
            console.error('Order Item ID is missing for item:', item);
            return;
        }

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${orderItemId}</td>
            <td>${item.product_name || `Product ID: ${item.product_id}`}</td>
            <td>${item.quantity}</td>
            <td class="actions">
                <div class="dropdown">
                    <button class="btn-icon menu" onclick="toggleMenu(this)">
                        <i class="fas fa-ellipsis-v"></i>
                    </button>
                    <div class="dropdown-content">
                        <a href="#" onclick="editOrderItem(${orderItemId}, ${orderId})">
                            <i class="fas fa-edit"></i> Edit
                        </a>
                        <a href="#" onclick="deleteOrderItem(${orderItemId})">
                            <i class="fas fa-trash"></i> Delete
                        </a>
                    </div>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function closeOrderItemsModal() {
    document.getElementById('orderItemsModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

async function openAddOrderItemForm() {
    const orderId = document.getElementById('orderIdForItems').value;

    document.getElementById('addOrderItemModal').style.display = 'block';
    document.getElementById('add_item_order_id').value = orderId;

    // Load products for the dropdown
    await loadProductsForOrderItems('add_product_id');
}

function closeAddOrderItemForm() {
    document.getElementById('addOrderItemModal').style.display = 'none';
    document.getElementById('addOrderItemForm').reset();
}

// FIXED: Edit order item function
async function editOrderItem(orderItemId, orderId) {
    try {
        console.log('Editing order item:', orderItemId, 'for order:', orderId);

        // Fetch order item data
        const response = await fetch(`/api/Customer_Order_Items/${orderItemId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch order item data');
        }

        const item = await response.json();
        console.log('Order item data:', item);

        // Show modal
        document.getElementById('editOrderItemModal').style.display = 'block';

        // Set form data
        document.getElementById('edit_order_item_id').value = orderItemId;
        document.getElementById('edit_item_order_id').value = orderId;
        document.getElementById('edit_item_quantity').value = item.quantity;

        // Load products and set selected
        await loadProductsForOrderItems('edit_item_product_id');
        document.getElementById('edit_item_product_id').value = item.product_id;
        document.getElementById('editOrderItemForm').addEventListener('submit', async function (e) {
            e.preventDefault(); // Prevent the default form submission

            const orderItemId = document.getElementById('edit_order_item_id').value;
            const orderId = document.getElementById('edit_item_order_id').value;
            const productId = document.getElementById('edit_item_product_id').value;
            const quantity = document.getElementById('edit_item_quantity').value;

            try {
                const response = await fetch(`/edit_order_item/${orderItemId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        product_id: productId,
                        quantity: quantity,
                        order_id: orderId
                    })
                });

                if (response.redirected) {
                    window.location.href = response.url; // Follow Flask's redirect
                } else {
                    const result = await response.json();
                    console.log('Update result:', result);
                }

            } catch (error) {
                console.error('Error submitting form:', error);
                alert('Error updating order item.');
            }
        });


    } catch (error) {
        console.error('Error loading order item data:', error);
        showNotification('Error loading order item data. Please try again.', 'error');
    }
}

function closeEditOrderItemForm() {
    document.getElementById('editOrderItemModal').style.display = 'none';
    document.getElementById('editOrderItemForm').reset();
}

// FIXED: Delete order item function
function deleteOrderItem(orderItemId) {
    console.log('Deleting order item:', orderItemId);

    if (!orderItemId || orderItemId === 'undefined') {
        console.error('Invalid order item ID:', orderItemId);
        showNotification('Error: Invalid item ID', 'error');
        return;
    }

    document.getElementById('deleteOrderItemModal').style.display = 'block';
    document.getElementById('deleteOrderItemForm').action = `/delete_order_item/${orderItemId}`;
}

function closeDeleteOrderItemConfirm() {
    document.getElementById('deleteOrderItemModal').style.display = 'none';
}

// REMOVED: Duplicate populateOrderItemsTable function to avoid confusion

// ===== Order Items for New Orders =====
async function addOrderItem() {
    const productId = document.getElementById('add_product_id_for_item').value;
    const quantity = document.getElementById('add_item_quantity_for_order').value;

    if (!productId || !quantity || quantity <= 0) {
        showNotification('Please select a product and enter a valid quantity', 'error');
        return;
    }

    // Find product details
    const product = allProducts.find(p => p.product_id == productId);
    if (!product) {
        showNotification('Product not found', 'error');
        return;
    }

    // Check if item already exists
    const existingIndex = orderItems.findIndex(item => item.product_id == productId);
    if (existingIndex >= 0) {
        // Update quantity
        orderItems[existingIndex].quantity = parseInt(quantity);
    } else {
        // Add new item
        orderItems.push({
            product_id: productId,
            product_name: product.product_name,
            price: product.price,
            quantity: parseInt(quantity)
        });
    }

    // Clear form
    document.getElementById('add_product_id_for_item').value = '';
    document.getElementById('add_item_quantity_for_order').value = '';

    // Update table and total
    updateOrderItemsTable();
    updateTotalAmount();
}

function removeOrderItem(index) {
    orderItems.splice(index, 1);
    updateOrderItemsTable();
    updateTotalAmount();
}

function updateOrderItemsTable() {
    const tbody = document.getElementById('orderItemsTableBody');
    const emptyState = document.getElementById('orderItemsEmptyState');

    tbody.innerHTML = '';

    if (orderItems.length === 0) {
        emptyState.style.display = 'block';
        return;
    }

    emptyState.style.display = 'none';

    orderItems.forEach((item, index) => {
        const subtotal = (item.price * item.quantity).toFixed(2);
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.product_name}</td>
            <td>${item.quantity}</td>
            <td>$${subtotal}</td>
            <td>
                <button type="button" class="btn btn-danger btn-sm" onclick="removeOrderItem(${index})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function updateTotalAmount() {
    const total = orderItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    document.getElementById('add_totalAmount').value = total.toFixed(2);
}

// ===== Product Loading Functions =====
async function loadProducts() {
    try {
        const response = await fetch('/api/products');
        if (response.ok) {
            allProducts = await response.json();
            populateProductDropdown('add_product_id_for_item', allProducts);
        }
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

async function loadProductsForOrderItems(selectId) {
    try {
        const response = await fetch('/api/products');
        if (response.ok) {
            const products = await response.json();
            populateProductDropdown(selectId, products);
        }
    } catch (error) {
        console.error('Error loading products:', error);
        showNotification('Error loading products. Please try again.', 'error');
    }
}

function populateProductDropdown(selectId, products) {
    const select = document.getElementById(selectId);
    if (!select) {
        console.error('Product select element not found:', selectId);
        return;
    }

    select.innerHTML = '<option value="">-- Select a product --</option>';

    products.forEach(product => {
        const option = document.createElement('option');
        option.value = product.product_id;
        option.textContent = `${product.product_name} - $${product.price}`;
        select.appendChild(option);
    });
}

// ===== Address Loading Functions =====
async function loadAddressesForCustomer(customerId, mode = 'add') {
    const addressSelect = document.getElementById(mode === 'add' ? 'add_address_id' : 'edit_address_id');

    if (!customerId) {
        addressSelect.innerHTML = '<option value="">-- Select an address --</option>';
        return;
    }

    // Show loading state
    addressSelect.innerHTML = '<option value="">Loading addresses...</option>';
    addressSelect.disabled = true;

    try {
        const response = await fetch(`/api/addresses/customer/${customerId}`);
        if (response.ok) {
            const addresses = await response.json();
            populateAddressSelect(addresses, mode);
        } else {
            throw new Error('Failed to load addresses');
        }
    } catch (error) {
        console.error('Error loading addresses:', error);
        addressSelect.innerHTML = '<option value="">Error loading addresses</option>';
        showNotification('Error loading addresses. Please try again.', 'error');
    } finally {
        addressSelect.disabled = false;
    }
}

function populateAddressSelect(addresses, mode = 'add') {
    const addressSelect = document.getElementById(mode === 'add' ? 'add_address_id' : 'edit_address_id');
    addressSelect.innerHTML = '<option value="">-- Select an address --</option>';

    if (addresses.length === 0) {
        addressSelect.innerHTML = '<option value="">No addresses found</option>';
        return;
    }

    addresses.forEach(address => {
        const option = document.createElement('option');
        option.value = address.address_id;

        // Create a readable address display
        let displayText = '';
        if (address.display) {
            displayText = address.display;
        } else {
            // Fallback to creating display text
            const parts = [];
            if (address.street_address) parts.push(address.street_address);
            if (address.city) parts.push(address.city);
            if (address.address_type) parts.push(`(${address.address_type})`);
            displayText = parts.join(', ') || `Address ID: ${address.address_id}`;
        }

        option.textContent = displayText;
        addressSelect.appendChild(option);
    });
}

// ===== Table Sorting Functions =====
let sortDirection = {};

function sortTable(columnIndex) {
    const table = document.getElementById('ordersTable');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    // Determine sort direction
    const direction = sortDirection[columnIndex] === 'asc' ? 'desc' : 'asc';
    sortDirection[columnIndex] = direction;

    // Sort rows
    rows.sort((a, b) => {
        const aValue = getCellValue(a, columnIndex);
        const bValue = getCellValue(b, columnIndex);

        if (direction === 'asc') {
            return aValue.localeCompare(bValue, undefined, { numeric: true });
        } else {
            return bValue.localeCompare(aValue, undefined, { numeric: true });
        }
    });

    // Reorder table rows
    rows.forEach(row => tbody.appendChild(row));

    // Update sort icons
    updateSortIcons(columnIndex, direction);
}

function getCellValue(row, columnIndex) {
    const cell = row.cells[columnIndex];
    return cell.textContent.trim();
}

function updateSortIcons(activeColumn, direction) {
    const headers = document.querySelectorAll('#ordersTable th');
    headers.forEach((header, index) => {
        const icon = header.querySelector('.sort-icon');
        if (icon) {
            icon.className = 'fas fa-sort sort-icon';
            if (index === activeColumn) {
                icon.className = direction === 'asc' ? 'fas fa-sort-up sort-icon' : 'fas fa-sort-down sort-icon';
            }
        }
    });
}

// ===== Menu Toggle Functions =====
function toggleMenu(button) {
    const dropdown = button.nextElementSibling;
    const isVisible = dropdown.style.display === 'block';

    // Hide all other dropdowns
    document.querySelectorAll('.dropdown-content').forEach(d => d.style.display = 'none');

    // Toggle current dropdown
    dropdown.style.display = isVisible ? 'none' : 'block';

    // Close dropdown when clicking outside
    if (!isVisible) {
        setTimeout(() => {
            document.addEventListener('click', function closeDropdown(e) {
                if (!button.contains(e.target) && !dropdown.contains(e.target)) {
                    dropdown.style.display = 'none';
                    document.removeEventListener('click', closeDropdown);
                }
            });
        }, 10);
    }
}

// ===== Notification Functions =====
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'}"></i>
        ${message}
        <button class="close-alert" onclick="this.parentElement.remove()">&times;</button>
    `;

    // Add to page
    let container = document.querySelector('.flash-messages');
    if (!container) {
        container = document.createElement('div');
        container.className = 'flash-messages';
        document.querySelector('.container').insertBefore(container, document.querySelector('.table-container'));
    }

    container.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// ===== Form Validation =====
function validateOrderForm(mode) {
    const prefix = mode === 'add' ? 'add' : 'edit';
    const customerId = document.getElementById(`${prefix}_customer_id`).value;
    const addressId = document.getElementById(`${prefix}_address_id`).value;
    const orderDate = document.getElementById(`${prefix}_order_date`).value;
    const status = document.getElementById(`${prefix}_status`).value;
    const totalAmount = document.getElementById(`${prefix}_totalAmount`).value;
    const paymentMethod = document.getElementById(`${prefix}_payment_method`).value;

    if (!customerId) {
        showNotification('Please select a customer', 'error');
        return false;
    }

    if (!addressId) {
        showNotification('Please select an address', 'error');
        return false;
    }

    if (!orderDate) {
        showNotification('Please select an order date', 'error');
        return false;
    }

    if (!status) {
        showNotification('Please select a status', 'error');
        return false;
    }

    if (!totalAmount || parseFloat(totalAmount) <= 0) {
        showNotification('Please enter a valid total amount greater than 0', 'error');
        return false;
    }

    if (!paymentMethod) {
        showNotification('Please select a payment method', 'error');
        return false;
    }

    // For add mode, validate order items
    if (mode === 'add' && orderItems.length === 0) {
        showNotification('Please add at least one item to the order', 'error');
        return false;
    }

    return true;
}

// ===== Event Listeners =====
document.addEventListener('DOMContentLoaded', function () {
    // Handle escape key to close modals
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            closeAddOrderForm();
            closeEditForm();
            closeDeleteConfirm();
            closeOrderItemsModal();
            closeAddOrderItemForm();
            closeEditOrderItemForm();
            closeDeleteOrderItemConfirm();
        }
    });

    // Customer selection change handler for loading addresses
    const addCustomerSelect = document.getElementById('add_customer_id');
    const editCustomerSelect = document.getElementById('edit_customer_id');

    if (addCustomerSelect) {
        addCustomerSelect.addEventListener('change', function () {
            const customerId = this.value;
            if (customerId) {
                loadAddressesForCustomer(customerId, 'add');
            } else {
                const addressSelect = document.getElementById('add_address_id');
                addressSelect.innerHTML = '<option value="">-- Select an address --</option>';
            }
        });
    }

    if (editCustomerSelect) {
        editCustomerSelect.addEventListener('change', function () {
            const customerId = this.value;
            if (customerId) {
                loadAddressesForCustomer(customerId, 'edit');
            } else {
                const addressSelect = document.getElementById('edit_address_id');
                addressSelect.innerHTML = '<option value="">-- Select an address --</option>';
            }
        });
    }

    // Form validation and submission
    const addOrderForm = document.getElementById('addOrderForm');
    const editOrderForm = document.getElementById('editOrderForm');

    if (addOrderForm) {
        addOrderForm.addEventListener('submit', function (e) {
            if (!validateOrderForm('add')) {
                e.preventDefault();
                return;
            }

            // Add order items as hidden inputs
            orderItems.forEach((item, index) => {
                const productInput = document.createElement('input');
                productInput.type = 'hidden';
                productInput.name = `items[${index}][product_id]`;
                productInput.value = item.product_id;
                this.appendChild(productInput);

                const quantityInput = document.createElement('input');
                quantityInput.type = 'hidden';
                quantityInput.name = `items[${index}][quantity]`;
                quantityInput.value = item.quantity;
                this.appendChild(quantityInput);
            });
        });
    }

    if (editOrderForm) {
        editOrderForm.addEventListener('submit', function (e) {
            if (!validateOrderForm('edit')) {
                e.preventDefault();
            }
        });
    }

    // Order item form submissions
    const addOrderItemForm = document.getElementById('addOrderItemForm');
    const editOrderItemForm = document.getElementById('editOrderItemForm');

    if (addOrderItemForm) {
        addOrderItemForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formData = new FormData(this);

            try {
                const response = await fetch('/add_order_item', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    showNotification('Order item added successfully!', 'success');
                    closeAddOrderItemForm();

                    // Refresh order items view
                    const orderId = document.getElementById('orderIdForItems').value;
                    viewOrderItems(orderId);
                } else {
                    const error = await response.text();
                    showNotification('Error adding order item: ' + error, 'error');
                }
            } catch (error) {
                console.error('Error adding order item:', error);
                showNotification('Error adding order item. Please try again.', 'error');
            }
        });
    }

    if (editOrderItemForm) {
        editOrderItemForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formData = new FormData(this);
            const orderItemId = document.getElementById('edit_order_item_id').value;

            try {
                const response = await fetch(`/edit_order_item/${orderItemId}`, {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    showNotification('Order item updated successfully!', 'success');
                    closeEditOrderItemForm();

                    // Refresh order items view
                    const orderId = document.getElementById('orderIdForItems').value;
                    viewOrderItems(orderId);
                } else {
                    const error = await response.text();
                    showNotification('Error updating order item: ' + error, 'error');
                }
            } catch (error) {
                console.error('Error updating order item:', error);
                showNotification('Error updating order item. Please try again.', 'error');
            }
        });
    }

    // Close modal when clicking outside
    window.addEventListener('click', function (e) {
        const modals = ['addOrderModal', 'editOrderModal', 'deleteModal', 'orderItemsModal', 'addOrderItemModal', 'editOrderItemModal', 'deleteOrderItemModal'];
        modals.forEach(modalId => {
            const modal = document.getElementById(modalId);
            if (e.target === modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    });

    // Auto-dismiss flash messages after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            if (alert.parentElement) {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 300);
            }
        });
    }, 5000);
});