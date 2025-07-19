// Dashboard JavaScript Functionality

// Tab Navigation
document.addEventListener('DOMContentLoaded', function() {
    const navItems = document.querySelectorAll('.nav-item');
    const tabContents = document.querySelectorAll('.tab-content');
    
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Remove active class from all nav items and tab contents
            navItems.forEach(nav => nav.classList.remove('active'));
            tabContents.forEach(tab => tab.classList.remove('active'));
            
            // Add active class to clicked nav item and corresponding tab
            this.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
});

// Form field configurations for each entity
const entityForms = {
    branch: [
        { name: 'branch_id', label: 'Branch ID', type: 'text', required: true },
        { name: 'branch_name', label: 'Branch Name', type: 'text', required: true },
        { name: 'location', label: 'Location', type: 'text', required: true },
        { name: 'capacity', label: 'Capacity', type: 'number', required: true }
    ],
    supplier: [
        { name: 'supplier_id', label: 'Supplier ID', type: 'text', required: true },
        { name: 'supplier_name', label: 'Supplier Name', type: 'text', required: true },
        { name: 'phone', label: 'Phone', type: 'tel', required: true },
        { name: 'email', label: 'Email', type: 'email', required: false },
        { name: 'address', label: 'Address', type: 'textarea', required: false }
    ],
    product: [
        { name: 'product_id', label: 'Product ID', type: 'text', required: true },
        { name: 'product_name', label: 'Product Name', type: 'text', required: true },
        { name: 'description', label: 'Description', type: 'textarea', required: true },
        { name: 'price', label: 'Price', type: 'number', step: '0.01', required: true },
        { name: 'stock_quantity', label: 'Stock Quantity', type: 'number', required: true },
        { name: 'category_id', label: 'Category ID', type: 'text', required: true },
        { name: 'supplier_id', label: 'Supplier ID', type: 'text', required: true },
        { name: 'warehouse_id', label: 'Warehouse ID', type: 'text', required: true }
    ],
    warehouse: [
        { name: 'warehouse_id', label: 'Warehouse ID', type: 'text', required: true },
        { name: 'location', label: 'Location', type: 'text', required: true },
        { name: 'capacity', label: 'Capacity', type: 'number', required: true },
        { name: 'branch_id', label: 'Branch ID', type: 'text', required: true }
    ],
    category: [
        { name: 'category_id', label: 'Category ID', type: 'text', required: true },
        { name: 'category_name', label: 'Category Name', type: 'text', required: true },
        { name: 'category_description', label: 'Description', type: 'textarea', required: false }
    ],
    manager: [
        { name: 'user_id', label: 'User ID', type: 'text', required: true },
        { name: 'first_name', label: 'First Name', type: 'text', required: true },
        { name: 'last_name', label: 'Last Name', type: 'text', required: true },
        { name: 'warehouse_id', label: 'Warehouse ID', type: 'text', required: true },
        { name: 'delivery_date', label: 'Delivery Date', type: 'date', required: false },
        { name: 'order_details', label: 'Order Details', type: 'textarea', required: false }
    ],
    customer: [
        { name: 'customer_id', label: 'Customer ID', type: 'text', required: true },
        { name: 'order_id', label: 'Order ID', type: 'text', required: true },
        { name: 'product_id', label: 'Product ID', type: 'text', required: true },
        { name: 'quantity', label: 'Quantity', type: 'number', required: true },
        { name: 'order_date', label: 'Order Date', type: 'date', required: false }
    ]
};

// Modal functions
function showAddForm(entityType) {
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modal-title');
    const formFields = document.getElementById('form-fields');
    
    modalTitle.textContent = `Add New ${entityType.charAt(0).toUpperCase() + entityType.slice(1)}`;
    
    // Clear existing form fields
    formFields.innerHTML = '';
    
    // Generate form fields based on entity type
    const fields = entityForms[entityType] || [];
    fields.forEach(field => {
        const formGroup = document.createElement('div');
        formGroup.className = 'form-group';
        
        const label = document.createElement('label');
        label.textContent = field.label;
        if (field.required) {
            label.innerHTML += ' <span style="color: red;">*</span>';
        }
        
        let input;
        if (field.type === 'textarea') {
            input = document.createElement('textarea');
            input.rows = 3;
        } else {
            input = document.createElement('input');
            input.type = field.type;
            if (field.step) {
                input.step = field.step;
            }
        }
        
        input.name = field.name;
        input.id = field.name;
        input.required = field.required;
        
        formGroup.appendChild(label);
        formGroup.appendChild(input);
        formFields.appendChild(formGroup);
    });
    
    modal.classList.add('show');
}

function editItem(entityType, itemId) {
    showAddForm(entityType);
    const modalTitle = document.getElementById('modal-title');
    modalTitle.textContent = `Edit ${entityType.charAt(0).toUpperCase() + entityType.slice(1)}`;
    
    // Here you would typically populate the form with existing data
    // For demo purposes, we'll just change the title
    console.log(`Editing ${entityType} with ID: ${itemId}`);
}

function deleteItem(entityType, itemId) {
    if (confirm(`Are you sure you want to delete this ${entityType}?`)) {
        console.log(`Deleting ${entityType} with ID: ${itemId}`);
        // Here you would typically make an API call to delete the item
        // For demo purposes, we'll just log it
        
        // Show success message
        showNotification(`${entityType.charAt(0).toUpperCase() + entityType.slice(1)} deleted successfully!`, 'success');
    }
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.classList.remove('show');
    
    // Clear form
    const form = document.getElementById('item-form');
    form.reset();
}

// Form submission
document.getElementById('item-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    console.log('Form submitted with data:', data);
    
    // Here you would typically send the data to your backend API
    // For demo purposes, we'll just show a success message
    showNotification('Item saved successfully!', 'success');
    
    closeModal();
});

// Notification system
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">&times;</button>
    `;
    
    // Add notification styles if not already added
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 90px;
                right: 20px;
                background: white;
                border-radius: 8px;
                padding: 1rem 1.5rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                z-index: 3000;
                animation: slideInRight 0.3s ease-out;
                min-width: 300px;
            }
            
            .notification-success {
                border-left: 4px solid #28a745;
                color: #155724;
            }
            
            .notification-error {
                border-left: 4px solid #dc3545;
                color: #721c24;
            }
            
            .notification-info {
                border-left: 4px solid #17a2b8;
                color: #0c5460;
            }
            
            .notification button {
                background: none;
                border: none;
                font-size: 1.2rem;
                cursor: pointer;
                color: #6c757d;
                padding: 0;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Close modal when clicking outside
document.getElementById('modal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeModal();
    }
});

// Mobile menu toggle (for responsive design)
function toggleMobileMenu() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('mobile-open');
}

// Search functionality (basic implementation)
function searchTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    const rows = table.getElementsByTagName('tr');
    
    input.addEventListener('keyup', function() {
        const filter = this.value.toLowerCase();
        
        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const cells = row.getElementsByTagName('td');
            let found = false;
            
            for (let j = 0; j < cells.length - 1; j++) { // -1 to exclude actions column
                if (cells[j].textContent.toLowerCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
            
            row.style.display = found ? '' : 'none';
        }
    });
}

// Initialize search for all tables when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Add search inputs to each table section
    const tableContainers = document.querySelectorAll('.data-table');
    tableContainers.forEach((container, index) => {
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Search...';
        searchInput.className = 'search-input';
        searchInput.style.cssText = `
            margin-bottom: 1rem;
            padding: 0.5rem;
            border: 2px solid #e9ecef;
            border-radius: 6px;
            width: 300px;
        `;
        
        container.parentElement.insertBefore(searchInput, container);
        
        // Add search functionality
        const table = container.querySelector('table');
        if (table) {
            searchInput.addEventListener('keyup', function() {
                const filter = this.value.toLowerCase();
                const rows = table.getElementsByTagName('tr');
                
                for (let i = 1; i < rows.length; i++) {
                    const row = rows[i];
                    const cells = row.getElementsByTagName('td');
                    let found = false;
                    
                    for (let j = 0; j < cells.length - 1; j++) {
                        if (cells[j].textContent.toLowerCase().indexOf(filter) > -1) {
                            found = true;
                            break;
                        }
                    }
                    
                    row.style.display = found ? '' : 'none';
                }
            });
        }
    });
});

// Export functionality (basic CSV export)
function exportToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    const rows = Array.from(table.querySelectorAll('tr'));
    
    const csvContent = rows.map(row => {
        const cells = Array.from(row.querySelectorAll('th, td'));
        return cells.slice(0, -1).map(cell => `"${cell.textContent}"`).join(',');
    }).join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Print functionality
function printTable(tableId) {
    const table = document.getElementById(tableId);
    const printWindow = window.open('', '_blank');
    
    printWindow.document.write(`
        <html>
            <head>
                <title>Print Table</title>
                <style>
                    body { font-family: Arial, sans-serif; }
                    table { width: 100%; border-collapse: collapse; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                </style>
            </head>
            <body>
                ${table.outerHTML}
            </body>
        </html>
    `);
    
    printWindow.document.close();
    printWindow.print();
}