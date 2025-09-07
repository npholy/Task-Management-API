const API_BASE_URL = 'http://127.0.0.1:8000/api/';
let accessToken = localStorage.getItem('accessToken');

// --- SECTION TOGGLING ---
function showSection(sectionId) {
    document.querySelectorAll('#login-section, #signup-section, #dashboard').forEach(section => {
        section.classList.add('hidden');
    });
    document.getElementById(sectionId).classList.remove('hidden');
}

// --- AUTHENTICATION & INITIALIZATION ---
document.getElementById('login-btn').addEventListener('click', async () => {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('login-error');

    try {
        const response = await fetch(`${API_BASE_URL}token/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Invalid credentials');
        }
        const data = await response.json();
        accessToken = data.access;
        localStorage.setItem('accessToken', accessToken);
        showSection('dashboard');
        loadCategories();
        loadTasks();
    } catch (error) {
        errorElement.textContent = error.message;
        errorElement.classList.remove('hidden');
    }
});

document.getElementById('signup-btn').addEventListener('click', async () => {
    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const errorElement = document.getElementById('signup-error');

    try {
        const response = await fetch(`${API_BASE_URL}users/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        if (!response.ok) {
            const errorData = await response.json();
            let errorMessage = 'Error creating account';
            if (errorData.username) errorMessage = `Username: ${errorData.username.join(', ')}`;
            else if (errorData.email) errorMessage = `Email: ${errorData.email.join(', ')}`;
            else if (errorData.password) errorMessage = `Password: ${errorData.password.join(', ')}`;
            else if (typeof errorData === 'object' && !Array.isArray(errorData)) {
                errorMessage = Object.values(errorData).flat().join(', ');
            } else {
                errorMessage = JSON.stringify(errorData);
            }
            throw new Error(errorMessage);
        }

        showSection('login-section');
        errorElement.classList.add('hidden');
        document.getElementById('signup-username').value = '';
        document.getElementById('signup-email').value = '';
        document.getElementById('signup-password').value = '';
    } catch (error) {
        errorElement.textContent = error.message;
        errorElement.classList.remove('hidden');
    }
});

document.getElementById('show-signup').addEventListener('click', (e) => {
    e.preventDefault();
    showSection('signup-section');
    document.getElementById('login-error').classList.add('hidden');
});
document.getElementById('show-login').addEventListener('click', (e) => {
    e.preventDefault();
    showSection('login-section');
    document.getElementById('signup-error').classList.add('hidden');
});

document.getElementById('logout-btn').addEventListener('click', () => {
    localStorage.removeItem('accessToken');
    accessToken = null;
    showSection('login-section');
});

// --- CATEGORY MANAGEMENT ---
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}categories/`, {
            headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (!response.ok) throw new Error('Failed to load categories.');
        const categories = await response.json();
        
        const categorySelect = document.getElementById('task-category');
        const categoryList = document.getElementById('category-list');
        
        categorySelect.innerHTML = '<option value="">No Category</option>';
        categoryList.innerHTML = '';
        
        categories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.id;
            option.textContent = cat.name;
            categorySelect.appendChild(option);
            
            const li = document.createElement('li');
            li.className = 'flex justify-between items-center bg-gray-50 p-3 rounded-lg';
            li.innerHTML = `
                <span>${cat.name}</span>
                <button class="text-red-600 hover:text-red-800 transition" onclick="deleteCategory(${cat.id})">Delete</button>
            `;
            categoryList.appendChild(li);
        });
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

document.getElementById('create-category-btn').addEventListener('click', async () => {
    const name = document.getElementById('category-name').value;
    const errorElement = document.getElementById('category-error');

    if (!name) {
        errorElement.textContent = 'Category name cannot be empty.';
        errorElement.classList.remove('hidden');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}categories/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({ name })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.name || 'Error creating category.');
        }
        
        document.getElementById('category-name').value = '';
        errorElement.classList.add('hidden');
        loadCategories();
    } catch (error) {
        errorElement.textContent = error.message;
        errorElement.classList.remove('hidden');
    }
});

async function deleteCategory(id) {
    try {
        const response = await fetch(`${API_BASE_URL}categories/${id}/`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (!response.ok) throw new Error('Failed to delete category.');
        loadCategories();
    } catch (error) {
        console.error('Error deleting category:', error);
    }
}

// --- TASK MANAGEMENT ---
document.getElementById('create-task-btn').addEventListener('click', async () => {
    const task = {
        title: document.getElementById('task-title').value,
        description: document.getElementById('task-description').value,
        due_date: document.getElementById('task-due-date').value,
        priority: document.getElementById('task-priority').value,
        status: 'todo', 
        category_id: document.getElementById('task-category').value || null
    };
    const errorElement = document.getElementById('create-task-error');

    try {
        const response = await fetch(`${API_BASE_URL}tasks/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(task)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            let errorMessage = 'Error creating task.';
            if (errorData.title) errorMessage = `Title: ${errorData.title.join(', ')}`;
            else if (errorData.description) errorMessage = `Description: ${errorData.description.join(', ')}`;
            else if (errorData.due_date) errorMessage = `Due Date: ${errorData.due_date.join(', ')}`;
            else if (errorData.category) errorMessage = `Category: ${errorData.category.join(', ')}`;
            else if (errorData.status) errorMessage = `Status: ${errorData.status.join(', ')}`;
            else errorMessage = JSON.stringify(errorData);
            throw new Error(errorMessage);
        }
        
        document.getElementById('task-title').value = '';
        document.getElementById('task-description').value = '';
        document.getElementById('task-due-date').value = '';
        errorElement.classList.add('hidden');
        loadTasks();
    } catch (error) {
        errorElement.textContent = error.message;
        errorElement.classList.remove('hidden');
    }
});

async function loadTasks() {
    const statusFilter = document.getElementById('filter-status').value;
    const priorityFilter = document.getElementById('filter-priority').value;
    const sortBy = document.getElementById('sort-by').value;
    
    // Always fetch all tasks with sorting, but without status/priority filters
    const url = `${API_BASE_URL}tasks/?ordering=${sortBy}`;

    try {
        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (!response.ok) {
            if (response.status === 401) {
                console.error('Unauthorized: Your session has expired.');
                localStorage.removeItem('accessToken');
                showSection('login-section');
                return;
            }
            throw new Error('Failed to load tasks.');
        }
        
        const data = await response.json();
        // Correctly handle both paginated and non-paginated responses
        const tasks = data.results || data; 

        // Apply filters on the client side to avoid 400 errors
        const filteredTasks = tasks.filter(task => {
            const matchesStatus = 
                !statusFilter || 
                (statusFilter === 'pending' && (task.status === 'todo' || task.status === 'in_progress')) ||
                (statusFilter === 'completed' && task.status === 'done');
            
            const matchesPriority = !priorityFilter || task.priority === priorityFilter;
            
            return matchesStatus && matchesPriority;
        });

        const taskList = document.getElementById('task-list');
        taskList.innerHTML = '';
        
        filteredTasks.forEach(task => {
            const card = document.createElement('div');
            card.className = `task-card bg-white p-6 rounded-xl shadow-lg border-l-4 ${task.status === 'done' ? 'border-green-500' : 'border-red-500'}`;
            card.innerHTML = `
                <h3 class="text-xl font-bold mb-2">${task.title}</h3>
                <p class="text-gray-600 text-sm mb-2">${task.description || 'No description'}</p>
                <p class="text-sm text-gray-500 mb-1">
                    <strong>Due:</strong> ${task.due_date ? new Date(task.due_date).toLocaleString() : 'Not set'}
                </p>
                <p class="text-sm text-gray-500 mb-1">
                    <strong>Priority:</strong> <span class="capitalize">${task.priority}</span>
                </p>
                <p class="text-sm text-gray-500 mb-4">
                    <strong>Status:</strong> <span class="capitalize">${task.status}</span>
                </p>
                <div class="flex justify-end space-x-2">
                    <button class="bg-yellow-500 text-white px-4 py-2 rounded-full text-sm hover:bg-yellow-600 transition" onclick="toggleTaskStatus(${task.id})">
                        ${task.status === 'done' ? 'Mark Pending' : 'Mark Complete'}
                    </button>
                    <button class="bg-red-500 text-white px-4 py-2 rounded-full text-sm hover:bg-red-600 transition" onclick="deleteTask(${task.id})">Delete</button>
                </div>
            `;
            taskList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

async function toggleTaskStatus(id) {
    try {
        const response = await fetch(`${API_BASE_URL}tasks/${id}/toggle_status/`, {
            method: 'PATCH',
            headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (!response.ok) {
            if (response.status === 401) {
                console.error('Unauthorized: Your session has expired.');
                localStorage.removeItem('accessToken');
                showSection('login-section');
                return;
            }
            throw new Error('Failed to toggle task status.');
        }
        loadTasks();
    } catch (error) {
        console.error('Error toggling status:', error);
    }
}

async function deleteTask(id) {
    try {
        const response = await fetch(`${API_BASE_URL}tasks/${id}/`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (!response.ok) {
            if (response.status === 401) {
                console.error('Unauthorized: Your session has expired.');
                localStorage.removeItem('accessToken');
                showSection('login-section');
                return;
            }
            throw new Error('Failed to delete task.');
        }
        loadTasks();
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}

document.getElementById('apply-filter-btn').addEventListener('click', loadTasks);

if (accessToken) {
    showSection('dashboard');
    loadCategories();
    loadTasks();
} else {
    showSection('login-section');
}
