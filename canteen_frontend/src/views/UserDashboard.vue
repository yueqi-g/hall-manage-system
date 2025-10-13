<template>
  <div class="user-dashboard">
    <!-- 复用现有Header -->
    <AppHeader />
    
    <!-- 主内容区 -->
    <main class="main">
      <!-- 英雄区域 -->
      <section class="hero">
        <div class="container">
          <div class="hero-content">
            <h1 class="hero-title">{{ $t('heroTitle') }}</h1>
            <p class="hero-subtitle">{{ $t('heroSubtitle') }}</p>
            <div class="search-box">
              <div class="search-input-container">
                <input 
                  type="text" 
                  :placeholder="$t('searchPlaceholder')" 
                  class="search-input"
                  v-model="searchQuery"
                  @input="handleSearchInput"
                  @keyup.enter="handleSearch"
                  @focus="showSuggestions = searchSuggestions.length > 0"
                  @blur="setTimeout(() => showSuggestions = false, 200)"
                >
                <!-- 搜索建议下拉框 -->
                <div v-if="showSuggestions && searchSuggestions.length > 0" class="search-suggestions">
                  <div 
                    v-for="(suggestion, index) in searchSuggestions" 
                    :key="index"
                    class="suggestion-item"
                    @click="useSuggestion(suggestion)"
                  >
                    <i class="fas fa-search"></i>
                    <span>{{ suggestion }}</span>
                  </div>
                </div>
              </div>
              <button class="search-btn" @click="handleSearch">
                <i class="fas fa-search"></i>
                {{ $t('smartRecommendation') }}
              </button>
            </div>
          </div>
          <div class="filter-panel">
            <h3>{{ $t('preciseFiltering') }}</h3>
            
            <!-- 品类筛选 -->
            <div class="filter-group">
              <label for="category">{{ $t('category') }}</label>
              <select id="category" class="filter-select" v-model="filters.category">
                <option value="">{{ $t('allCategories') }}</option>
                <option value="饭">{{ $t('rice') }}</option>
                <option value="面">{{ $t('noodles') }}</option>
                <option value="饺子">{{ $t('dumplings') }}</option>
                <option value="其他">{{ $t('other') }}</option>
              </select>
            </div>
            
            <!-- 口味筛选 -->
            <div class="filter-group">
              <span>{{ $t('tastePreference') }}</span>
              <div class="flavor-tags">
                <span 
                  v-for="flavor in flavorOptions" 
                  :key="flavor.value"
                  class="flavor-tag" 
                  :class="{ active: filters.flavors.includes(flavor.value) }"
                  @click="toggleFlavor(flavor.value)"
                >
                  {{ $t(flavor.value) }}
                </span>
              </div>
            </div>
            
            <!-- 价格范围 -->
            <div class="filter-group">
              <span>{{ $t('priceRange') }}</span>
              <div class="range-inputs">
                <input 
                  type="number" 
                  id="price-min" 
                  :placeholder="$t('minPrice')" 
                  min="0" 
                  max="100"
                  v-model.number="filters.priceMin"
                >
                <span class="range-separator">-</span>
                <input 
                  type="number" 
                  id="price-max" 
                  :placeholder="$t('maxPrice')" 
                  min="0" 
                  max="100"
                  v-model.number="filters.priceMax"
                >
              </div>
              <div class="price-slider">
                <input 
                  type="range" 
                  id="price-range-min" 
                  min="0" 
                  max="50" 
                  v-model.number="filters.priceMin"
                >
                <input 
                  type="range" 
                  id="price-range-max" 
                  min="0" 
                  max="50" 
                  v-model.number="filters.priceMax"
                >
              </div>
              <div class="price-display">¥{{ filters.priceMin }} - ¥{{ filters.priceMax }}</div>
            </div>
            
            <!-- 人流量 -->
            <div class="filter-group">
              <span>{{ $t('crowdFlow') }}</span>
              <div class="crowd-level">
                <div class="crowd-option" v-for="option in crowdOptions" :key="option.value">
                  <input 
                    type="radio" 
                    :id="'crowd-' + option.value" 
                    name="crowd" 
                    :value="option.value"
                    v-model="filters.crowd"
                  >
                  <label :for="'crowd-' + option.value">{{ $t(option.value) }}</label>
                </div>
              </div>
            </div>
            
            <!-- 辣度筛选 -->
            <div class="filter-group">
              <span>{{ $t('spiceLevel') }}</span>
              <div class="spice-level-filter">
                <input 
                  type="range" 
                  v-model="filters.spiceLevel"
                  min="0" 
                  max="5" 
                  step="1"
                  class="spice-slider"
                >
                <div class="spice-labels">
                  <span>{{ $t('notSpicy') }}</span>
                  <span>{{ $t('mildSpicy') }}</span>
                  <span>{{ $t('mediumSpicy') }}</span>
                  <span>{{ $t('hotSpicy') }}</span>
                  <span>{{ $t('extraSpicy') }}</span>
                </div>
                <div class="spice-value">{{ $t('maxSpiceLevel') }}: {{ filters.spiceLevel }}</div>
              </div>
            </div>
            
            <!-- 食堂筛选 -->
            <div class="filter-group">
              <label for="hall">{{ $t('canteen') }}</label>
              <select id="hall" class="filter-select" v-model="filters.hall">
                <option value="">{{ $t('allCanteens') }}</option>
                <option value="第一食堂">{{ $t('firstCanteen') }}</option>
                <option value="第二食堂">{{ $t('secondCanteen') }}</option>
                <option value="第三食堂">{{ $t('thirdCanteen') }}</option>
                <option value="第四食堂">{{ $t('fourthCanteen') }}</option>
              </select>
            </div>
            
            <!-- 排序方式 -->
            <div class="filter-group">
              <label for="sortBy">{{ $t('sortBy') }}</label>
              <select id="sortBy" class="filter-select" v-model="filters.sortBy">
                <option value="created_at">{{ $t('newest') }}</option>
                <option value="price">{{ $t('priceLowToHigh') }}</option>
                <option value="-price">{{ $t('priceHighToLow') }}</option>
                <option value="name">{{ $t('nameSort') }}</option>
                <option value="popular">{{ $t('popular') }}</option>
              </select>
            </div>
            
            <!-- 操作按钮 -->
            <div class="filter-actions">
              <button class="btn-filter-apply" @click="applyFilters">
                <i class="fas fa-search"></i> {{ $t('applyFilters') }}
              </button>
              <button class="btn-filter-reset" @click="resetFilters">
                <i class="fas fa-undo"></i> {{ $t('reset') }}
              </button>
              <button class="btn-filter-save" @click="savePreferences">
                <i class="fas fa-heart"></i> {{ $t('savePreferences') }}
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- 功能区域 -->
      <section class="features">
        <div class="container">
          <h2 class="section-title">{{ $t('coreFeatures') }}</h2>
          <div class="features-grid">
            <div class="feature-card" v-for="feature in features" :key="feature.id">
              <div class="feature-icon">
                <i :class="feature.icon"></i>
              </div>
              <h3>{{ $t(`features.${feature.id-1}.title`) }}</h3>
              <p>{{ $t(`features.${feature.id-1}.description`) }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 热门推荐和AI助手区域 -->
      <section class="recommendation-section">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">{{ $t('aiFoodAssistant') }}</h2>
            <h2 class="section-title">{{ $t('todayHotRecommendations') }}</h2>
          </div>
          <div class="red-line"></div>
          
          <div class="content-container">
            <!-- 左侧：AI助手 -->
            <div class="ai-assistant-side">
              <div class="ai-header">
                <div class="ai-avatar">
                  <i class="fas fa-robot"></i>
                </div>
                <div class="ai-intro">
                  <h3>{{ $t('aiAssistantIntro') }}</h3>
                  <p>{{ $t('aiAssistantDescription') }}</p>
                </div>
              </div>
              
              <div class="ai-chat-container">
                <div class="chat-messages" ref="chatMessages">
                  <div class="message ai-message">
                    <div class="message-content">
                      <p>{{ $t('aiAssistantPrompt') }}</p>
                    </div>
                  </div>
                </div>
                
                <div class="chat-input-container">
                  <div class="input-example">
                    <span>{{ $t('inputExample') }}</span>
                  </div>
                  <div class="input-group">
                    <input 
                      type="text" 
                      ref="foodInput"
                      :placeholder="$t('inputPlaceholder')" 
                      class="chat-input"
                      v-model="aiInput"
                      @keypress.enter="handleAIMessage"
                    >
                    <button class="send-btn" @click="handleAIMessage">
                      <i class="fas fa-paper-plane"></i>
                    </button>
                  </div>
                  <div class="examples">
                    <span>{{ $t('examples') }}</span>
                    <span 
                      class="example-text" 
                      v-for="example in exampleQuestions" 
                      :key="example"
                      @click="useExample(example)"
                    >
                      {{ example }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 右侧：热门推荐 -->
            <div class="popular-dishes-side">
              <div class="dishes-grid">
                <div 
                  class="dish-card" 
                  v-for="dish in popularDishes" 
                  :key="dish.id"
                  @click="viewDishDetail(dish.id)"
                >
                  <div class="dish-image" :style="{ background: dish.color }">
                    <div class="dish-rating">
                      <i class="fas fa-star"></i> {{ dish.rating }}
                    </div>
                    <i :class="dish.icon"></i>
                  </div>
                  <div class="dish-info">
                    <div class="dish-header">
                      <h3 class="dish-name">{{ dish.name }}</h3>
                      <div class="dish-price">¥{{ dish.price }}</div>
                    </div>
                    <p class="dish-description">{{ dish.description }}</p>
                    <div class="dish-meta">
                      <span class="dish-canteen">{{ dish.canteen }}</span>
                      <span class="dish-wait-time">
                        <i class="fas fa-clock"></i> {{ dish.waitTime }}
                      </span>
                    </div>
                    <div class="dish-tags">
                      <span 
                        v-for="tag in dish.tags" 
                        :key="tag"
                        class="dish-tag"
                        :class="getTagClass(tag)"
                      >
                        {{ tag }}
                      </span>
                    </div>
                    <div class="dish-actions">
                      <button class="dish-btn primary" @click.stop="orderDish(dish.id)">
                        <i class="fas fa-utensils"></i> {{ $t('orderNow') }}
                      </button>
                      <button class="dish-btn secondary" @click.stop="addToFavorites(dish.id)">
                        <i class="fas fa-heart"></i> {{ $t('addToFavorites') }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
    
    <!-- 复用现有Footer -->
    <AppFooter />
    
    <!-- 复用现有LoginModal -->
    <LoginModal v-if="showLoginModal" @close="showLoginModal = false" />
  </div>
</template>

<script>
import AppHeader from '@/components/Header.vue'
import AppFooter from '@/components/Footer.vue'
import LoginModal from '@/components/LoginModal.vue'
import { dishesAPI, ordersAPI, userAPI  } from '@/services/api'

export default {
  name: 'UserDashboard',
  components: {
    AppHeader,
    AppFooter,
    LoginModal
  },
  data() {
    return {
      showLoginModal: false,
      searchQuery: '',
      searchSuggestions: [],
      showSuggestions: false,
      searchTimeout: null,
      filters: {
        category: '',
        flavors: [],
        priceMin: 0,
        priceMax: 50,
        crowd: 'any',
        spiceLevel: '',  // 默认不限制辣度，让用户可以看到所有菜品
        hall: '',
        sortBy: 'created_at'
      },
      flavorOptions: [
        { value: '辣', label: '辣' },
        { value: '咸', label: '咸' },
        { value: '淡', label: '淡' },
        { value: '酸甜', label: '酸甜' }
      ],
      crowdOptions: [
        { value: 'low', label: '稀少' },
        { value: 'medium', label: '适中' },
        { value: 'high', label: '拥挤' },
        { value: 'any', label: '不限' }
      ],
      features: [
        {
          id: 1,
          icon: 'fas fa-utensils',
          title: '智能菜品推荐',
          description: '基于AI分析您的口味偏好，为您精准推荐合适的美食'
        },
        {
          id: 2,
          icon: 'fas fa-chart-line',
          title: '实时客流量',
          description: '查看各食堂窗口实时客流，避开排队高峰'
        },
        {
          id: 3,
          icon: 'fas fa-search',
          title: '精准筛选',
          description: '按品类、口味、价格等多维度筛选菜品'
        },
        {
          id: 4,
          icon: 'fas fa-store',
          title: '商家管理',
          description: '商家可便捷管理菜品信息和更新客流数据'
        }
      ],
      aiInput: '',
      exampleQuestions: [
        '我想吃辣的面食，价格实惠的',
        '推荐清淡的粤菜，人均100-200元',
        '适合情侣约会的西餐厅'
      ],
      popularDishes: [
        {
          id: 1,
          name: "麻辣香锅",
          price: 28,
          rating: 4.8,
          description: "香辣可口，配料丰富，多种食材任你选择",
          canteen: "第一食堂",
          waitTime: "15-20分钟",
          tags: ["辣", "实惠", "推荐"],
          color: "linear-gradient(45deg, #ff9a9e, #fad0c4)",
          icon: "fas fa-utensils"
        },
        {
          id: 2,
          name: "番茄牛肉面",
          price: 22,
          rating: 4.6,
          description: "新鲜番茄熬制汤底，牛肉鲜嫩多汁",
          canteen: "第二食堂",
          waitTime: "10-15分钟",
          tags: ["不辣", "面食"],
          color: "linear-gradient(45deg, #a1c4fd, #c2e9fb)",
          icon: "fas fa-bowl-food"
        },
        {
          id: 3,
          name: "黄焖鸡米饭",
          price: 25,
          rating: 4.7,
          description: "鸡肉鲜嫩，汤汁浓郁，配米饭绝佳",
          canteen: "第三食堂",
          waitTime: "12-18分钟",
          tags: ["微辣", "米饭", "热门"],
          color: "linear-gradient(45deg, #ffecd2, #fcb69f)",
          icon: "fas fa-burger"
        },
        {
          id: 4,
          name: "扬州炒饭",
          price: 18,
          rating: 4.5,
          description: "粒粒分明，配料丰富，传统经典",
          canteen: "第四食堂",
          waitTime: "8-12分钟",
          tags: ["不辣", "实惠", "推荐"],
          color: "linear-gradient(45deg, #84fab0, #8fd3f4)",
          icon: "fas fa-pizza-slice"
        }
      ]
    }
  },
  methods: {
    // 处理搜索输入
    handleSearchInput() {
      // 清除之前的定时器
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout)
      }
      
      // 设置新的定时器，延迟500ms执行搜索建议
      this.searchTimeout = setTimeout(() => {
        this.getSearchSuggestions()
      }, 500)
    },
    
    // 获取搜索建议
    async getSearchSuggestions() {
      if (!this.searchQuery.trim() || this.searchQuery.length < 2) {
        this.showSuggestions = false
        return
      }
      
      try {
        const response = await dishesAPI.searchSuggestions({
          q: this.searchQuery
        })
        
        this.searchSuggestions = response || []
        this.showSuggestions = this.searchSuggestions.length > 0
      } catch (error) {
        console.error('获取搜索建议失败:', error)
        this.showSuggestions = false
      }
    },
    
    // 使用搜索建议
    useSuggestion(suggestion) {
      this.searchQuery = suggestion
      this.showSuggestions = false
      this.handleSearch()
    },
    
    // 菜品搜索
    async handleSearch() {
      if (!this.searchQuery.trim()) return
      
      this.showSuggestions = false
      console.log('开始菜品搜索:', this.searchQuery)
      
      try {
        const response = await dishesAPI.search({
          q: this.searchQuery,
          page: 1,
          limit: 10
        })
        
        console.log('菜品搜索结果:', response)
        
        if (response.success) {
          // 这里可以处理搜索结果，比如显示搜索结果页面
          alert(`搜索到 ${response.data.dishes.length} 个相关菜品`)
        } else {
          alert('搜索失败: ' + (response.message || '未知错误'))
        }
      } catch (error) {
        console.error('菜品搜索失败:', error)
        alert('搜索失败，请检查网络连接')
      }
    },
    
    toggleFlavor(flavor) {
      const index = this.filters.flavors.indexOf(flavor)
      if (index > -1) {
        this.filters.flavors.splice(index, 1)
      } else {
        this.filters.flavors.push(flavor)
      }
    },
    
    // 菜品筛选
    async applyFilters() {
      console.log('应用筛选条件:', this.filters)
      
      try {
        const params = {
          category: this.filters.category,
          tastes: this.filters.flavors.join(','),
          price_min: this.filters.priceMin,
          price_max: this.filters.priceMax,
          crowd_level: this.filters.crowd,
          spice_level: this.filters.spiceLevel,
          hall: this.filters.hall,
          ordering: this.filters.sortBy
        }
        
        // 移除空值参数
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) {
            delete params[key]
          }
        })
        
        console.log('发送筛选请求参数:', params)
        
        const response = await dishesAPI.filter(params)
        
        console.log('菜品筛选结果:', response)
        
        // 后端返回格式: {success: true, data: {dishes: [...], filters: {...}}}
        if (response && response.success && response.data) {
          const dishes = Array.isArray(response.data.dishes) ? response.data.dishes : []
          const count = dishes.length
          
          console.log('解析后的菜品数据:', dishes)
          
          // 显示筛选结果
          this.showFilterResults(dishes, count)
        } else {
          alert('筛选失败: ' + (response?.message || '未知错误'))
        }
      } catch (error) {
        console.error('菜品筛选失败:', error)
        alert('筛选失败，请检查网络连接')
      }
    },
    
    // 显示筛选结果
    showFilterResults(dishes, count) {
      console.log('显示筛选结果，菜品数量:', count, dishes)
      
      // 如果没有找到菜品
      if (count === 0 || dishes.length === 0) {
        alert('未找到符合条件的菜品，请尝试调整筛选条件')
        return
      }
      
      // 这里可以创建一个模态框或结果页面来显示筛选结果
      const resultMessage = `找到 ${count} 个符合条件的菜品：\n\n` + 
        dishes.slice(0, 5).map(dish => 
          `• ${dish.name} - ¥${dish.price} (${dish.merchant_name || '未知商家'})`
        ).join('\n') + 
        (dishes.length > 5 ? `\n... 还有 ${dishes.length - 5} 个菜品` : '')
      
      alert(resultMessage)
    },
    
    // 保存用户偏好
    async savePreferences() {
      const currentUser = JSON.parse(localStorage.getItem('currentUser'))
      if (!currentUser) {
        this.showLoginModal = true
        return
      }
      
      try {
        const preferences = {
          preferred_categories: this.filters.category ? [this.filters.category] : [],
          preferred_tastes: this.filters.flavors,
          price_range_min: this.filters.priceMin,
          price_range_max: this.filters.priceMax,
          dietary_restrictions: []
        }
        
        const response = await userAPI.updatePreferences(preferences)
        
        if (response.success) {
          alert('偏好设置已保存！')
        } else {
          alert('保存偏好失败: ' + (response.message || '未知错误'))
        }
      } catch (error) {
        console.error('保存偏好失败:', error)
        alert('保存偏好失败，请检查网络连接')
      }
    },
    
    resetFilters() {
      this.filters = {
        category: '',
        flavors: [],
        priceMin: 0,
        priceMax: 50,
        crowd: 'any',
        spiceLevel: '',  // 改为空字符串，表示不限制辣度
        hall: '',
        sortBy: 'created_at'
      }
    },
    
    // AI智能推荐
    async handleAIMessage() {
      if (!this.aiInput.trim()) return
      
      // 添加用户消息
      this.addMessage(this.aiInput, 'user')
      
      try {
        // 获取用户偏好
        const currentUser = JSON.parse(localStorage.getItem('currentUser'))
        const preferences = currentUser?.preferences || {
          flavors: [],
          budget: { min: 0, max: 50 },
          dietary: []
        }
        
        console.log('发送AI推荐请求:', this.aiInput, preferences)
        
        const response = await dishesAPI.aiRecommend({
          query: this.aiInput,
          preferences: preferences
        })
        
        console.log('AI推荐结果:', response)
        
        if (response.success) {
          const aiResponse = this.formatAIResponse(response.data)
          this.addMessage(aiResponse, 'ai')
        } else {
          this.addMessage('抱歉，AI推荐服务暂时不可用，请稍后再试。', 'ai')
        }
      } catch (error) {
        console.error('AI推荐失败:', error)
        this.addMessage('抱歉，AI推荐服务暂时不可用，请稍后再试。', 'ai')
      }
      
      // 滚动到底部
      this.$nextTick(() => {
        const chatMessages = this.$refs.chatMessages
        if (chatMessages) {
          chatMessages.scrollTop = chatMessages.scrollHeight
        }
      })
      
      // 清空输入框
      this.aiInput = ''
    },
    
    formatAIResponse(data) {
      let response = '根据您的需求，我为您推荐以下菜品：\n\n'
      
      if (data.recommendations && data.recommendations.length > 0) {
        data.recommendations.forEach((rec, index) => {
          response += `${index + 1}. ${rec.dish.name} (${rec.dish.canteen}) - ¥${rec.dish.price}\n`
          response += `   推荐理由: ${rec.reason}\n`
          response += `   匹配度: ${Math.round(rec.matchScore * 100)}%\n\n`
        })
      } else {
        response = '抱歉，没有找到符合您需求的菜品，请尝试调整您的搜索条件。'
      }
      
      return response
    },
    
    addMessage(text, type) {
      const chatMessages = this.$refs.chatMessages
      if (!chatMessages) return
      
      const messageDiv = document.createElement('div')
      messageDiv.className = `message ${type}-message`
      
      if (type === 'user') {
        messageDiv.innerHTML = `
          <div class="message-content">
            <p>${text}</p>
          </div>
        `
      } else {
        messageDiv.innerHTML = `
          <div class="message-content">
            <p>${text}</p>
          </div>
        `
      }
      
      chatMessages.appendChild(messageDiv)
    },
    
    useExample(example) {
      this.aiInput = example
      this.handleAIMessage()
    },
    
    getTagClass(tag) {
      if (tag === '辣' || tag === '麻辣' || tag === '酸辣') return 'spicy'
      if (tag === '实惠' || tag === '便宜') return 'cheap'
      return ''
    },
    
    viewDishDetail(dishId) {
      console.log('查看菜品详情:', dishId)
      // 这里可以跳转到菜品详情页面
    },
    
    // 下单菜品
    async orderDish(dishId) {
      const currentUser = JSON.parse(localStorage.getItem('currentUser'))
      if (!currentUser) {
        this.showLoginModal = true
        return
      }
      
      try {
        console.log('下单菜品:', dishId)
        
        const response = await ordersAPI.createOrder({
          dishId: dishId,
          quantity: 1
        })
        
        console.log('下单结果:', response)
        
        if (response.success) {
          alert(`下单成功！订单号: ${response.data.orderId}\n预计等待时间: ${response.data.estimatedWaitTime}分钟`)
        } else {
          alert('下单失败: ' + (response.message || '未知错误'))
        }
      } catch (error) {
        console.error('下单失败:', error)
        alert('下单失败，请检查网络连接')
      }
    },
    
    // 收藏菜品
    async addToFavorites(dishId) {
      const currentUser = JSON.parse(localStorage.getItem('currentUser'))
      if (!currentUser) {
        this.showLoginModal = true
        return
      }
      
      try {
        console.log('收藏菜品:', dishId)
        
        const response = await ordersAPI.addFavorite({
          dishId: dishId
        })
        
        console.log('收藏结果:', response)
        
        if (response.success) {
          alert('收藏成功！')
        } else {
          alert('收藏失败: ' + (response.message || '未知错误'))
        }
      } catch (error) {
        console.error('收藏失败:', error)
        alert('收藏失败，请检查网络连接')
      }
    },
    
    // 加载热门推荐
    async loadPopularDishes() {
      try {
        console.log('加载热门推荐...')
        
        const response = await dishesAPI.getPopular()
        
        console.log('热门推荐结果:', response)
        
        // 后端返回格式: {success: true, data: {dishes: [...]}}
        if (response && response.success && response.data) {
          const dishes = Array.isArray(response.data.dishes) ? response.data.dishes : []
          
          console.log('解析后的热门菜品:', dishes)
          
          this.popularDishes = dishes.map(dish => ({
            ...dish,
            color: this.getRandomGradient(),
            icon: this.getDishIcon(dish.category)
          }))
        } else {
          console.log('加载热门推荐失败:', response?.message || '未知错误')
        }
      } catch (error) {
        console.error('加载热门推荐失败:', error)
      }
    },
    
    getRandomGradient() {
      const gradients = [
        'linear-gradient(45deg, #ff9a9e, #fad0c4)',
        'linear-gradient(45deg, #a1c4fd, #c2e9fb)',
        'linear-gradient(45deg, #ffecd2, #fcb69f)',
        'linear-gradient(45deg, #84fab0, #8fd3f4)'
      ]
      return gradients[Math.floor(Math.random() * gradients.length)]
    },
    
    getDishIcon(category) {
      const icons = {
        '主食': 'fas fa-utensils',
        '面食': 'fas fa-bowl-food',
        '米饭': 'fas fa-burger',
        '小吃': 'fas fa-pizza-slice',
        '饮品': 'fas fa-coffee',
        '早餐': 'fas fa-egg'
      }
      return icons[category] || 'fas fa-utensils'
    }
  },
  mounted() {
    console.log('用户仪表板已加载')
    // 加载热门推荐数据
    this.loadPopularDishes()
  }
}
</script>

<style>
/* 搜索建议样式 */
.search-input-container {
  position: relative;
  flex: 1;
}

.search-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  max-height: 200px;
  overflow-y: auto;
}

.suggestion-item {
  padding: 12px 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: background-color 0.2s ease;
  border-bottom: 1px solid #f8f9fa;
}

.suggestion-item:hover {
  background-color: #f8f9fa;
}

.suggestion-item:last-child {
  border-bottom: none;
}

.suggestion-item i {
  color: #6c757d;
  font-size: 0.9rem;
}

/* 筛选面板样式增强 */
.filter-panel {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-top: 30px;
}

.filter-group {
  margin-bottom: 20px;
}

.filter-group label {
  display: block;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.filter-select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 0.9rem;
  background: white;
  transition: border-color 0.3s ease;
}

.filter-select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.flavor-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.flavor-tag {
  padding: 6px 12px;
  border: 1px solid #dee2e6;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.8rem;
  background: white;
  color: #495057;
}

.flavor-tag:hover {
  border-color: #007bff;
  color: #007bff;
}

.flavor-tag.active {
  background: #007bff;
  border-color: #007bff;
  color: white;
}

.range-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
}

.range-inputs input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 0.9rem;
}

.range-separator {
  color: #6c757d;
  font-weight: bold;
}

.price-slider {
  margin-top: 10px;
}

.price-display {
  text-align: center;
  font-weight: bold;
  color: #e74c3c;
  margin-top: 8px;
}

.crowd-level {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 8px;
}

.crowd-option {
  display: flex;
  align-items: center;
  gap: 6px;
}

.crowd-option input[type="radio"] {
  margin: 0;
}

.crowd-option label {
  margin: 0;
  cursor: pointer;
  font-weight: normal;
}

.spice-level-filter {
  margin-top: 8px;
}

.spice-slider {
  width: 100%;
  margin: 10px 0;
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

.filter-actions {
  display: flex;
  gap: 15px;
  margin-top: 25px;
  flex-wrap: wrap;
}

.btn-filter-apply,
.btn-filter-reset,
.btn-filter-save {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-filter-apply {
  background: #007bff;
  color: white;
}

.btn-filter-apply:hover {
  background: #0056b3;
  transform: translateY(-1px);
}

.btn-filter-reset {
  background: #6c757d;
  color: white;
}

.btn-filter-reset:hover {
  background: #545b62;
  transform: translateY(-1px);
}

.btn-filter-save {
  background: #28a745;
  color: white;
}

.btn-filter-save:hover {
  background: #1e7e34;
  transform: translateY(-1px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .filter-actions {
    flex-direction: column;
  }
  
  .btn-filter-apply,
  .btn-filter-reset,
  .btn-filter-save {
    width: 100%;
    justify-content: center;
  }
  
  .flavor-tags {
    justify-content: center;
  }
  
  .crowd-level {
    justify-content: center;
  }
}
</style>
