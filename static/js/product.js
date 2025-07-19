// Product Management JavaScript Functions
document.addEventListener('DOMContentLoaded', function() {
    // Initialize table sorting if products exist
    const productTable = document.getElementById('productTable');
    if (productTable) {
        initializeTableSorting();
    }

    // Auto-hide flash messages
    setTimeout(function() {
        const flashMessages = document.querySelectorAll('.alert');
        flashMessages.forEach(function(message) {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        });
    }, 5000);

    // Handle form submissions
    setupFormSubmissions();
});

// Modal Management Functions
function openAddForm() {
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById('addProductModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // Focus on first input
    setTimeout(() => {
        document.getElementById('product_name').focus();
    }, 100);
}

function closeAddForm() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('addProductModal').style.display = 'none';
    document.body.style.overflow = 'auto';
    resetAddForm();
}

function resetAddForm() {
    const form = document.getElementById('addProductForm');
    if (form) {
        form.reset();
    }
}

function openEditForm(productId, productName, description, price, stockQuantity, categoryId, supplierId, warehouseId) {
    // Set form action
    const editForm = document.getElementById('editProductForm');
    editForm.action = `/product/edit/${productId}`;
    
    // Populate form fields
    document.getElementById('edit_product_id').value = productId;
    document.getElementById('edit_product_name').value = productName;
    document.getElementById('edit_description').value = description || '';
    document.getElementById('edit_price').value = price;
    document.getElementById('edit_stock_quantity').value = stockQuantity;
    
    // Set selected options
    if (categoryId && categoryId !== 'null') {
        document.getElementById('edit_category_id').value = categoryId;
    }
    if (supplierId && supplierId !== 'null') {
        document.getElementById('edit_supplier_id').value = supplierId;
    }
    if (warehouseId && warehouseId !== 'null') {
        document.getElementById('edit_warehouse_id').value = warehouseId;
    }

    // Show modal
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById('editProductModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // Focus on first input
    setTimeout(() => {
        document.getElementById('edit_product_name').focus();
    }, 100);
}

function closeEditForm() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('editProductModal').style.display = 'none';
    document.body.style.overflow = 'auto';
    
    // Reset form
    const form = document.getElementById('editProductForm');
    if (form) {
        form.reset();
    }
}

function openDeleteConfirm(productId, productName) {
    // Set form action
    const deleteForm = document.getElementById('deleteForm');
    deleteForm.action = `/product/delete/${productId}`;
    
    // Set product details
    document.getElementById('delete_product_id').value = productId;
    document.getElementById('deleteProductName').textContent = productName;

    // Show modal
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById('deleteModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeDeleteConfirm() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('deleteModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function closeAllModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.style.display = 'none';
    });
    document.getElementById('modalOverlay').style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Table Sorting Functions
let sortColumn = -1;
let sortDirection = 'asc';

function sortTable(columnIndex) {
    const table = document.getElementById('productTable');
    const tbody = table.getElementsByTagName('tbody')[0];
    const rows = Array.from(tbody.getElementsByTagName('tr'));
    
    // Update sort direction
    if (sortColumn === columnIndex) {
        sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
        sortDirection = 'asc';
        sortColumn = columnIndex;
    }
    
    // Update sort icons
    updateSortIcons(columnIndex, sortDirection);
    
    // Sort rows
    rows.sort((a, b) => {
        let aValue = getCellValue(a, columnIndex);
        let bValue = getCellValue(b, columnIndex);
        
        // Handle numeric columns (ID, Price, Stock)
        if (columnIndex === 0 || columnIndex === 2 || columnIndex === 3) {
            aValue = parseFloat(aValue.replace(/[^\d.-]/g, '')) || 0;
            bValue = parseFloat(bValue.replace(/[^\d.-]/g, '')) || 0;
        }
        
        if (sortDirection === 'asc') {
            return aValue > bValue ? 1 : aValue < bValue ? -1 : 0;
        } else {
            return aValue < bValue ? 1 : aValue > bValue ? -1 : 0;
        }
    });
    
    // Reinsert sorted rows
    rows.forEach(row => tbody.appendChild(row));
}

function getCellValue(row, columnIndex) {
    const cell = row.cells[columnIndex];
    if (!cell) return '';
    
    // Get text content, excluding icons and buttons
    let text = cell.textContent || cell.innerText || '';
    
    // For linked columns (category, supplier, warehouse), get the link text
    const link = cell.querySelector('a');
    if (link) {
        text = link.textContent || link.innerText || '';
    }
    
    return text.trim();
}

function updateSortIcons(activeColumn, direction) {
    const headers = document.querySelectorAll('#productTable th .sort-icon');
    
    headers.forEach((icon, index) => {
        if (index === activeColumn) {
            icon.className = `fas fa-sort-${direction === 'asc' ? 'up' : 'down'} sort-icon active`;
        } else {
            icon.className = 'fas fa-sort sort-icon';
        }
    });
}

function initializeTableSorting() {
    // Add click listeners to sortable headers
    const sortableHeaders = document.querySelectorAll('#productTable th[onclick]');
    sortableHeaders.forEach((header, index) => {
        header.style.cursor = 'pointer';
        header.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(0, 123, 255, 0.1)';
        });
        header.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
}

// Form Submission Handling
function setupFormSubmissions() {
    // Add Product Form
    const addForm = document.getElementById('addProductForm');
    if (addForm) {
        addForm.addEventListener('submit', function(e) {
            if (!validateProductForm(this)) {
                e.preventDefault();
                return false;
            }
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
            submitBtn.disabled = true;
            
            // Re-enable button after a delay (in case of errors)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 5000);
        });
    }
    
    // Edit Product Form
    const editForm = document.getElementById('editProductForm');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            if (!validateProductForm(this)) {
                e.preventDefault();
                return false;
            }
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Updating...';
            submitBtn.disabled = true;
            
            // Re-enable button after a delay (in case of errors)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 5000);
        });
    }
    
    // Delete Form
    const deleteForm = document.getElementById('deleteForm');
    if (deleteForm) {
        deleteForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Deleting...';
            submitBtn.disabled = true;
            
            // Re-enable button after a delay (in case of errors)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 5000);
        });
    }
}

// Form Validation
function validateProductForm(form) {
    let isValid = true;
    const errors = [];
    
    // Product Name
    const productName = form.querySelector('[name="product_name"]');
    if (!productName.value.trim()) {
        errors.push('Product name is required');
        isValid = false;
    }
    
    // Price
    const price = form.querySelector('[name="price"]');
    if (!price.value || parseFloat(price.value) < 0) {
        errors.push('Valid price is required');
        isValid = false;
    }
    
    // Stock Quantity
    const stockQuantity = form.querySelector('[name="stock_quantity"]');
    if (!stockQuantity.value || parseInt(stockQuantity.value) < 0) {
        errors.push('Valid stock quantity is required');
        isValid = false;
    }
    
    // Category
    const category = form.querySelector('[name="category_id"]');
    if (!category.value) {
        errors.push('Category is required');
        isValid = false;
    }
    
    // Supplier
    const supplier = form.querySelector('[name="supplier_id"]');
    if (!supplier.value) {
        errors.push('Supplier is required');
        isValid = false;
    }
    
    // Warehouse
    const warehouse = form.querySelector('[name="warehouse_id"]');
    if (!warehouse.value) {
        errors.push('Warehouse is required');
        isValid = false;
    }
    
    // Show errors if any
    if (!isValid) {
        showValidationErrors(errors);
    }
    
    return isValid;
}

function showValidationErrors(errors) {
    // Remove existing error messages
    const existingErrors = document.querySelectorAll('.validation-error');
    existingErrors.forEach(error => error.remove());
    
    // Create error container
    const errorContainer = document.createElement('div');
    errorContainer.className = 'alert alert-error validation-error';
    errorContainer.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        <div>
            <strong>Please fix the following errors:</strong>
            <ul style="margin: 5px 0 0 20px;">
                ${errors.map(error => `<li>${error}</li>`).join('')}
            </ul>
        </div>
        <button class="close-alert" onclick="this.parentElement.remove()">×</button>
    `;
    
    // Insert at the top of the modal body
    const activeModal = document.querySelector('.modal[style*="block"] .modal-body');
    if (activeModal) {
        activeModal.insertBefore(errorContainer, activeModal.firstChild);
    }
}

// Keyboard Navigation
document.addEventListener('keydown', function(e) {
    // Close modals with Escape key
    if (e.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal[style*="block"]');
        if (openModals.length > 0) {
            closeAllModals();
        }
    }
    
    // Submit forms with Ctrl+Enter
    if (e.ctrlKey && e.key === 'Enter') {
        const activeModal = document.querySelector('.modal[style*="block"]');
        if (activeModal) {
            const submitBtn = activeModal.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.click();
            }
        }
    }
});

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-US').format(number);
}

// Search functionality enhancement
function enhanceSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        // Add real-time search suggestion (optional)
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            if (query.length > 2) {
                highlightSearchResults(query);
            } else {
                clearHighlights();
            }
        });
    }
}

function highlightSearchResults(query) {
    const rows = document.querySelectorAll('#productTable tbody tr');
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        let hasMatch = false;
        
        cells.forEach(cell => {
            const text = cell.textContent.toLowerCase();
            if (text.includes(query)) {
                hasMatch = true;
            }
        });
        
        row.style.opacity = hasMatch ? '1' : '0.5';
    });
}

function clearHighlights() {
    const rows = document.querySelectorAll('#productTable tbody tr');
    rows.forEach(row => {
        row.style.opacity = '1';
    });
}

// Stock level indicators
function updateStockIndicators() {
    const stockCells = document.querySelectorAll('.stock-badge');
    stockCells.forEach(cell => {
        const quantity = parseInt(cell.textContent);
        
        // Remove existing classes
        cell.classList.remove('low-stock', 'medium-stock', 'high-stock', 'out-of-stock');
        
        // Add appropriate class based on stock level
        if (quantity === 0) {
            cell.classList.add('out-of-stock');
            cell.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${quantity}`;
        } else if (quantity < 10) {
            cell.classList.add('low-stock');
            cell.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${quantity}`;
        } else if (quantity < 50) {
            cell.classList.add('medium-stock');
            cell.innerHTML = `<i class="fas fa-info-circle"></i> ${quantity}`;
        } else {
            cell.classList.add('high-stock');
            cell.innerHTML = `<i class="fas fa-check-circle"></i> ${quantity}`;
        }
    });
}

// Initialize enhancements when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    enhanceSearch();
    updateStockIndicators();
    
    // Add tooltips to action buttons
    addTooltips();
    
    // Initialize responsive table features
    initializeResponsiveTable();
});

function addTooltips() {
    const actionButtons = document.querySelectorAll('.btn-icon');
    actionButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            const title = this.getAttribute('title');
            if (title) {
                showTooltip(this, title);
            }
        });
        
        button.addEventListener('mouseleave', function() {
            hideTooltip();
        });
    });
}

function showTooltip(element, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
    
    setTimeout(() => tooltip.classList.add('show'), 10);
}

function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

function initializeResponsiveTable() {
    // Add mobile-friendly features for smaller screens
    if (window.innerWidth <= 768) {
        const table = document.getElementById('productTable');
        if (table) {
            table.classList.add('mobile-responsive');
        }
    }
}

// Handle window resize
window.addEventListener('resize', function() {
    initializeResponsiveTable();
});

// Export functionality (optional)
function exportToCSV() {
    const table = document.getElementById('productTable');
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    for (let i = 0; i < rows.length - 1; i++) { // Exclude last row (actions)
        let row = [];
        const cols = rows[i].querySelectorAll('td, th');
        
        for (let j = 0; j < cols.length - 1; j++) { // Exclude actions column
            let text = cols[j].textContent.trim();
            // Clean up text (remove extra spaces, newlines)
            text = text.replace(/\s+/g, ' ');
            row.push('"' + text + '"');
        }
        csv.push(row.join(','));
    }
    
    // Download CSV
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', 'products_export.csv');
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Bulk operations (future enhancement)
function toggleBulkMode() {
    const checkboxes = document.querySelectorAll('.row-checkbox');
    const bulkActions = document.querySelector('.bulk-actions');
    
    if (checkboxes.length === 0) {
        // Add checkboxes to each row
        addBulkCheckboxes();
    } else {
        // Remove checkboxes
        removeBulkCheckboxes();
    }
}

function addBulkCheckboxes() {
    const rows = document.querySelectorAll('#productTable tbody tr');
    rows.forEach(row => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'row-checkbox';
        
        const cell = document.createElement('td');
        cell.appendChild(checkbox);
        row.insertBefore(cell, row.firstChild);
    });
    
    // Add header checkbox
    const headerRow = document.querySelector('#productTable thead tr');
    const headerCell = document.createElement('th');
    const headerCheckbox = document.createElement('input');
    headerCheckbox.type = 'checkbox';
    headerCheckbox.addEventListener('change', function() {
        const checkboxes = document.querySelectorAll('.row-checkbox');
        checkboxes.forEach(cb => cb.checked = this.checked);
    });
    headerCell.appendChild(headerCheckbox);
    headerRow.insertBefore(headerCell, headerRow.firstChild);
}

function removeBulkCheckboxes() {
    const checkboxes = document.querySelectorAll('.row-checkbox');
    checkboxes.forEach(cb => {
        cb.closest('td').remove();
    });
    
    // Remove header checkbox
    const headerCheckbox = document.querySelector('#productTable thead input[type="checkbox"]');
    if (headerCheckbox) {
        headerCheckbox.closest('th').remove();
    }
}

// Performance optimization: Lazy loading for large tables
function initializeLazyLoading() {
    const rows = document.querySelectorAll('#productTable tbody tr');
    if (rows.length > 100) {
        // Show only first 50 rows initially
        for (let i = 50; i < rows.length; i++) {
            rows[i].style.display = 'none';
        }
        
        // Add "Load More" button
        const loadMoreBtn = document.createElement('button');
        loadMoreBtn.className = 'btn btn-secondary load-more';
        loadMoreBtn.innerHTML = '<i class="fas fa-chevron-down"></i> Load More Products';
        loadMoreBtn.addEventListener('click', loadMoreRows);
        
        const tableContainer = document.querySelector('.table-container');
        tableContainer.appendChild(loadMoreBtn);
    }
}

function loadMoreRows() {
    const hiddenRows = document.querySelectorAll('#productTable tbody tr[style*="none"]');
    const rowsToShow = Math.min(50, hiddenRows.length);
    
    for (let i = 0; i < rowsToShow; i++) {
        hiddenRows[i].style.display = '';
    }
    
    // Remove button if no more rows to show
    if (hiddenRows.length <= rowsToShow) {
        const loadMoreBtn = document.querySelector('.load-more');
        if (loadMoreBtn) {
            loadMoreBtn.remove();
        }
    }
}


function showWarehouseDetails(warehouseId, warehouseName) {
    // You can expand this to fetch more details via AJAX if needed
    alert(`Warehouse Details:\nID: ${warehouseId}\nName: ${warehouseName}`);
    
    // OR show a modal (see HTML below)
    document.getElementById('warehouseModal').style.display = 'block';
    document.getElementById('modalWarehouseName').textContent = warehouseName;
    document.getElementById('modalWarehouseId').textContent = warehouseId;
}

function closeWarehouseModal() {
    document.getElementById('warehouseModal').style.display = 'none';
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById('warehouseModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}