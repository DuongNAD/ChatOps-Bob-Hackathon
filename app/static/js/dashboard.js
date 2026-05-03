// ChatOps-Bob Gateway — Dashboard JS

const API_BASE = '';

async function fetchHealth() {
    try {
        const res = await fetch(`${API_BASE}/health`);
        const data = await res.json();
        updateHealth(data);
    } catch (e) {
        console.error('Health check failed:', e);
    }
}

async function fetchConversations() {
    try {
        const res = await fetch(`${API_BASE}/api/v1/conversations?limit=20`);
        const data = await res.json();
        updateConversations(data);
    } catch (e) {
        console.error('Fetch conversations failed:', e);
        document.getElementById('conversations-list').innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">💬</div>
                <p>No conversations yet</p>
                <p style="font-size:0.75rem;margin-top:0.5rem">Send a message via Telegram to get started</p>
            </div>`;
    }
}

async function fetchStats() {
    try {
        const res = await fetch(`${API_BASE}/api/v1/stats`);
        const data = await res.json();
        updateStats(data);
    } catch (e) {
        console.error('Fetch stats failed:', e);
    }
}

function updateHealth(data) {
    // Status badge
    const badge = document.getElementById('status-badge');
    const dot = document.getElementById('pulse-dot');
    
    if (data.status === 'healthy') {
        badge.className = 'status-badge status-healthy';
        badge.innerHTML = `<span class="pulse-dot" id="pulse-dot"></span> Healthy`;
    } else {
        badge.className = 'status-badge status-mock';
        badge.innerHTML = `⚠️ Degraded`;
    }
    
    // AI mode badge
    const aiBadge = document.getElementById('ai-mode-badge');
    if (data.components?.ai_engine?.status === 'mock') {
        aiBadge.className = 'status-badge status-mock';
        aiBadge.textContent = '🧪 Mock AI';
    } else {
        aiBadge.className = 'status-badge status-healthy';
        aiBadge.textContent = '🧠 Live AI';
    }
    
    // Model name
    document.getElementById('model-name').textContent = data.components?.ai_engine?.model || 'N/A';
    
    // DB records
    const records = data.components?.database?.records || 0;
    document.getElementById('stat-messages').textContent = records;
}

function updateStats(data) {
    document.getElementById('stat-sessions').textContent = data.total_sessions || 0;
    document.getElementById('stat-messages').textContent = data.total_messages || 0;
    document.getElementById('stat-user-msgs').textContent = data.user_messages || 0;
    document.getElementById('stat-ai-msgs').textContent = data.ai_responses || 0;
}

function updateConversations(data) {
    const list = document.getElementById('conversations-list');
    
    if (!data.messages || data.messages.length === 0) {
        list.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">💬</div>
                <p>No conversations yet</p>
                <p style="font-size:0.75rem;margin-top:0.5rem">Send a message via Telegram to get started</p>
            </div>`;
        return;
    }
    
    list.innerHTML = data.messages.map(msg => {
        const roleClass = msg.role === 'user' ? 'role-user' : 'role-assistant';
        const roleLabel = msg.role === 'user' ? '👤 User' : '🤖 AI';
        const timeStr = msg.timestamp ? new Date(msg.timestamp).toLocaleString() : '';
        const content = escapeHtml(msg.content || '');
        const truncated = content.length > 150 ? content.substring(0, 150) + '…' : content;
        
        return `
            <div class="message-item ${roleClass}">
                <div class="message-meta">
                    <span class="message-role">${roleLabel}</span>
                    <span class="message-session">${msg.session_id || ''}</span>
                    <span class="message-time">${timeStr}</span>
                </div>
                <div class="message-content">${truncated}</div>
            </div>`;
    }).join('');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function refreshAll() {
    const btn = document.getElementById('btn-refresh');
    btn.innerHTML = '<span class="loading-spinner"></span> Loading...';
    btn.disabled = true;
    
    await Promise.all([fetchHealth(), fetchConversations(), fetchStats()]);
    
    btn.innerHTML = '🔄 Refresh';
    btn.disabled = false;
}

// Auto-refresh every 30 seconds
document.addEventListener('DOMContentLoaded', () => {
    refreshAll();
    setInterval(refreshAll, 30000);
});
