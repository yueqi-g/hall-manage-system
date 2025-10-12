// 商家功能
document.addEventListener('DOMContentLoaded', function() {
    // 检查登录状态
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser || currentUser.type !== 'merchant') {
        window.location.href = 'index.html';
        return;
    }
    
    // 添加退出登录按钮事件
    document.getElementById('logoutBtn').addEventListener('click', function() {
        if (confirm('确定要退出登录吗？')) {
            // 清除本地存储
            localStorage.removeItem('currentUser');
            localStorage.removeItem('userToken');
            
            // 跳转到首页
            window.location.href = 'index.html';
        }
    });
    
    // 加载商家菜品
    loadMerchantDishes();
    
    // 加载客流量数据
    loadTrafficData();
    
    // 菜品表单提交
    document.getElementById('dishForm').addEventListener('submit', function(e) {
        e.preventDefault();
        addDish();
    });
    
    // 客流量表单提交
    document.getElementById('trafficForm').addEventListener('submit', function(e) {
        e.preventDefault();
        updateTraffic();
    });
    
    // 添加编辑和删除事件监听
    addDishEvents();
});

// 加载商家菜品
async function loadMerchantDishes() {
    try {
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        const response = await fetch('/api/merchant/dishes/', {
            headers: {
                'Authorization': `Bearer ${currentUser.token}`
            }
        });
        
        const dishes = await response.json();
        const dishesContainer = document.getElementById('dishesContainer');
        dishesContainer.innerHTML = '';
        
        if (dishes.length === 0) {
            dishesContainer.innerHTML = `
                <div class="empty-state" style="text-align: center; padding: 40px; color: #7f8c8d;">
                    <i class="fas fa-utensils" style="font-size: 3rem; margin-bottom: 15px;"></i>
                    <p>暂无菜品，请添加您的第一个菜品</p>
                </div>
            `;
            return;
        }
        
        dishes.forEach(dish => {
            const dishElement = document.createElement('div');
            dishElement.className = 'dish-item';
            dishElement.innerHTML = `
                <div class="dish-info">
                    <h3>${dish.name}</h3>
                    <p>${dish.description || '暂无描述'}</p>
                    <div class="dish-meta">
                        <span>${getCategoryText(dish.category)}</span>
                        <span>${getTasteText(dish.taste)}</span>
                        <span class="dish-price">¥${dish.price}</span>
                    </div>
                </div>
                <div class="dish-actions">
                    <button class="btn btn-secondary edit-dish" data-id="${dish.id}">
                        <i class="fas fa-edit"></i> 编辑
                    </button>
                    <button class="btn btn-danger delete-dish" data-id="${dish.id}">
                        <i class="fas fa-trash"></i> 删除
                    </button>
                </div>
            `;
            
            dishesContainer.appendChild(dishElement);
        });
        
        // 添加编辑和删除事件
        addDishEvents();
    } catch (error) {
        console.error('加载菜品失败:', error);
        showNotification('加载菜品失败，请刷新重试', 'error');
    }
}

// 添加菜品
async function addDish() {
    const name = document.getElementById('dishName').value;
    const price = document.getElementById('dishPrice').value;
    const category = document.getElementById('dishCategory').value;
    const taste = document.getElementById('dishTaste').value;
    const description = document.getElementById('dishDescription').value;
    
    const submitBtn = document.querySelector('#dishForm button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    try {
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        const response = await fetch('/api/merchant/dishes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentUser.token}`
            },
            body: JSON.stringify({
                name,
                price: parseFloat(price),
                category,
                taste,
                description
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 显示成功状态
            submitBtn.innerHTML = '<i class="fas fa-check"></i> 添加成功';
            submitBtn.style.background = 'linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)';
            
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.style.background = '';
                document.getElementById('dishForm').reset();
                loadMerchantDishes();
            }, 1500);
        } else {
            alert('菜品添加失败: ' + result.message);
        }
    } catch (error) {
        console.error('添加菜品错误:', error);
        showNotification('网络错误，请稍后重试', 'error');
    }
}

// 更新客流量
async function updateTraffic() {
    const trafficCount = document.getElementById('trafficCount').value;
    const waitingTime = document.getElementById('waitingTime').value;
    
    const submitBtn = document.querySelector('#trafficForm button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    try {
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        const response = await fetch('/api/merchant/traffic/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentUser.token}`
            },
            body: JSON.stringify({
                count: parseInt(trafficCount),
                waitTime: parseFloat(waitingTime)
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 显示成功状态
            submitBtn.innerHTML = '<i class="fas fa-check"></i> 更新成功';
            submitBtn.style.background = 'linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)';
            
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.style.background = '';
                document.getElementById('trafficForm').reset();
                loadTrafficData();
            }, 1500);
        } else {
            alert('客流量更新失败: ' + result.message);
        }
    } catch (error) {
        console.error('更新客流量错误:', error);
        showNotification('网络错误，请稍后重试', 'error');
    }
}

// 加载客流量数据
async function loadTrafficData() {
    try {
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        const response = await fetch('/api/merchant/traffic/', {
            headers: {
                'Authorization': `Bearer ${currentUser.token}`
            }
        });
        
        const data = await response.json();
        
        document.getElementById('currentTraffic').textContent = data.currentCount || 0;
        document.getElementById('avgWaitTime').textContent = data.avgWaitTime || 0;
        document.getElementById('lastUpdate').textContent = data.lastUpdate || '--:--';
    } catch (error) {
        console.error('加载客流量数据失败:', error);
    }
}

// 添加菜品事件监听
function addDishEvents() {
    // 编辑菜品事件
    document.querySelectorAll('.edit-dish').forEach(btn => {
        btn.addEventListener('click', function() {
            const dishId = this.getAttribute('data-id');
            editDish(dishId);
        });
    });
    
    // 删除菜品事件
    document.querySelectorAll('.delete-dish').forEach(btn => {
        btn.addEventListener('click', function() {
            const dishId = this.getAttribute('data-id');
            deleteDish(dishId);
        });
    });
}

// 编辑菜品
async function editDish(dishId) {
    // 这里可以添加编辑菜品的逻辑
    showNotification('编辑功能开发中', 'info');
}

// 删除菜品
async function deleteDish(dishId) {
    if (confirm('确定要删除这个菜品吗？此操作不可恢复。')) {
        try {
            const currentUser = JSON.parse(localStorage.getItem('currentUser'));
            const response = await fetch(`/api/merchant/dishes/${dishId}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${currentUser.token}`
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                showNotification('菜品删除成功', 'success');
                loadMerchantDishes();
            } else {
                showNotification('删除失败: ' + result.message, 'error');
            }
        } catch (error) {
            console.error('删除菜品错误:', error);
            showNotification('网络错误，请稍后重试', 'error');
        }
    }
}

// 显示通知
function showNotification(message, type = 'info') {
    // 移除现有的通知
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
        ${message}
    `;
    
    // 添加样式
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
        background: ${type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : '#3498db'};
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // 显示动画
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // 3秒后自动消失
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// 辅助函数：获取品类文本
function getCategoryText(category) {
    const categories = {
        'rice': '米饭',
        'noodle': '面食',
        'dumpling': '饺子',
        'snack': '小吃'
    };
    return categories[category] || category;
}

// 辅助函数：获取口味文本
function getTasteText(taste) {
    const tastes = {
        'spicy': '辣',
        'salty': '咸',
        'light': '淡',
        'sweet': '甜'
    };
    return tastes[taste] || taste;
}