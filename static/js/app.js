// API Base URL
const API_BASE = '/api';

// State
let currentPage = 1;
let currentSearch = '';
let currentStatus = '';
let editingProductId = null;
let editingWebhookId = null;

// Initialize app
// Initialize app
// (Moved to bottom)

// ===== UPLOAD FUNCTIONALITY =====
function initializeUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');

    // Click to upload
    uploadArea.addEventListener('click', () => fileInput.click());

    // File selection
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');

        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });
}

async function handleFileUpload(file) {
    if (!file.name.endsWith('.csv')) {
        showNotification('Please upload a CSV file', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            showNotification('File uploaded successfully! Processing...', 'success');
            startProgressTracking(data.task_id);
        } else {
            showNotification(data.detail || 'Upload failed', 'error');
        }
    } catch (error) {
        showNotification('Error uploading file: ' + error.message, 'error');
    }
}

function startProgressTracking(taskId) {
    const progressContainer = document.getElementById('progressContainer');
    const progressFill = document.getElementById('progressFill');
    const progressStatus = document.getElementById('progressStatus');
    const progressPercentage = document.getElementById('progressPercentage');

    progressContainer.classList.add('active');

    // Connect to SSE endpoint
    const eventSource = new EventSource(`${API_BASE}/progress/${taskId}`);

    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);

        progressFill.style.width = `${data.percentage || 0}%`;
        progressPercentage.textContent = `${data.percentage || 0}%`;
        progressStatus.textContent = data.status || 'Processing...';

        if (data.status === 'complete') {
            eventSource.close();
            showNotification(data.message || 'Import completed successfully!', 'success');
            setTimeout(() => {
                progressContainer.classList.remove('active');
                loadProducts();
            }, 2000);
        } else if (data.status === 'error') {
            eventSource.close();
            showNotification(data.error || 'Import failed', 'error');
            setTimeout(() => {
                progressContainer.classList.remove('active');
            }, 2000);
        }
    };

    eventSource.onerror = () => {
        eventSource.close();
        showNotification('Connection error. Please refresh the page.', 'error');
    };
}

// ===== PRODUCT FUNCTIONALITY =====
function initializeProducts() {
    const addProductBtn = document.getElementById('addProductBtn');
    const bulkDeleteBtn = document.getElementById('bulkDeleteBtn');
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');
    const productModal = document.getElementById('productModal');
    const closeProductModal = document.getElementById('closeProductModal');
    const cancelProductBtn = document.getElementById('cancelProductBtn');
    const productForm = document.getElementById('productForm');

    addProductBtn.addEventListener('click', () => openProductModal());
    bulkDeleteBtn.addEventListener('click', () => handleBulkDelete());

    // Debounced search
    let searchTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            currentSearch = e.target.value;
            currentPage = 1;
            loadProducts();
        }, 500);
    });

    statusFilter.addEventListener('change', (e) => {
        currentStatus = e.target.value;
        currentPage = 1;
        loadProducts();
    });

    closeProductModal.addEventListener('click', () => closeModal(productModal));
    cancelProductBtn.addEventListener('click', () => closeModal(productModal));
    productForm.addEventListener('submit', (e) => {
        e.preventDefault();
        handleProductSubmit();
    });
}

async function loadProducts() {
    try {
        let url = `${API_BASE}/products?page=${currentPage}&per_page=50`;

        if (currentSearch) {
            url += `&search=${encodeURIComponent(currentSearch)}`;
        }

        if (currentStatus !== '') {
            url += `&is_active=${currentStatus}`;
        }

        const response = await fetch(url);
        const data = await response.json();

        renderProducts(data.products);
        renderPagination(data.page, data.total_pages);
    } catch (error) {
        showNotification('Error loading products: ' + error.message, 'error');
    }
}

function renderProducts(products) {
    const tbody = document.getElementById('productsTableBody');

    if (products.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" style="text-align: center; padding: 2rem; color: var(--text-muted);">
                    No products found.
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = products.map(product => `
        <tr>
            <td><strong>${escapeHtml(product.sku)}</strong></td>
            <td>${escapeHtml(product.name)}</td>
            <td>${escapeHtml(product.description || '-')}</td>
            <td>$${parseFloat(product.price).toFixed(2)}</td>
            <td>${product.quantity}</td>
            <td>
                <span class="badge ${product.is_active ? 'badge-success' : 'badge-danger'}">
                    ${product.is_active ? 'Active' : 'Inactive'}
                </span>
            </td>
            <td>
                <button class="btn btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.9rem;" 
                        onclick="editProduct(${product.id})">Edit</button>
                <button class="btn btn-danger" style="padding: 0.5rem 1rem; font-size: 0.9rem;" 
                        onclick="deleteProduct(${product.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function renderPagination(currentPage, totalPages) {
    const pagination = document.getElementById('pagination');

    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }

    let html = '';

    // Previous button
    if (currentPage > 1) {
        html += `<button class="page-btn" onclick="changePage(${currentPage - 1})">← Previous</button>`;
    }

    // Page numbers
    const maxVisible = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2));
    let endPage = Math.min(totalPages, startPage + maxVisible - 1);

    if (endPage - startPage < maxVisible - 1) {
        startPage = Math.max(1, endPage - maxVisible + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
        html += `<button class="page-btn ${i === currentPage ? 'active' : ''}" 
                        onclick="changePage(${i})">${i}</button>`;
    }

    // Next button
    if (currentPage < totalPages) {
        html += `<button class="page-btn" onclick="changePage(${currentPage + 1})">Next →</button>`;
    }

    pagination.innerHTML = html;
}

function changePage(page) {
    currentPage = page;
    loadProducts();
}

function openProductModal(product = null) {
    const modal = document.getElementById('productModal');
    const title = document.getElementById('productModalTitle');
    const form = document.getElementById('productForm');

    if (product) {
        title.textContent = 'Edit Product';
        document.getElementById('productSku').value = product.sku;
        document.getElementById('productSku').disabled = true;
        document.getElementById('productName').value = product.name;
        document.getElementById('productDescription').value = product.description || '';
        document.getElementById('productPrice').value = product.price;
        document.getElementById('productQuantity').value = product.quantity;
        document.getElementById('productActive').checked = product.is_active;
        editingProductId = product.id;
    } else {
        title.textContent = 'Add Product';
        form.reset();
        document.getElementById('productSku').disabled = false;
        editingProductId = null;
    }

    modal.classList.add('active');
}

function closeModal(modal) {
    modal.classList.remove('active');
}

async function handleProductSubmit() {
    const productData = {
        sku: document.getElementById('productSku').value,
        name: document.getElementById('productName').value,
        description: document.getElementById('productDescription').value,
        price: parseFloat(document.getElementById('productPrice').value),
        quantity: parseInt(document.getElementById('productQuantity').value),
        is_active: document.getElementById('productActive').checked
    };

    try {
        let response;
        if (editingProductId) {
            response = await fetch(`${API_BASE}/products/${editingProductId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(productData)
            });
        } else {
            response = await fetch(`${API_BASE}/products`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(productData)
            });
        }

        if (response.ok) {
            showNotification(editingProductId ? 'Product updated!' : 'Product created!', 'success');
            closeModal(document.getElementById('productModal'));
            loadProducts();
        } else {
            const error = await response.json();
            showNotification(error.detail || 'Error saving product', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    }
}

async function editProduct(id) {
    try {
        const response = await fetch(`${API_BASE}/products/${id}`);
        const product = await response.json();
        openProductModal(product);
    } catch (error) {
        showNotification('Error loading product: ' + error.message, 'error');
    }
}

// ===== CONFIRMATION MODAL =====
let confirmCallback = null;

function initializeConfirmation() {
    const modal = document.getElementById('confirmModal');
    const closeBtn = document.getElementById('closeConfirmModal');
    const cancelBtn = document.getElementById('cancelConfirmBtn');
    const confirmBtn = document.getElementById('confirmActionBtn');

    const closeModal = () => {
        modal.classList.remove('active');
        confirmCallback = null;
    };

    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);

    confirmBtn.addEventListener('click', () => {
        if (confirmCallback) {
            confirmCallback();
        }
        closeModal();
    });
}

function showConfirm(message, onConfirm) {
    const modal = document.getElementById('confirmModal');
    const messageEl = document.getElementById('confirmMessage');

    messageEl.textContent = message;
    confirmCallback = onConfirm;

    modal.classList.add('active');
}

// Update initialize function to include confirmation
document.addEventListener('DOMContentLoaded', () => {
    initializeUpload();
    initializeProducts();
    initializeWebhooks();
    initializeConfirmation(); // Add this
    loadProducts();
    loadWebhooks();
});

async function deleteProduct(id) {
    console.log('deleteProduct called for id:', id);
    showConfirm('Are you sure you want to delete this product?', async () => {
        console.log('Confirmed delete for id:', id);
        try {
            const response = await fetch(`${API_BASE}/products/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                showNotification('Product deleted!', 'success');
                loadProducts();
            } else {
                showNotification('Error deleting product', 'error');
            }
        } catch (error) {
            showNotification('Error: ' + error.message, 'error');
        }
    });
}

async function handleBulkDelete() {
    showConfirm('⚠️ Are you sure you want to delete ALL products? This action cannot be undone!', async () => {
        try {
            const response = await fetch(`${API_BASE}/products`, {
                method: 'DELETE'
            });

            const data = await response.json();

            if (response.ok) {
                showNotification(data.message, 'success');
                loadProducts();
            } else {
                showNotification('Error deleting products', 'error');
            }
        } catch (error) {
            showNotification('Error: ' + error.message, 'error');
        }
    });
}

// ===== WEBHOOK FUNCTIONALITY =====
function initializeWebhooks() {
    const addWebhookBtn = document.getElementById('addWebhookBtn');
    const webhookModal = document.getElementById('webhookModal');
    const closeWebhookModal = document.getElementById('closeWebhookModal');
    const cancelWebhookBtn = document.getElementById('cancelWebhookBtn');
    const webhookForm = document.getElementById('webhookForm');

    addWebhookBtn.addEventListener('click', () => openWebhookModal());
    closeWebhookModal.addEventListener('click', () => closeModal(webhookModal));
    cancelWebhookBtn.addEventListener('click', () => closeModal(webhookModal));
    webhookForm.addEventListener('submit', (e) => {
        e.preventDefault();
        handleWebhookSubmit();
    });
}

async function loadWebhooks() {
    try {
        const response = await fetch(`${API_BASE}/webhooks`);
        const data = await response.json();
        renderWebhooks(data.webhooks);
    } catch (error) {
        showNotification('Error loading webhooks: ' + error.message, 'error');
    }
}

function renderWebhooks(webhooks) {
    const tbody = document.getElementById('webhooksTableBody');

    if (webhooks.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; padding: 2rem; color: var(--text-muted);">
                    No webhooks configured.
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = webhooks.map(webhook => `
        <tr>
            <td style="max-width: 300px; overflow: hidden; text-overflow: ellipsis;">${escapeHtml(webhook.url)}</td>
            <td>${escapeHtml(webhook.event_type)}</td>
            <td>
                <span class="badge ${webhook.is_enabled ? 'badge-success' : 'badge-danger'}">
                    ${webhook.is_enabled ? 'Enabled' : 'Disabled'}
                </span>
            </td>
            <td>${webhook.last_triggered_at ? new Date(webhook.last_triggered_at).toLocaleString() : 'Never'}</td>
            <td>
                <button class="btn btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.9rem;" 
                        onclick="testWebhook(${webhook.id})">Test</button>
                <button class="btn btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.9rem;" 
                        onclick="editWebhook(${webhook.id})">Edit</button>
                <button class="btn btn-danger" style="padding: 0.5rem 1rem; font-size: 0.9rem;" 
                        onclick="deleteWebhook(${webhook.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function openWebhookModal(webhook = null) {
    const modal = document.getElementById('webhookModal');
    const title = document.getElementById('webhookModalTitle');
    const form = document.getElementById('webhookForm');

    if (webhook) {
        title.textContent = 'Edit Webhook';
        document.getElementById('webhookUrl').value = webhook.url;
        document.getElementById('webhookEventType').value = webhook.event_type;
        document.getElementById('webhookEnabled').checked = webhook.is_enabled;
        editingWebhookId = webhook.id;
    } else {
        title.textContent = 'Add Webhook';
        form.reset();
        editingWebhookId = null;
    }

    modal.classList.add('active');
}

async function handleWebhookSubmit() {
    const webhookData = {
        url: document.getElementById('webhookUrl').value,
        event_type: document.getElementById('webhookEventType').value,
        is_enabled: document.getElementById('webhookEnabled').checked
    };

    try {
        let response;
        if (editingWebhookId) {
            response = await fetch(`${API_BASE}/webhooks/${editingWebhookId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(webhookData)
            });
        } else {
            response = await fetch(`${API_BASE}/webhooks`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(webhookData)
            });
        }

        if (response.ok) {
            showNotification(editingWebhookId ? 'Webhook updated!' : 'Webhook created!', 'success');
            closeModal(document.getElementById('webhookModal'));
            loadWebhooks();
        } else {
            const error = await response.json();
            showNotification(error.detail || 'Error saving webhook', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    }
}

async function editWebhook(id) {
    try {
        const response = await fetch(`${API_BASE}/webhooks`);
        const data = await response.json();
        const webhook = data.webhooks.find(w => w.id === id);
        if (webhook) {
            openWebhookModal(webhook);
        }
    } catch (error) {
        showNotification('Error loading webhook: ' + error.message, 'error');
    }
}

async function deleteWebhook(id) {
    if (!confirm('Are you sure you want to delete this webhook?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/webhooks/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showNotification('Webhook deleted!', 'success');
            loadWebhooks();
        } else {
            showNotification('Error deleting webhook', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    }
}

async function testWebhook(id) {
    try {
        const response = await fetch(`${API_BASE}/webhooks/${id}/test`, {
            method: 'POST'
        });

        const data = await response.json();

        if (response.ok) {
            showNotification(`Webhook test successful! Status: ${data.status_code}`, 'success');
        } else {
            showNotification(data.detail || 'Webhook test failed', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    }
}

// ===== UTILITY FUNCTIONS =====
function showNotification(message, type = 'success') {
    const container = document.getElementById('notificationContainer');

    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    container.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Expose functions to global scope for inline onclick handlers
window.editProduct = editProduct;
window.deleteProduct = deleteProduct;
window.testWebhook = testWebhook;
window.editWebhook = editWebhook;
window.deleteWebhook = deleteWebhook;
window.changePage = changePage;

