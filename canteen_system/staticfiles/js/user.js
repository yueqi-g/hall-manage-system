// main.js - 主页面功能实现

document.addEventListener('DOMContentLoaded', function() {
    // 初始化热门推荐
    loadPopularDishes();
    
    // 初始化AI助手
    initAIAssistant();
    
    // 初始化导航栏用户菜单 - 先检查登录状态
    updateUserMenuState();
});

// 初始化筛选功能
function initFilterPanel() {
    // 口味标签选择
    const flavorTags = document.querySelectorAll('.flavor-tag');
    flavorTags.forEach(tag => {
        tag.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    });
    
    // 价格范围滑块
    const priceMin = document.getElementById('price-range-min');
    const priceMax = document.getElementById('price-range-max');
    const priceMinInput = document.getElementById('price-min');
    const priceMaxInput = document.getElementById('price-max');
    const priceDisplay = document.querySelector('.price-display');
    
    function updatePriceDisplay() {
        const min = priceMin.value;
        const max = priceMax.value;
        priceDisplay.textContent = `¥${min} - ¥${max}`;
        priceMinInput.value = min;
        priceMaxInput.value = max;
    }
    
    priceMin.addEventListener('input', updatePriceDisplay);
    priceMax.addEventListener('input', updatePriceDisplay);
    
    // 输入框同步
    priceMinInput.addEventListener('input', function() {
        priceMin.value = this.value;
        updatePriceDisplay();
    });
    
    priceMaxInput.addEventListener('input', function() {
        priceMax.value = this.value;
        updatePriceDisplay();
    });
    
    // 应用筛选
    document.querySelector('.btn-filter-apply').addEventListener('click', applyFilters);
    
    // 重置筛选
    document.querySelector('.btn-filter-reset').addEventListener('click', resetFilters);
}

// 应用筛选函数
function applyFilters() {
    const filters = {
        category: document.getElementById('category').value,
        flavors: Array.from(document.querySelectorAll('.flavor-tag.active')).map(tag => tag.dataset.value),
        priceMin: document.getElementById('price-min').value,
        priceMax: document.getElementById('price-max').value,
        crowd: document.querySelector('input[name="crowd"]:checked').value
    };
    
    console.log('应用筛选条件:', filters);
    // 这里可以调用实际的筛选API或函数
    filterDishes(filters);
}

// 重置筛选
function resetFilters() {
    // 重置表单
    document.getElementById('category').value = '';
    document.querySelectorAll('.flavor-tag').forEach(tag => tag.classList.remove('active'));
    document.getElementById('price-min').value = '0';
    document.getElementById('price-max').value = '50';
    document.getElementById('price-range-min').value = '0';
    document.getElementById('price-range-max').value = '50';
    document.getElementById('crowd-any').checked = true;
    updatePriceDisplay();
}

// 筛选菜品函数（需要根据实际数据结构实现）
function filterDishes(filters) {
    // 这里实现具体的筛选逻辑
    alert(`正在根据条件筛选：\n品类：${filters.category || '不限'}\n口味：${filters.flavors.join(', ') || '不限'}\n价格：${filters.priceMin}-${filters.priceMax}元\n人流量：${filters.crowd}`);
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    initFilterPanel();
});

// 加载热门推荐菜品
function loadPopularDishes() {
    // 模拟API调用获取热门菜品
    const popularDishes = [
        {
            id: 1,
            name: "麻辣香锅",
            price: 28,
            rating: 4.8,
            description: "香辣可口，配料丰富，多种食材任你选择",
            canteen: "第一食堂",
            waitTime: "15-20分钟",
            tags: ["辣", "实惠", "推荐"]
        },
        {
            id: 2,
            name: "番茄牛肉面",
            price: 22,
            rating: 4.6,
            description: "新鲜番茄熬制汤底，牛肉鲜嫩多汁",
            canteen: "第二食堂",
            waitTime: "10-15分钟",
            tags: ["不辣", "面食"]
        },
        {
            id: 3,
            name: "黄焖鸡米饭",
            price: 25,
            rating: 4.7,
            description: "鸡肉鲜嫩，汤汁浓郁，配米饭绝佳",
            canteen: "第三食堂",
            waitTime: "12-18分钟",
            tags: ["微辣", "米饭", "热门"]
        },
        {
            id: 4,
            name: "扬州炒饭",
            price: 18,
            rating: 4.5,
            description: "粒粒分明，配料丰富，传统经典",
            canteen: "第四食堂",
            waitTime: "8-12分钟",
            tags: ["不辣", "实惠", "推荐"]
        }
    ];
    
    const dishesGrid = document.querySelector('.dishes-grid');
    if (!dishesGrid) return;
    
    dishesGrid.innerHTML = '';
    
    popularDishes.forEach(dish => {
        const dishCard = createDishCard(dish);
        dishesGrid.appendChild(dishCard);
    });
}

// 创建菜品卡片
function createDishCard(dish) {
    const card = document.createElement('div');
    card.className = 'dish-card';
    card.dataset.id = dish.id;
    
    // 构建标签HTML
    const tagsHTML = dish.tags.map(tag => {
        let className = 'dish-tag';
        if (tag === '辣' || tag === '麻辣' || tag === '酸辣') className += ' spicy';
        if (tag === '实惠' || tag === '便宜') className += ' cheap';
        return `<span class="${className}">${tag}</span>`;
    }).join('');
    
    card.innerHTML = `
        <div class="dish-image">
            <div class="dish-rating">
                <i class="fas fa-star"></i> ${dish.rating}
            </div>
        </div>
        <div class="dish-info">
            <div class="dish-header">
                <h3 class="dish-name">${dish.name}</h3>
                <div class="dish-price">¥${dish.price}</div>
            </div>
            <p class="dish-description">${dish.description}</p>
            <div class="dish-meta">
                <span class="dish-canteen">${dish.canteen}</span>
                <span class="dish-wait-time">
                    <i class="fas fa-clock"></i> ${dish.waitTime}
                </span>
            </div>
            <div class="dish-tags">
                ${tagsHTML}
            </div>
            <div class="dish-actions">
                <button class="dish-btn primary" onclick="orderDish(${dish.id})">
                    <i class="fas fa-utensils"></i> 立即下单
                </button>
                <button class="dish-btn secondary" onclick="addToFavorites(${dish.id})">
                    <i class="fas fa-heart"></i> 收藏
                </button>
            </div>
        </div>
    `;
    
    // 设置菜品图片背景色
    const dishImage = card.querySelector('.dish-image');
    const colors = ['#ff9a9e', '#fad0c4', '#a1c4fd', '#ffecd2'];
    const randomColor = colors[dish.id % colors.length];
    dishImage.style.background = `linear-gradient(45deg, ${randomColor}, #fbc2eb)`;
    
    // 添加菜品图标
    const foodIcons = ['fa-utensils', 'fa-bowl-food', 'fa-burger', 'fa-pizza-slice'];
    const randomIcon = foodIcons[dish.id % foodIcons.length];
    dishImage.innerHTML = `<i class="fas ${randomIcon}"></i>` + dishImage.innerHTML;
    
    return card;
}

// 初始化AI助手
function initAIAssistant() {
    const chatMessages = document.getElementById('chatMessages');
    const foodInput = document.getElementById('foodInput');
    const sendButton = document.getElementById('sendMessage');
    
    if (!chatMessages || !foodInput || !sendButton) return;
    
    // 发送消息事件
    sendButton.addEventListener('click', handleAIMessage);
    foodInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleAIMessage();
    });
    
    // 示例问题点击事件
    const exampleTexts = document.querySelectorAll('.example-text');
    exampleTexts.forEach(example => {
        example.addEventListener('click', () => {
            foodInput.value = example.textContent;
            handleAIMessage();
        });
    });
}

// 处理AI消息
function handleAIMessage() {
    const foodInput = document.getElementById('foodInput');
    const chatMessages = document.getElementById('chatMessages');
    
    if (!foodInput.value.trim()) return;
    
    // 添加用户消息
    addMessage(foodInput.value, 'user');
    
    // 模拟AI响应
    setTimeout(() => {
        const aiResponse = generateAIResponse(foodInput.value);
        addMessage(aiResponse, 'ai');
        
        // 滚动到底部
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 1000);
    
    // 清空输入框
    foodInput.value = '';
}

// 添加消息到聊天框
function addMessage(text, type) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    if (type === 'user') {
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${text}</p>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${text}</p>
            </div>
        `;
    }
    
    chatMessages.appendChild(messageDiv);
    
    // 滚动到底部
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 生成AI响应（模拟）
function generateAIResponse(userInput) {
    const responses = [
        `根据您的需求"${userInput}"，我为您推荐以下菜品：麻辣香锅(第一食堂)、重庆小面(第二食堂)。这些菜品符合您的口味偏好且价格合理。`,
        `感谢您的查询！基于"${userInput}"，我建议尝试：番茄牛肉面(第二食堂)、清蒸鲈鱼(第三食堂)。这些菜品评分高，等待时间短。`,
        `明白了！针对"${userInput}"的要求，这些是不错的选择：黄焖鸡米饭(第三食堂)、扬州炒饭(第一食堂)。它们都备受学生欢迎，性价比高。`
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
}

// 初始化认证模态框
function initAuthModal() {
    const modal = document.getElementById('authModal');
    const userMenuBtn = document.getElementById('userMenuBtn');
    const closeBtn = document.querySelector('.close-btn');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const authTypeLinks = document.querySelectorAll('[data-auth-type]');
    
    if (!modal) return;
    
    // 打开模态框
    userMenuBtn?.addEventListener('click', (e) => {
        e.preventDefault();
        modal.style.display = 'block';
    });
    
    // 关闭模态框
    closeBtn?.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    // 点击外部关闭
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // 标签切换
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.tab;
            
            // 更新激活的标签
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // 显示对应的内容
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // 认证类型链接
    authTypeLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const authType = link.dataset.authType;
            
            // 切换到对应的标签
            const targetTab = authType === 'user' ? 'user-login' : 
                             authType === 'merchant' ? 'merchant-login' : 'register';
            
            document.querySelectorAll('.tab-btn').forEach(btn => {
                if (btn.dataset.tab === targetTab) {
                    btn.click();
                }
            });
        });
    });
    
    // 表单提交处理
    const forms = document.querySelectorAll('.auth-form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            handleAuthFormSubmit(form.id);
        });
    });
}

// 处理认证表单提交
function handleAuthFormSubmit(formId) {
    // 实际应用中应调用API进行认证
    alert(`表单 ${formId} 提交成功！`);
    document.getElementById('authModal').style.display = 'none';
}

// 更新用户菜单状态
function updateUserMenuState() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const userMenuBtn = document.getElementById('userMenuBtn');
    const authLinks = document.querySelector('.auth-links');
    
    if (currentUser) {
        // 用户已登录，显示用户名和下拉菜单
        userMenuBtn.innerHTML = `
            <i class="fas fa-user-circle"></i>
            <span>${currentUser.username}</span>
            <i class="fas fa-chevron-down"></i>
        `;
        userMenuBtn.style.display = 'flex';
        if (authLinks) authLinks.style.display = 'none';
        
        // 重新初始化用户菜单
        initUserMenu();
    } else {
        // 用户未登录，显示登录注册链接
        if (authLinks) authLinks.style.display = 'flex';
        userMenuBtn.style.display = 'none';
    }
}

// 初始化用户菜单（修改后的版本）
function initUserMenu() {
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');
    
    if (!userMenuBtn || !userDropdown) return;
    
    // 清空并重新构建下拉菜单内容
    userDropdown.innerHTML = `
        <div class="dropdown-item" onclick="showFavorites()">
            <i class="fas fa-heart"></i> 我的收藏
        </div>
        <div class="dropdown-item" onclick="showOrders()">
            <i class="fas fa-receipt"></i> 我的订单
        </div>
        <div class="dropdown-divider"></div>
        <div class="dropdown-item" onclick="logout()">
            <i class="fas fa-sign-out-alt"></i> 退出登录
        </div>
    `;
    
    userMenuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userDropdown.style.display = userDropdown.style.display === 'block' ? 'none' : 'block';
    });
    
    // 点击其他地方关闭下拉菜单
    document.addEventListener('click', () => {
        userDropdown.style.display = 'none';
    });
    
    userDropdown.addEventListener('click', (e) => {
        e.stopPropagation();
    });
}

// 处理认证表单提交（修改版）
function handleAuthFormSubmit(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    
    // 模拟登录成功
    if (formId.includes('login')) {
        const username = formData.get('username') || 'testuser';
        const userData = {
            id: 1,
            username: username,
            email: 'user@example.com',
            loginTime: new Date().toISOString()
        };
        
        localStorage.setItem('currentUser', JSON.stringify(userData));
        document.getElementById('authModal').style.display = 'none';
        
        // 更新用户菜单状态
        updateUserMenuState();
        
        alert(`欢迎回来，${username}！`);
    } else {
        // 注册逻辑
        alert('注册成功！请登录。');
        // 切换到登录标签
        document.querySelector('[data-tab="user-login"]').click();
    }
}

// 显示收藏页面
function showFavorites() {
    alert('显示我的收藏页面');
    // 实际应用中应该跳转到收藏页面或显示收藏模态框
}

// 显示订单页面
function showOrders() {
    alert('显示我的订单页面');
    // 实际应用中应该跳转到订单页面或显示订单模态框
}

// 退出登录（修改版）
function logout() {
    localStorage.removeItem('currentUser');
    updateUserMenuState();
    alert('已退出登录');
    
    // 跳转回主页
    window.location.href = 'index.html';
}

// 下单功能（修改版，保持原功能）
function orderDish(dishId) {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) {
        document.getElementById('authModal').style.display = 'block';
        return;
    }
    alert(`菜品ID: ${dishId} 下单成功！`);
}

// 添加到收藏（修改版，保持原功能）
function addToFavorites(dishId) {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) {
        document.getElementById('authModal').style.display = 'block';
        return;
    }
    alert(`已收藏菜品ID: ${dishId}`);
}