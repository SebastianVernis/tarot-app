/**
 * Tarot Místico - Frontend con autenticación y persistencia
 */

// Configuración
const API_BASE_URL = 'http://localhost:5000/api';

// Estado global
let appState = {
    user: null,
    accessToken: null,
    refreshToken: null,
    theme: 'dark',
    selectedSpread: null,
    usage: null
};

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

async function initializeApp() {
    // Cargar tema guardado
    loadTheme();
    
    // Crear estrellas
    createStars();
    
    // Verificar sesión guardada
    await checkSavedSession();
    
    // Cargar tiradas
    loadSpreads();
}

// ============= TEMA =============

function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    appState.theme = savedTheme;
    applyTheme(savedTheme);
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    const icon = theme === 'dark' ? '🌙' : '☀️';
    const text = theme === 'dark' ? 'Oscuro' : 'Claro';
    
    document.getElementById('themeIcon').textContent = icon;
    document.getElementById('themeText').textContent = text;
    
    appState.theme = theme;
    localStorage.setItem('theme', theme);
}

async function toggleTheme() {
    const newTheme = appState.theme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
    
    // Si el usuario está autenticado, guardar en el backend
    if (appState.user) {
        try {
            await apiRequest('/user/theme', 'PUT', { theme: newTheme });
        } catch (error) {
            console.error('Error al guardar tema:', error);
        }
    }
}

// ============= AUTENTICACIÓN =============

async function checkSavedSession() {
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');
    
    if (accessToken && refreshToken) {
        appState.accessToken = accessToken;
        appState.refreshToken = refreshToken;
        
        try {
            // Verificar si el token es válido
            const response = await apiRequest('/auth/me', 'GET');
            if (response.user) {
                setUser(response.user);
                await loadUsage();
            }
        } catch (error) {
            // Token inválido, intentar refresh
            try {
                await refreshAccessToken();
            } catch (refreshError) {
                // Refresh falló, limpiar sesión
                clearSession();
            }
        }
    }
}

async function refreshAccessToken() {
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${appState.refreshToken}`
        }
    });
    
    if (!response.ok) throw new Error('Refresh failed');
    
    const data = await response.json();
    appState.accessToken = data.access_token;
    localStorage.setItem('accessToken', data.access_token);
    
    if (data.user) {
        setUser(data.user);
    }
}

function setUser(user) {
    appState.user = user;
    
    // Actualizar UI
    document.getElementById('authButtons').style.display = 'none';
    document.getElementById('userSection').style.display = 'flex';
    document.getElementById('username').textContent = user.username;
    document.getElementById('userAvatar').textContent = user.username[0].toUpperCase();
    
    if (user.is_premium) {
        document.getElementById('premiumBadge').style.display = 'inline-block';
    }
    
    // Aplicar tema del usuario
    if (user.theme) {
        applyTheme(user.theme);
    }
}

function clearSession() {
    appState.user = null;
    appState.accessToken = null;
    appState.refreshToken = null;
    appState.usage = null;
    
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    
    // Actualizar UI
    document.getElementById('authButtons').style.display = 'flex';
    document.getElementById('userSection').style.display = 'none';
}

async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await apiRequest('/auth/login', 'POST', { email, password });
        
        // Guardar tokens
        appState.accessToken = response.access_token;
        appState.refreshToken = response.refresh_token;
        localStorage.setItem('accessToken', response.access_token);
        localStorage.setItem('refreshToken', response.refresh_token);
        
        // Establecer usuario
        setUser(response.user);
        
        // Cargar uso
        await loadUsage();
        
        // Cerrar modal
        closeModal('loginModal');
        
        // Mostrar mensaje de éxito
        showNotification('¡Bienvenido de vuelta!', 'success');
        
    } catch (error) {
        showError('loginError', error.message || 'Error al iniciar sesión');
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    
    try {
        const response = await apiRequest('/auth/register', 'POST', {
            username,
            email,
            password,
            theme: appState.theme
        });
        
        // Guardar tokens
        appState.accessToken = response.access_token;
        appState.refreshToken = response.refresh_token;
        localStorage.setItem('accessToken', response.access_token);
        localStorage.setItem('refreshToken', response.refresh_token);
        
        // Establecer usuario
        setUser(response.user);
        
        // Cargar uso
        await loadUsage();
        
        // Cerrar modal
        closeModal('registerModal');
        
        // Mostrar mensaje de éxito
        showNotification('¡Cuenta creada exitosamente!', 'success');
        
    } catch (error) {
        showError('registerError', error.message || 'Error al registrarse');
    }
}

function logout() {
    clearSession();
    showNotification('Sesión cerrada', 'success');
    loadSpreads(); // Recargar tiradas para mostrar locks
}

// ============= API HELPERS =============

async function apiRequest(endpoint, method = 'GET', body = null) {
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (appState.accessToken) {
        headers['Authorization'] = `Bearer ${appState.accessToken}`;
    }
    
    const options = {
        method,
        headers
    };
    
    if (body) {
        options.body = JSON.stringify(body);
    }
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Error en la petición');
    }
    
    return await response.json();
}

// ============= USAGE & FREEMIUM =============

async function loadUsage() {
    if (!appState.user) return;
    
    try {
        const usage = await apiRequest('/user/usage', 'GET');
        appState.usage = usage;
        updateUsageIndicator(usage);
    } catch (error) {
        console.error('Error al cargar uso:', error);
    }
}

function updateUsageIndicator(usage) {
    const indicator = document.getElementById('usageIndicator');
    const text = document.getElementById('usageText');
    
    if (usage.is_premium) {
        text.textContent = '✨ Premium - Ilimitado';
        indicator.style.display = 'flex';
    } else {
        const remaining = usage.readings_remaining;
        const limit = usage.readings_limit;
        text.textContent = `📖 ${remaining}/${limit} lecturas hoy`;
        indicator.style.display = 'flex';
    }
}

async function checkReadingAccess(spreadType) {
    if (!appState.user) {
        showNotification('Debes iniciar sesión para realizar lecturas', 'error');
        showLogin();
        return false;
    }
    
    try {
        const response = await apiRequest('/readings/check-access', 'POST', {
            spread_type: spreadType
        });
        
        if (!response.can_access) {
            if (response.spread_access && !response.spread_access.allowed) {
                showUpgradeModal(response.spread_access.message);
                return false;
            }
            
            if (response.reading_limit && !response.reading_limit.allowed) {
                showUpgradeModal(response.reading_limit.message);
                return false;
            }
        }
        
        return true;
    } catch (error) {
        showNotification(error.message, 'error');
        return false;
    }
}

function showUpgradeModal(message) {
    if (confirm(`${message}\n\n¿Deseas actualizar a Premium ahora?`)) {
        upgradeToPremium();
    }
}

async function upgradeToPremium() {
    if (!appState.user) {
        showLogin();
        return;
    }
    
    try {
        // Usar endpoint de demo para desarrollo
        const response = await apiRequest('/subscription/demo-upgrade', 'POST');
        
        // Actualizar usuario
        appState.user = response.user;
        setUser(response.user);
        await loadUsage();
        
        showNotification('¡Actualizado a Premium! 🎉', 'success');
        loadSpreads(); // Recargar para quitar locks
        
    } catch (error) {
        showNotification(error.message || 'Error al actualizar', 'error');
    }
}

// ============= TIRADAS =============

const SPREADS = {
    una_carta: {
        name: 'Una Carta del Día',
        description: 'Guía y reflexión diaria',
        cards: 1,
        free: true
    },
    tres_cartas: {
        name: 'Pasado, Presente y Futuro',
        description: 'Visión temporal completa',
        cards: 3,
        free: true
    },
    cruz_celta: {
        name: 'Cruz Celta',
        description: 'Análisis profundo y detallado',
        cards: 10,
        free: false
    },
    herradura: {
        name: 'Herradura',
        description: 'Situación y consejo',
        cards: 7,
        free: false
    },
    relacion: {
        name: 'Lectura de Relación',
        description: 'Análisis de vínculos',
        cards: 6,
        free: false
    }
};

function loadSpreads() {
    const container = document.getElementById('tiradasContainer');
    container.innerHTML = '';
    
    const isPremium = appState.user && appState.user.is_premium;
    
    Object.entries(SPREADS).forEach(([key, spread]) => {
        const isLocked = !spread.free && !isPremium;
        
        const div = document.createElement('div');
        div.className = `tirada-option ${isLocked ? 'locked' : ''}`;
        div.dataset.tipo = key;
        
        div.innerHTML = `
            <h3>${spread.name} ${isLocked ? '<span class="lock-icon">🔒</span>' : ''}</h3>
            <p>${spread.description}</p>
            <p class="num-cartas">${spread.cards} carta${spread.cards > 1 ? 's' : ''}</p>
        `;
        
        if (!isLocked) {
            div.addEventListener('click', () => selectSpread(key));
        } else {
            div.addEventListener('click', () => {
                showUpgradeModal('Esta tirada requiere suscripción Premium');
            });
        }
        
        container.appendChild(div);
    });
}

function selectSpread(spreadType) {
    // Quitar selección previa
    document.querySelectorAll('.tirada-option').forEach(opt => {
        opt.classList.remove('selected');
    });
    
    // Agregar selección actual
    const selected = document.querySelector(`[data-tipo="${spreadType}"]`);
    if (selected) {
        selected.classList.add('selected');
        appState.selectedSpread = spreadType;
        document.getElementById('btnIniciarLectura').disabled = false;
    }
}

async function iniciarLectura() {
    if (!appState.selectedSpread) return;
    
    // Verificar acceso
    const canAccess = await checkReadingAccess(appState.selectedSpread);
    if (!canAccess) return;
    
    // Aquí iría la lógica de la lectura
    // Por ahora, solo crear un registro
    const question = document.getElementById('pregunta').value;
    
    try {
        // Simular cartas (en producción, usar el generador del backend)
        const cards = generateMockCards(SPREADS[appState.selectedSpread].cards);
        
        const response = await apiRequest('/readings/', 'POST', {
            spread_type: appState.selectedSpread,
            question: question,
            cards: cards,
            interpretation: 'Interpretación generada...'
        });
        
        // Actualizar uso
        await loadUsage();
        
        showNotification('¡Lectura creada exitosamente!', 'success');
        
        // Limpiar formulario
        document.getElementById('pregunta').value = '';
        appState.selectedSpread = null;
        document.querySelectorAll('.tirada-option').forEach(opt => {
            opt.classList.remove('selected');
        });
        document.getElementById('btnIniciarLectura').disabled = true;
        
    } catch (error) {
        showNotification(error.message || 'Error al crear lectura', 'error');
    }
}

function generateMockCards(count) {
    const cards = [];
    for (let i = 0; i < count; i++) {
        cards.push({
            name: `Carta ${i + 1}`,
            position: `Posición ${i + 1}`,
            reversed: Math.random() > 0.5
        });
    }
    return cards;
}

// ============= UI HELPERS =============

function createStars() {
    const starsContainer = document.getElementById('stars');
    const numStars = 100;
    
    for (let i = 0; i < numStars; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.width = Math.random() * 3 + 'px';
        star.style.height = star.style.width;
        star.style.animationDelay = Math.random() * 3 + 's';
        star.style.animationDuration = (Math.random() * 3 + 2) + 's';
        starsContainer.appendChild(star);
    }
}

function showLogin() {
    document.getElementById('loginModal').classList.add('active');
}

function showRegister() {
    document.getElementById('registerModal').classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
    // Limpiar errores
    const errorDiv = document.getElementById(modalId.replace('Modal', 'Error'));
    if (errorDiv) {
        errorDiv.style.display = 'none';
    }
}

function switchToRegister() {
    closeModal('loginModal');
    showRegister();
}

function switchToLogin() {
    closeModal('registerModal');
    showLogin();
}

function showError(elementId, message) {
    const errorDiv = document.getElementById(elementId);
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

function showNotification(message, type = 'info') {
    // Crear notificación temporal
    const notification = document.createElement('div');
    notification.className = type === 'success' ? 'success-message' : 'error-message';
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '100px';
    notification.style.right = '20px';
    notification.style.zIndex = '10000';
    notification.style.minWidth = '300px';
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function showUserMenu() {
    const menu = confirm('Opciones:\n\n1. Ver Perfil\n2. Actualizar a Premium\n3. Cerrar Sesión\n\nElige una opción (1-3)');
    
    if (menu) {
        // Implementar menú de usuario
        if (confirm('¿Cerrar sesión?')) {
            logout();
        }
    }
}
