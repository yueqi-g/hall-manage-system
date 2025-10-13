<template>
  <div class="merchant-dashboard merchant-page">
    <!-- 商家专用头部 - 直接集成在页面中 -->
    <header class="header merchant-header">
      <div class="container">
        <div class="merchant-header-content">
          <div class="merchant-logo">
            <i class="fas fa-store"></i>
            <span>商家管理中心</span>
          </div>
          <div class="merchant-actions">
            <div class="merchant-info">
              <span class="merchant-name" v-if="currentUser">{{ currentUser.username }}</span>
            </div>
            <button class="logout-btn" @click="logout">
              <i class="fas fa-sign-out-alt"></i>
              退出登录
            </button>
          </div>
        </div>
      </div>
    </header>
    
    <!-- 主内容区 -->
    <main class="main merchant-main">
      <div class="container">
        <h1 class="page-title">商家管理中心</h1>
        
        <!-- 菜品管理区域 -->
        <section class="merchant-section">
          <h2><i class="fas fa-utensils"></i> 菜品管理</h2>
          <form class="dish-form" @submit.prevent="addDish" enctype="multipart/form-data">
            <div class="form-row">
              <div class="form-group">
                <label for="dishName">菜品名称 *</label>
                <input 
                  type="text" 
                  id="dishName" 
                  v-model="dishForm.name"
                  placeholder="请输入菜品名称"
                  required
                  maxlength="50"
                >
                <div class="form-hint">最多50个字符</div>
              </div>
              <div class="form-group">
                <label for="dishPrice">价格 (元) *</label>
                <input 
                  type="number" 
                  id="dishPrice" 
                  v-model="dishForm.price"
                  min="0.01" 
                  max="999.99"
                  step="0.01" 
                  placeholder="0.00"
                  required
                >
                <div class="form-hint">价格范围：0.01-999.99元</div>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="dishCategory">品类 *</label>
                <select 
                  id="dishCategory" 
                  v-model="dishForm.category"
                  required
                >
                  <option value="">请选择品类</option>
                  <option value="饭">米饭</option>
                  <option value="面">面食</option>
                  <option value="饺子">饺子</option>
                  <option value="其他">其他</option>
                </select>
              </div>
              <div class="form-group">
                <label for="dishTaste">口味 *</label>
                <select 
                  id="dishTaste" 
                  v-model="dishForm.taste"
                  required
                >
                  <option value="">请选择口味</option>
                  <option value="辣">辣</option>
                  <option value="咸">咸</option>
                  <option value="淡">淡</option>
                  <option value="酸甜">酸甜</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="spiceLevel">辣度等级</label>
                <div class="spice-level-selector">
                  <input 
                    type="range" 
                    id="spiceLevel" 
                    v-model="dishForm.spice_level"
                    min="0" 
                    max="5" 
                    step="1"
                  >
                  <div class="spice-labels">
                    <span>不辣</span>
                    <span>微辣</span>
                    <span>中辣</span>
                    <span>重辣</span>
                    <span>特辣</span>
                  </div>
                  <div class="spice-value">当前等级: {{ dishForm.spice_level }}</div>
                </div>
              </div>
              <div class="form-group">
                <label for="stockQuantity">库存数量</label>
                <input 
                  type="number" 
                  id="stockQuantity" 
                  v-model="dishForm.stock_quantity"
                  min="0" 
                  placeholder="0"
                >
                <div class="form-hint">0表示无限供应</div>
              </div>
            </div>
            <div class="form-group">
              <label for="dishDescription">菜品描述</label>
              <textarea 
                id="dishDescription" 
                v-model="dishForm.description"
                rows="3"
                placeholder="请输入菜品描述，如食材、特色等"
                maxlength="200"
              ></textarea>
              <div class="form-hint">最多200个字符，当前：{{ dishForm.description.length }}</div>
            </div>
            <div class="form-group">
              <label for="dishImage">菜品图片</label>
              <div class="image-upload">
                <input 
                  type="file" 
                  id="dishImage" 
                  ref="imageInput"
                  @change="handleImageUpload"
                  accept="image/*"
                  style="display: none"
                >
                <div class="upload-area" @click="$refs.imageInput.click()">
                  <div v-if="!dishForm.image_preview" class="upload-placeholder">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <p>点击上传菜品图片</p>
                    <small>支持 JPG、PNG 格式，大小不超过 5MB</small>
                  </div>
                  <div v-else class="image-preview">
                    <img :src="dishForm.image_preview" alt="菜品预览">
                    <button type="button" class="remove-image" @click.stop="removeImage">
                      <i class="fas fa-times"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                <i class="fas fa-plus" v-if="!isSubmitting"></i>
                <i class="fas fa-spinner fa-spin" v-else></i>
                {{ isSubmitting ? '添加中...' : '添加菜品' }}
              </button>
              <button type="button" class="btn btn-secondary" @click="resetForm">
                <i class="fas fa-undo"></i> 重置
              </button>
            </div>
          </form>
          
          <div class="dish-list">
            <h3>我的菜品列表</h3>
            <div class="dishes-container">
              <div 
                v-for="dish in dishes" 
                :key="dish.id" 
                class="dish-item"
              >
                <div class="dish-info">
                  <h3 class="dish-name">{{ dish.name }}</h3>
                  <p class="dish-price">¥{{ dish.price }}</p>
                  <div class="dish-meta">
                    <span class="dish-category">{{ getCategoryName(dish.category) }}</span>
                    <span class="dish-taste">{{ getTasteName(dish.taste) }}</span>
                  </div>
                  <p class="dish-description" v-if="dish.description">{{ dish.description }}</p>
                </div>
                <div class="dish-actions">
                  <button 
                    class="btn btn-secondary"
                    @click="editDish(dish)"
                  >
                    <i class="fas fa-edit"></i> 编辑
                  </button>
                  <button 
                    class="btn btn-danger"
                    @click="deleteDish(dish.id)"
                  >
                    <i class="fas fa-trash"></i> 删除
                  </button>
                </div>
              </div>
              <div v-if="dishes.length === 0" class="empty-state">
                <i class="fas fa-utensils"></i>
                <p>暂无菜品，请添加您的第一个菜品</p>
              </div>
            </div>
          </div>
        </section>
        
        <!-- 客流量上报区域 -->
        <section class="merchant-section">
          <h2><i class="fas fa-users"></i> 客流量管理</h2>
          <form class="traffic-form" @submit.prevent="updateTraffic">
            <div class="form-group">
              <label for="trafficCount">当前客流量</label>
              <input 
                type="number" 
                id="trafficCount" 
                v-model="trafficForm.count"
                min="0" 
                required
              >
            </div>
            <div class="form-group">
              <label for="waitingTime">平均等待时间 (分钟)</label>
              <input 
                type="number" 
                id="waitingTime" 
                v-model="trafficForm.waitingTime"
                min="0" 
                step="0.5" 
                required
              >
            </div>
            <button type="submit" class="btn btn-primary">
              <i class="fas fa-sync-alt"></i> 更新客流量
            </button>
          </form>
          
          <div class="traffic-stats">
            <div class="stat-card">
              <div class="stat-value">{{ currentTraffic }}</div>
              <div class="stat-label">当前客流量</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ avgWaitTime }}</div>
              <div class="stat-label">平均等待时间(分钟)</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ lastUpdate }}</div>
              <div class="stat-label">最后更新时间</div>
            </div>
          </div>
        </section>
      </div>
    </main>

    <!-- 页脚 -->
    <AppFooter />
  </div>
</template>

<script>
import AppFooter from '@/components/Footer.vue'
import { merchantAPI } from '@/services/api'

export default {
  name: 'MerchantDashboard',
  components: {
    AppFooter
  },
  data() {
    return {
      currentUser: null,
      isSubmitting: false,
      dishForm: {
        name: '',
        price: '',
        category: '',
        taste: '',
        description: '',
        spice_level: 0,
        stock_quantity: 0,
        image_preview: null,
        image_file: null
      },
      trafficForm: {
        count: '',
        waitingTime: ''
      },
      dishes: [],
      currentTraffic: 0,
      avgWaitTime: 0,
      lastUpdate: '--:--',
      nextDishId: 1
    }
  },
  computed: {
    getCategoryName() {
      return (category) => {
        const categories = {
          'rice': '米饭',
          'noodle': '面食',
          'dumpling': '饺子',
          'snack': '小吃'
        }
        return categories[category] || category
      }
    },
    getTasteName() {
      return (taste) => {
        const tastes = {
          'spicy': '辣',
          'salty': '咸',
          'light': '淡',
          'sweet': '甜'
        }
        return tastes[taste] || taste
      }
    }
  },
  methods: {
    checkLoginStatus() {
      const userData = localStorage.getItem('currentUser')
      if (userData) {
        this.currentUser = JSON.parse(userData)
      }
    },
    logout() {
      localStorage.removeItem('currentUser')
      localStorage.removeItem('token')
      this.currentUser = null
      alert('已退出登录')
      // 跳转到首页
      this.$router.push('/')
    },
    
    // 加载商家菜品列表
    async loadDishes() {
      try {
        console.log('加载商家菜品列表...')
        const merchant = JSON.parse(localStorage.getItem('currentUser') || '{}')
        const merchantId = merchant.merchantId || merchant.id
        const response = await merchantAPI.getDishes(merchantId)
        console.log('商家菜品列表响应:', response)
        
        // 解析后端返回的标准格式: {success: true, data: {dishes: [...]}}
        if (response && response.success && response.data) {
          this.dishes = Array.isArray(response.data.dishes) ? response.data.dishes : []
          console.log('已加载菜品数量:', this.dishes.length)
        } else {
          this.dishes = []
          console.warn('响应格式不正确或无菜品数据')
        }
      } catch (error) {
        console.error('加载菜品列表异常:', error)
        alert('加载菜品列表失败，请检查网络连接')
      }
    },
    
    // 表单验证
    validateForm() {
      const errors = []
      
      if (!this.dishForm.name.trim()) {
        errors.push('菜品名称不能为空')
      }
      if (this.dishForm.name.length > 50) {
        errors.push('菜品名称不能超过50个字符')
      }
      if (!this.dishForm.price || this.dishForm.price <= 0) {
        errors.push('请输入有效的价格')
      }
      if (this.dishForm.price > 999.99) {
        errors.push('价格不能超过999.99元')
      }
      if (!this.dishForm.category) {
        errors.push('请选择菜品品类')
      }
      if (!this.dishForm.taste) {
        errors.push('请选择菜品口味')
      }
      if (this.dishForm.description.length > 200) {
        errors.push('菜品描述不能超过200个字符')
      }
      
      return errors
    },
    
    // 处理图片上传
    handleImageUpload(event) {
      const file = event.target.files[0]
      if (!file) return
      
      // 验证文件类型
      if (!file.type.startsWith('image/')) {
        alert('请选择图片文件')
        return
      }
      
      // 验证文件大小 (5MB)
      if (file.size > 5 * 1024 * 1024) {
        alert('图片大小不能超过5MB')
        return
      }
      
      // 创建预览
      const reader = new FileReader()
      reader.onload = (e) => {
        this.dishForm.image_preview = e.target.result
        this.dishForm.image_file = file
      }
      reader.readAsDataURL(file)
    },
    
    // 移除图片
    removeImage() {
      this.dishForm.image_preview = null
      this.dishForm.image_file = null
      this.$refs.imageInput.value = ''
    },
    
    // 重置表单
    resetForm() {
      this.dishForm = {
        name: '',
        price: '',
        category: '',
        taste: '',
        description: '',
        spice_level: 0,
        stock_quantity: 0,
        image_preview: null,
        image_file: null
      }
      this.removeImage()
    },
    
    // 添加菜品
    async addDish() {
      // 表单验证
      const errors = this.validateForm()
      if (errors.length > 0) {
        alert('表单验证失败：\n' + errors.join('\n'))
        return
      }
      
      if (this.isSubmitting) return
      this.isSubmitting = true
      
      try {
        console.log('添加菜品请求:', this.dishForm)
        const merchant = JSON.parse(localStorage.getItem('currentUser') || '{}')
        const merchantId = merchant.merchantId || merchant.id
        
        // 检查 merchantId 是否有效
        if (!merchantId) {
          alert('无法确定商家信息，请重新登录')
          this.isSubmitting = false
          this.$router.push('/')
          return
        }
        
        const payload = {
          merchant: merchantId,
          name: this.dishForm.name.trim(),
          description: this.dishForm.description.trim(),
          price: Number(this.dishForm.price),
          category: this.dishForm.category,
          taste: this.dishForm.taste,
          spice_level: Number(this.dishForm.spice_level),
          stock_quantity: Number(this.dishForm.stock_quantity) || 0,
          is_available: true
        }
        
        // 如果有图片，先上传图片
        if (this.dishForm.image_file) {
          const imageUrl = await this.uploadImage(this.dishForm.image_file)
          payload.image_url = imageUrl
        }
        
        console.log('发送的payload:', payload)
        const response = await merchantAPI.addDish(payload)
        console.log('添加菜品响应:', response)
        
        // 检查响应格式：后端返回 {success: true, data: {...}, message: "..."}
        if (response && response.success) {
          alert('菜品添加成功！')
          this.resetForm()
          this.loadDishes()
        } else {
          alert('菜品添加失败: ' + ((response && response.message) || '未知错误'))
        }
      } catch (error) {
        console.error('添加菜品异常:', error)
        let errorMessage = '添加菜品失败'
        if (error.response?.data) {
          // 提取后端返回的错误信息
          const errorData = error.response.data
          if (typeof errorData === 'object') {
            errorMessage += ':\n' + Object.entries(errorData)
              .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
              .join('\n')
          } else {
            errorMessage += ': ' + errorData
          }
        } else if (error.message) {
          errorMessage += ': ' + error.message
        }
        alert(errorMessage)
      } finally {
        this.isSubmitting = false
      }
    },
    
    // 上传图片
    async uploadImage(file) {
      // 这里可以实现图片上传到云存储或本地存储
      // 暂时返回一个占位符URL
      return new Promise((resolve) => {
        const reader = new FileReader()
        reader.onload = (e) => {
          resolve(e.target.result) // 返回base64编码的图片
        }
        reader.readAsDataURL(file)
      })
    },
    
    // 编辑菜品
    editDish(dish) {
      // 将菜品数据填充到表单进行编辑
      this.dishForm = { ...dish }
    },
    
    // 删除菜品
    async deleteDish(dishId) {
      if (!confirm('确定要删除这个菜品吗？')) {
        return
      }
      
      try {
        console.log('删除菜品请求:', dishId)
        const response = await merchantAPI.deleteDish(dishId)
        console.log('删除菜品响应:', response)
        
        // 检查响应格式
        if (response && response.success) {
          alert('菜品删除成功！')
          // 重新加载菜品列表
          this.loadDishes()
        } else {
          alert('菜品删除失败: ' + (response?.message || '未知错误'))
        }
      } catch (error) {
        console.error('删除菜品异常:', error)
        alert('删除菜品失败，请检查网络连接')
      }
    },
    
    // 更新客流量
    async updateTraffic() {
      try {
        // 获取商家ID
        const merchant = JSON.parse(localStorage.getItem('currentUser') || '{}')
        const merchantId = merchant.merchantId || merchant.id
        
        if (!merchantId) {
          alert('无法获取商家信息，请重新登录')
          return
        }
        
        console.log('更新客流量请求:', this.trafficForm, 'merchantId:', merchantId)
        const response = await merchantAPI.updateTraffic(merchantId, this.trafficForm)
        console.log('更新客流量响应:', response)
        
        if (response && response.success) {
          alert('客流量信息更新成功！')
          // 更新统计数据
          this.currentTraffic = response.data.currentTraffic
          this.avgWaitTime = response.data.avgWaitTime
          this.lastUpdate = new Date().toLocaleTimeString('zh-CN', { 
            hour: '2-digit', 
            minute: '2-digit' 
          })
          // 重置表单
          this.trafficForm = {
            count: '',
            waitingTime: ''
          }
        } else {
          alert('客流量更新失败: ' + (response?.message || '未知错误'))
        }
      } catch (error) {
        console.error('更新客流量异常:', error)
        alert('更新客流量失败，请检查网络连接')
      }
    },
    
    // 加载商家统计
    async loadStats() {
      try {
        console.log('加载商家统计...')
        const response = await merchantAPI.getStats()
        console.log('商家统计响应:', response)
        
        if (response.success) {
          // 这里可以根据实际API响应结构更新统计数据
          // 暂时使用默认值
          this.currentTraffic = response.data.currentTraffic || 0
          this.avgWaitTime = response.data.avgWaitTime || 0
          this.lastUpdate = response.data.lastUpdate || '--:--'
        } else {
          // getStats暂未实现，这是正常的，不需要报错
          console.log('商家统计功能暂未实现（这是正常的）')
        }
      } catch (error) {
        console.error('加载商家统计异常:', error)
      }
    }
  },
  async mounted() {
    this.checkLoginStatus()
    
    // 检查登录状态和权限
    const userData = localStorage.getItem('currentUser')
    if (!userData) {
      this.$router.push('/')
      return
    }
    
    const currentUser = JSON.parse(userData)
    // 这里可以添加商家权限检查
    if (currentUser.type && currentUser.type !== 'merchant') {
      this.$router.push('/')
      return
    }
    
    // 若缺少 merchantId，尝试查找并补全后再加载
    const proceed = async () => {
      await this.loadDishes()
      this.loadStats()
    }
    if (!currentUser.merchantId) {
      try {
        const base = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000/api'
        const resp = await fetch(`${base}/merchants/?search=${encodeURIComponent(currentUser.username)}`)
        const data = await resp.json()
        const results = Array.isArray(data?.results) ? data.results : data
        if (Array.isArray(results) && results.length > 0) {
          const patched = { ...currentUser, merchantId: results[0].id }
          localStorage.setItem('currentUser', JSON.stringify(patched))
        }
      } catch (e) {
        // 忽略查找失败
      }
    }
    await proceed()
  }
}
</script>

<style scoped>
/* 只定义必要的组件特定样式，大部分样式复用merchant.css */
.merchant-dashboard {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #6c757d;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 15px;
  color: #adb5bd;
}

.dishes-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* 商家头部样式 */
.merchant-header {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  color: white;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.2);
}

.merchant-header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
}

.merchant-logo {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
}

.merchant-logo i {
  margin-right: 10px;
  font-size: 1.8rem;
}

.merchant-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.merchant-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.merchant-name {
  font-weight: 500;
  color: #ecf0f1;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
}

/* 表单样式增强 */
.form-hint {
  font-size: 0.8rem;
  color: #6c757d;
  margin-top: 4px;
}

.spice-level-selector {
  margin-top: 8px;
}

.spice-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #6c757d;
  margin-top: 8px;
}

.spice-value {
  text-align: center;
  font-weight: bold;
  color: #e74c3c;
  margin-top: 8px;
}

.image-upload {
  margin-top: 8px;
}

.upload-area {
  border: 2px dashed #dee2e6;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

.upload-area:hover {
  border-color: #007bff;
  background: #e3f2fd;
}

.upload-placeholder {
  color: #6c757d;
}

.upload-placeholder i {
  font-size: 2rem;
  margin-bottom: 10px;
  display: block;
}

.image-preview {
  position: relative;
  display: inline-block;
}

.image-preview img {
  max-width: 200px;
  max-height: 150px;
  border-radius: 8px;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn .fa-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 菜品列表样式增强 */
.dish-item {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
}

.dish-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.dish-info {
  margin-bottom: 15px;
}

.dish-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.dish-price {
  font-size: 1.1rem;
  font-weight: bold;
  color: #e74c3c;
  margin-bottom: 8px;
}

.dish-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 8px;
}

.dish-meta span {
  background: #f8f9fa;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #495057;
}

.dish-description {
  color: #6c757d;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 15px;
}

.dish-actions {
  display: flex;
  gap: 10px;
}

.dish-actions .btn {
  flex: 1;
  padding: 8px 16px;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .merchant-header-content {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .merchant-logo {
    font-size: 1.3rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .dish-actions {
    flex-direction: column;
  }
}
</style>
