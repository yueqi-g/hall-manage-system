// 认证相关功能
document.addEventListener('DOMContentLoaded', function() {
    const authModal = document.getElementById('authModal');
    const closeBtn = document.querySelector('.close-btn');
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // 用户菜单交互
    userMenuBtn.addEventListener('click', function() {
        userDropdown.classList.toggle('show');
    });
    
    // 关闭下拉菜单当点击外部
    window.addEventListener('click', function(event) {
        if (!event.target.matches('.user-btn')) {
            if (userDropdown.classList.contains('show')) {
                userDropdown.classList.remove('show');
            }
        }
    });
    
    // 下拉菜单项点击事件
    document.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const authType = this.getAttribute('data-auth-type');
            
            // 打开模态框并切换到对应标签
            authModal.style.display = 'flex';
            
            // 移除所有活动状态
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // 根据类型激活对应标签
            if (authType === 'user') {
                document.querySelector('[data-tab="user-login"]').classList.add('active');
                document.getElementById('user-login').classList.add('active');
            } else if (authType === 'merchant') {
                document.querySelector('[data-tab="merchant-login"]').classList.add('active');
                document.getElementById('merchant-login').classList.add('active');
            } else if (authType === 'register') {
                document.querySelector('[data-tab="register"]').classList.add('active');
                document.getElementById('register').classList.add('active');
            }
        });
    });
    
    // 关闭登录模态框
    closeBtn.addEventListener('click', function() {
        authModal.style.display = 'none';
    });
    
    // 点击模态框外部关闭
    window.addEventListener('click', function(event) {
        if (event.target === authModal) {
            authModal.style.display = 'none';
        }
    });
    
    // 标签切换
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // 移除所有活动状态
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // 添加当前活动状态
            this.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // 用户登录表单提交
    document.getElementById('userLoginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        handleLogin('user');
    });
    
    // 商家登录表单提交
    document.getElementById('merchantLoginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        handleLogin('merchant');
    });
    
    // 注册表单提交
    document.getElementById('registerForm').addEventListener('submit', function(e) {
        e.preventDefault();
        handleRegister();
    });
    
    // 生成验证码
    generateCaptcha();
});

// 处理登录
async function handleLogin(userType) {
    const username = userType === 'user' 
        ? document.getElementById('username').value 
        : document.getElementById('merchant-username').value;
    const password = userType === 'user' 
        ? document.getElementById('password').value 
        : document.getElementById('merchant-password').value;
    const captcha = userType === 'user' 
        ? document.getElementById('captcha').value 
        : document.getElementById('merchant-captcha').value;
    
    try {
        // 调用后端API
        const response = await fetch('/api/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'login',
                username,
                password,
                userType
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 存储用户信息
            localStorage.setItem('currentUser', JSON.stringify({
                id: data.user.id,
                username: data.user.username,
                type: userType,
                token: data.token
            }));
            
            // 关闭模态框
            document.getElementById('authModal').style.display = 'none';
            
            // 更新UI显示登录状态
            updateUIAfterLogin(data.user.username, userType);
            
            // 根据用户类型重定向
            if (userType === 'user') {
                window.location.href = 'user_dashboard.html';
            } else {
                window.location.href = 'merchant_dashboard.html';
            }
        } else {
            alert('登录失败: ' + data.message);
        }
    } catch (error) {
        console.error('登录错误:', error);
        alert('网络错误，请稍后重试');
    }
}

// 处理注册
async function handleRegister() {
    const userType = document.getElementById('register-type').value;
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;
    const email = document.getElementById('register-email').value;
    
    if (password !== confirmPassword) {
        alert('两次输入的密码不一致');
        return;
    }
    
    try {
        // 调用后端API
        const response = await fetch('/api/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'register',
                username,
                password,
                email,
                userType
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('注册成功，请登录');
            // 切换到登录标签
            document.querySelector('[data-tab="user-login"]').click();
        } else {
            alert('注册失败: ' + data.message);
        }
    } catch (error) {
        console.error('注册错误:', error);
        alert('网络错误，请稍后重试');
    }
}

// 生成验证码
function generateCaptcha() {
    const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    let captcha = '';
    for (let i = 0; i < 6; i++) {
        captcha += chars[Math.floor(Math.random() * chars.length)];
    }
    
    document.getElementById('captchaCode').textContent = captcha;
    document.getElementById('merchantCaptchaCode').textContent = captcha;
}

// 更新登录后的UI
function updateUIAfterLogin(username, userType) {
    const userBtn = document.querySelector('.user-btn');
    userBtn.innerHTML = `
        <i class="fas fa-user"></i>
        <span>${username} (${userType === 'user' ? '用户' : '商家'})</span>
    `;
    
    // 更新下拉菜单
    const userDropdown = document.getElementById('userDropdown');
    userDropdown.innerHTML = `
        <a href="#" class="dropdown-item" id="profileLink">个人主页</a>
        <a href="#" class="dropdown-item" id="logoutLink">退出登录</a>
    `;
    
    // 添加退出登录事件
    document.getElementById('logoutLink').addEventListener('click', function(e) {
        e.preventDefault();
        handleLogout();
    });
}

// 处理退出登录
function handleLogout() {
    localStorage.removeItem('currentUser');
    window.location.reload();
}

// 检查登录状态
function checkLoginStatus() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (currentUser) {
        updateUIAfterLogin(currentUser.username, currentUser.type);
    }
}

// 页面加载时检查登录状态
window.addEventListener('load', checkLoginStatus);

// 处理登录
async function handleLogin(userType) {
    const username = userType === 'user' 
        ? document.getElementById('username').value 
        : document.getElementById('merchant-username').value;
    const password = userType === 'user' 
        ? document.getElementById('password').value 
        : document.getElementById('merchant-password').value;
    
    // 显示加载状态
    const submitBtn = userType === 'user' 
        ? document.querySelector('#userLoginForm .auth-btn')
        : document.querySelector('#merchantLoginForm .auth-btn');
    
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;

    try {
        // 模拟网络延迟
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 模拟API调用
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                password,
                userType
            })
        });
        
        // 模拟网络错误测试
        if (Math.random() < 0.3) { // 30%概率模拟网络错误
            throw new Error('网络连接失败');
        }
        
        const data = await response.json();
        
        if (data.success) {
            // 登录成功逻辑...
            showSuccessMessage('登录成功！');
        } else {
            showErrorMessage('登录失败: ' + data.message);
        }
    } catch (error) {
        console.error('登录错误:', error);
        if (error.message.includes('网络')) {
            showNetworkError();
        } else {
            showErrorMessage('网络错误，请稍后重试');
        }
    } finally {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
}

// 显示网络错误提示
function showNetworkError() {
    const networkErrorModal = document.createElement('div');
    networkErrorModal.className = 'network-error-modal';
    networkErrorModal.innerHTML = `
        <div class="network-error-content">
            <div class="network-error-header">
                <h3>网络连接问题</h3>
            </div>
            <div class="network-error-body">
                <i class="fas fa-wifi"></i>
                <p>网络错误，请检查网络连接后重试</p>
            </div>
            <div class="network-error-footer">
                <button class="btn btn-primary" onclick="this.closest('.network-error-modal').remove()">确定</button>
                <button class="btn btn-secondary" onclick="window.location.reload()">刷新页面</button>
            </div>
        </div>
    `;
    document.body.appendChild(networkErrorModal);
}

// 显示成功消息
function showSuccessMessage(message) {
    const toast = document.createElement('div');
    toast.className = 'toast toast-success';
    toast.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.remove(), 3000);
}

// 显示错误消息
function showErrorMessage(message) {
    const toast = document.createElement('div');
    toast.className = 'toast toast-error';
    toast.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        <span>${message}</span>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.remove(), 3000);
}

// 在文件末尾添加以下修复代码
// 修复注册功能
async function handleRegister() {
    const userType = document.getElementById('register-type').value;
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;
    const email = document.getElementById('register-email').value;
    
    if (password !== confirmPassword) {
        showErrorMessage('两次输入的密码不一致');
        return;
    }
    
    try {
        // 显示加载状态
        const submitBtn = document.querySelector('#registerForm .auth-btn');
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;

        // 模拟API调用 - 实际应该使用真实API
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 模拟成功响应
        const mockResponse = {
            success: true,
            user: {
                id: Date.now(),
                username: username,
                type: userType,
                email: email
            }
        };
        
        if (mockResponse.success) {
            showSuccessMessage('注册成功，请登录');
            // 存储用户信息到localStorage
            localStorage.setItem('currentUser', JSON.stringify(mockResponse.user));
            // 关闭模态框
            document.getElementById('authModal').style.display = 'none';
            // 更新UI
            updateUIAfterLogin(username, userType);
        }
    } catch (error) {
        console.error('注册错误:', error);
        showErrorMessage('注册失败，请稍后重试');
    }
}

// 修复登录功能
async function handleLogin(userType) {
    const username = userType === 'user' 
        ? document.getElementById('username').value 
        : document.getElementById('merchant-username').value;
    const password = userType === 'user' 
        ? document.getElementById('password').value 
        : document.getElementById('merchant-password').value;
    
    try {
        // 显示加载状态
        const submitBtn = userType === 'user' 
            ? document.querySelector('#userLoginForm .auth-btn')
            : document.querySelector('#merchantLoginForm .auth-btn');
        
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;

        // 模拟API调用 - 实际应该使用真实API
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 模拟成功响应
        const mockResponse = {
            success: true,
            user: {
                id: Date.now(),
                username: username,
                type: userType
            },
            token: 'mock-token-' + Date.now()
        };
        
        if (mockResponse.success) {
            // 存储用户信息
            localStorage.setItem('currentUser', JSON.stringify({
                id: mockResponse.user.id,
                username: mockResponse.user.username,
                type: mockResponse.user.type,
                token: mockResponse.token
            }));
            
            // 关闭模态框
            document.getElementById('authModal').style.display = 'none';
            
            // 更新UI显示登录状态
            updateUIAfterLogin(mockResponse.user.username, userType);
            
            // 根据用户类型重定向
            if (userType === 'user') {
                window.location.href = 'user_dashboard.html';
            } else {
                window.location.href = 'merchant_dashboard.html';
            }
        }
    } catch (error) {
        console.error('登录错误:', error);
        showErrorMessage('登录失败，请稍后重试');
    }
}

// 确保页面加载时检查登录状态
document.addEventListener('DOMContentLoaded', function() {
    checkLoginStatus();
    
    // 添加注册表单提交事件
    document.getElementById('registerForm').addEventListener('submit', function(e) {
        e.preventDefault();
        handleRegister();
    });
    
    // 添加登录表单提交事件
    document.getElementById('userLoginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        handleLogin('user');
    });
    
    document.getElementById('merchantLoginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        handleLogin('merchant');
    });
});

// 在文件末尾添加退出登录函数
function logout() {
    // 清除本地存储的用户信息
    localStorage.removeItem('currentUser');
    localStorage.removeItem('userToken');
    
    // 跳转到首页
    window.location.href = 'index.html';
}

// 更新检查登录状态的函数
function checkLoginStatus() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const authBtn = document.getElementById('authBtn');
    
    if (currentUser) {
        // 用户已登录，显示用户名和退出按钮
        authBtn.innerHTML = `
            <span>欢迎，${currentUser.username}</span>
            <button onclick="logout()" class="logout-btn" style="margin-left: 10px; background: #e74c3c; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">
                退出
            </button>
        `;
    } else {
        // 用户未登录，显示登录/注册按钮
        authBtn.innerHTML = '<i class="fas fa-user"></i> 登录/注册';
        authBtn.onclick = showAuthModal;
    }
}

// 更新登录后的UI显示函数
function updateUIAfterLogin(username, userType) {
    const authBtn = document.getElementById('authBtn');
    if (authBtn) {
        authBtn.innerHTML = `
            <span>欢迎，${username}</span>
            <button onclick="logout()" class="logout-btn" style="margin-left: 10px; background: #e74c3c; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">
                退出
            </button>
        `;
    }
}