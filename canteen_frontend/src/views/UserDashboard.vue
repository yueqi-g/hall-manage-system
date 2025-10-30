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
                  @blur="handleSearchBlur"
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
            <div class="filter-header">
              <h3>{{ $t('preciseFiltering') }}</h3>
              <button class="btn-filter-reset-small" @click="resetFilters">
                <i class="fas fa-undo"></i> {{ $t('reset') }}
              </button>
            </div>
            
            <!-- 品类筛选 - 标签和下拉框在同一行 -->
            <div class="filter-row-inline">
              <span class="filter-label">{{ $t('category') }}</span>
              <select id="category" class="filter-select-inline" v-model="filters.category">
                <option value="">{{ $t('allCategories') }}</option>
                <option value="饭">{{ $t('rice') }}</option>
                <option value="面">{{ $t('noodles') }}</option>
                <option value="饺子">{{ $t('dumplings') }}</option>
                <option value="其他">{{ $t('other') }}</option>
              </select>
            </div>
            
            <!-- 口味偏好 - 标签和按钮在同一行 -->
            <div class="filter-row-inline">
              <span class="filter-label">{{ $t('tastePreference') }}</span>
              <div class="flavor-tags-inline">
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
            
            <!-- 价格范围 - 标签和输入框在同一行 -->
            <div class="filter-row-inline">
              <span class="filter-label">{{ $t('priceRange') }}</span>
              <div class="price-range-inline">
                <span class="price-symbol">¥</span>
                <input 
                  type="number" 
                  id="price-min" 
                  :placeholder="$t('minPrice')" 
                  min="0" 
                  max="100"
                  v-model.number="filters.priceMin"
                  class="price-input-inline"
                >
                <span class="range-separator">-</span>
                <span class="price-symbol">¥</span>
                <input 
                  type="number" 
                  id="price-max" 
                  :placeholder="$t('maxPrice')" 
                  min="0" 
                  max="100"
                  v-model.number="filters.priceMax"
                  class="price-input-inline"
                >
              </div>
            </div>
            
            <!-- 辣度等级 - 使用新的格式 -->
            <div class="filter-row-inline">
              <span class="filter-label">{{ $t('maxSpiceLevel') }}</span>
              <div class="spice-level-display">
                <span class="spice-level-value">{{ filters.spiceLevel }}</span>
                <span class="spice-level-text">({{ getSpiceLevelText(filters.spiceLevel) }})</span>
                <div class="spice-slider-container">
                  <input 
                    type="range" 
                    v-model="filters.spiceLevel"
                    min="0" 
                    max="5" 
                    step="1"
                    class="spice-slider"
                  >
                </div>
              </div>
            </div>
            
            <!-- 所属食堂 - 标签和下拉框在同一行 -->
            <div class="filter-row-inline">
              <span class="filter-label">{{ $t('canteen') }}</span>
              <select id="hall" class="filter-select-inline" v-model="filters.hall">
                <option value="">{{ $t('allCanteens') }}</option>
                <option value="一食堂">一食堂</option>
                <option value="二食堂">二食堂</option>
                <option value="三食堂">三食堂</option>
                <option value="四食堂">四食堂</option>
              </select>
            </div>
            
            <!-- 底部按钮区域 -->
            <div class="filter-bottom-actions">
              <button class="btn-precise-search" @click="applyFilters">
                <i class="fas fa-search"></i> {{ $t('preciseSearch') }}
              </button>
              <button class="btn-save-preference" @click="savePreferences">
                <i class="fas fa-heart"></i> {{ $t('savePreferences') }}
              </button>
              <button class="btn-load-preference" @click="loadPreferences">
                <i class="fas fa-download"></i> {{ $t('loadPreferences') }}
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- 功能区域 -->
      <section class="features" id="features">
        <div class="container">
          <div class="features-grid">
            <div 
              class="feature-card" 
              v-for="feature in features" 
              :key="feature.id"
              @click="handleFeatureClick(feature.id)"
            >
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
      <section class="recommendation-section" id="ai-assistant">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">{{ $t('aiFoodAssistant') }}</h2>
            <div class="popular-dishes-header">
              <h2 class="section-title">{{ $t('todayHotRecommendations') }}</h2>
              <button class="refresh-btn" @click="refreshRandomDishes" title="刷新随机菜品">
                <i class="fas fa-sync-alt"></i>
              </button>
            </div>
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
                <div class="chat-messages" ref="chatMessages" style="max-height: 300px; overflow-y: auto;">
                  <div class="message ai-message">
                    <div class="message-content">
                      <p>{{ $t('aiAssistantPrompt') }}</p>
                    </div>
                  </div>
                </div>
                
                <div class="chat-input-container">
                  <!-- 用户偏好开关 -->
                  <div class="preference-toggle">
                    <label class="toggle-label">
                      <input 
                        type="checkbox" 
                        v-model="applyUserPreferences"
                        class="toggle-checkbox"
                      >
                      <span class="toggle-slider"></span>
                      <span class="toggle-text">应用保存的偏好限制</span>
                    </label>
                  </div>
                  
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
                      <span class="dish-store">{{ dish.store_name }}({{ dish.canteen }})</span>
                      <span class="dish-wait-time">
                        <i class="fas fa-clock"></i> {{ dish.waitTime }}
                      </span>
                    </div>
                    <div class="dish-tags-actions">
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
                      <button class="dish-btn secondary small" @click.stop="addToFavorites(dish.id)">
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
import { dishesAPI, ordersAPI, userAPI, favoritesAPI  } from '@/services/api'

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
        priceMax: 100,
        crowd: 'any',
        spiceLevel: 0,  // 默认辣度等级为0（不辣）
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
          icon: 'fas fa-fire',
          title: '热门推荐',
          description: '查看今日最受欢迎的菜品，发现校园美食热点'
        },
        {
          id: 3,
          icon: 'fas fa-search',
          title: '精准筛选',
          description: '按品类、口味、价格等多维度筛选菜品'
        },
        {
          id: 4,
          icon: 'fas fa-heart',
          title: '用户收藏',
          description: '管理您收藏的菜品，快速找到心仪美食'
        }
      ],
      aiInput: '',
      applyUserPreferences: true, // 默认应用用户偏好
      exampleQuestions: [
        '我想吃辣的面食，价格实惠的',
        '我赶时间，在一食堂有哪些推荐的菜'
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
    
    // 顶部搜索框搜索 - 跳转到AI对话框
    async handleSearch() {
      if (!this.searchQuery.trim()) return
      
      this.showSuggestions = false
      console.log('顶部搜索框搜索:', this.searchQuery)
      
      // 滚动到AI助手区域
      this.scrollToAIAssistant()
      
      // 设置AI输入框内容
      this.aiInput = this.searchQuery
      
      // 延迟执行AI消息处理，确保滚动完成
      setTimeout(() => {
        this.handleAIMessage()
      }, 500)
    },
    
    // 滚动到AI助手区域
    scrollToAIAssistant() {
      const aiAssistantSection = document.querySelector('.ai-assistant-side')
      if (aiAssistantSection) {
        aiAssistantSection.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        })
      }
    },
    
    // 处理搜索框失去焦点
    handleSearchBlur() {
      setTimeout(() => {
        this.showSuggestions = false
      }, 200)
    },
    
    toggleFlavor(flavor) {
      const index = this.filters.flavors.indexOf(flavor)
      if (index > -1) {
        this.filters.flavors.splice(index, 1)
      } else {
        this.filters.flavors.push(flavor)
      }
    },
    
    // 菜品筛选 - 使用Vue Router跳转
    async applyFilters() {
      console.log('应用筛选条件:', this.filters)
      
      try {
        // 构建查询参数对象
        const queryParams = {
          type: 'filter'
        }
        
        // 添加筛选条件
        if (this.filters.category) queryParams.category = this.filters.category
        if (this.filters.flavors.length > 0) queryParams.tastes = this.filters.flavors.join(',')
        
        // 价格范围：总是发送，让后端处理
        queryParams.price_min = this.filters.priceMin
        queryParams.price_max = this.filters.priceMax
        
        if (this.filters.crowd !== 'any') queryParams.crowd_level = this.filters.crowd
        if (this.filters.spiceLevel !== '') queryParams.spice_level = this.filters.spiceLevel
        if (this.filters.hall) queryParams.hall = this.filters.hall
        if (this.filters.sortBy) queryParams.ordering = this.filters.sortBy
        
        console.log('跳转参数:', queryParams)
        
        // 使用Vue Router进行页面跳转，保持SPA体验
        this.$router.push({
          path: '/search',
          query: queryParams
        })
        
      } catch (error) {
        console.error('跳转失败:', error)
        // 备用方案：使用编程式导航
        this.$router.push('/search')
      }
    },


    
    // 保存用户偏好
    async savePreferences() {
      const currentUser = JSON.parse(localStorage.getItem('currentUser'))
      if (!currentUser) {
        this.showLoginModal = true
        return
      }
      
      try {
        // 构建完整的偏好数据结构
        const preferences = {
          // 品类偏好
          preferred_categories: this.filters.category ? [this.filters.category] : [],
          
          // 口味偏好
          preferred_tastes: this.filters.flavors,
          
          // 价格范围
          price_range_min: this.filters.priceMin,
          price_range_max: this.filters.priceMax,
          
          // 辣度等级
          spice_level: this.filters.spiceLevel,
          
          // 食堂偏好
          preferred_halls: this.filters.hall ? [this.filters.hall] : [],
          
          // 排序偏好
          sort_preference: this.filters.sortBy,
          
          // 人流量偏好
          crowd_preference: this.filters.crowd,
          
          // 饮食限制（暂时为空）
          dietary_restrictions: []
        }
        
        console.log('保存偏好数据:', preferences)
        
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
        priceMax: 100,
        crowd: 'any',
        spiceLevel: 0,  // 重置时也回到0（不辣）
        hall: '',
        sortBy: 'created_at'
      }
    },
    
    // AI智能推荐
    async handleAIMessage() {
      if (!this.aiInput.trim()) return
      
      // 添加用户消息
      this.addMessage(this.aiInput, 'user')
      
      // 显示加载状态
      const loadingMessage = this.addLoadingMessage()
      
      try {
        // 获取当前用户
        const currentUser = JSON.parse(localStorage.getItem('currentUser'))
        const userId = currentUser?.id
        
        console.log('发送AI推荐请求:', this.aiInput, '应用用户偏好:', this.applyUserPreferences, '用户ID:', userId)
        
        const response = await dishesAPI.aiRecommend({
          query: this.aiInput,
          merge_user_preference: this.applyUserPreferences,
          user_id: userId
        })
        
        console.log('AI推荐结果:', response)
        
        // 移除加载消息
        this.removeLoadingMessage(loadingMessage)
        
        if (response.success) {
          // 显示API调用状态
          const apiStatus = response.data.context_data ? '大模型推荐仅供参考' : 'ai连接失败，根据您的要求搜索'
          const aiResponse = this.formatAIResponse(response.data, apiStatus)
          
          // 传递完整的响应数据给消息显示
          const dishes = response.data.dishes || []
          const reasons = response.data.reasons || []
          
          this.addMessage(aiResponse, 'ai', dishes, reasons, apiStatus)
        } else {
          this.addMessage('抱歉，AI推荐服务暂时不可用，请稍后再试。', 'ai')
        }
      } catch (error) {
        console.error('AI推荐失败:', error)
        // 移除加载消息
        this.removeLoadingMessage(loadingMessage)
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
    
    // 添加加载消息
    addLoadingMessage() {
      const chatMessages = this.$refs.chatMessages
      if (!chatMessages) return null
      
      const loadingDiv = document.createElement('div')
      loadingDiv.className = 'message ai-message loading-message'
      loadingDiv.innerHTML = `
        <div class="message-content">
          <div class="loading-indicator">
            <div class="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <p>AI正在思考中...</p>
          </div>
        </div>
      `
      
      chatMessages.appendChild(loadingDiv)
      return loadingDiv
    },
    
    // 移除加载消息
    removeLoadingMessage(loadingMessage) {
      if (loadingMessage && loadingMessage.parentNode) {
        loadingMessage.parentNode.removeChild(loadingMessage)
      }
    },
    
    formatAIResponse(data) {
      console.log('格式化AI响应数据:', data)
      
      // 检查响应类型
      if (data.type === 'chat_response') {
        return data.content
      }
      
      if (data.type === 'recommendation') {
        // 直接返回AI生成的推荐文本，不添加额外的菜品信息
        // 菜品信息会在addMessage方法中单独显示
        return data.content
      }
      
      if (data.type === 'error') {
        return data.content
      }
      
      return '抱歉，AI推荐服务暂时不可用，请稍后再试。'
    },
    
    addMessage(text, type, dishes = null, reasons = [], apiStatus = '') {
      const chatMessages = this.$refs.chatMessages
      if (!chatMessages) return
      
      const messageDiv = document.createElement('div')
      messageDiv.className = `message ${type}-message`
      
      if (type === 'user') {
        messageDiv.innerHTML = `
          <div class="message-content">
            <div class="user-input-container">
              <div class="user-input-icon">
                <i class="fas fa-user"></i>
              </div>
              <div class="user-input-text">
                <p>${text}</p>
              </div>
            </div>
          </div>
        `
      } else {
        let content = `<div class="message-content"><p>${text}</p>`
        
        // 如果有菜品数据，添加简化版菜品展示区域
        if (dishes && dishes.length > 0) {
          content += `
            <div class="ai-dishes-container">
              <div class="ai-dishes-list">
                ${dishes.map((dish, index) => `
                  <div class="ai-dish-item" data-dish-id="${dish.id}">
                    <div class="ai-dish-image" style="background: ${this.getRandomGradient()}">
                      <i class="${this.getDishIcon(dish.category)}"></i>
                    </div>
                    <div class="ai-dish-content">
                      <div class="ai-dish-header">
                        <span class="ai-dish-name">${dish.name}</span>
                        <span class="ai-dish-price">¥${dish.price}</span>
                      </div>
                      <div class="ai-dish-details">
                        <span class="ai-dish-description">${dish.description}</span>
                        <span class="ai-dish-canteen">${dish.canteen || dish.store_name}</span>
                      </div>
                      <div class="ai-dish-reason-actions">
                        <div class="ai-dish-reason">
                          <i class="fas fa-lightbulb"></i> ${reasons && reasons[index] ? reasons[index] : '推荐菜品'}
                        </div>
                        <button class="ai-dish-action-btn ai-favorite-btn">
                          <i class="fas fa-heart"></i> 添加收藏
                        </button>
                      </div>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
          `
        }
        
        // 添加API状态信息（调试用）
        if (apiStatus) {
          content += `<div class="api-status">${apiStatus}</div>`
        }
        
        content += '</div>'
        messageDiv.innerHTML = content
        
        // 添加事件监听器
        if (dishes && dishes.length > 0) {
          const actionButtons = messageDiv.querySelectorAll('.ai-dish-action-btn')
          actionButtons.forEach(button => {
            button.addEventListener('click', (e) => {
              const dishItem = e.target.closest('.ai-dish-item')
              const dishId = dishItem.dataset.dishId
              if (e.target.closest('.ai-order-btn')) {
                this.orderDish(dishId)
              } else if (e.target.closest('.ai-favorite-btn')) {
                this.addToFavorites(dishId)
              }
            })
          })
        }
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
        
        const response = await favoritesAPI.addFavorite({
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
    
    // 加载随机菜品
    async loadRandomDishes() {
      try {
        console.log('加载随机菜品...')
        
        // 调用随机菜品API，默认返回5个菜品
        const response = await dishesAPI.getRandom({ limit: 5 })
        
        console.log('随机菜品结果:', response)
        
        // 后端返回格式: {success: true, data: {dishes: [...]}}
        if (response && response.success && response.data) {
          const dishes = Array.isArray(response.data.dishes) ? response.data.dishes : []
          
          console.log('解析后的随机菜品:', dishes)
          
          this.popularDishes = dishes.map(dish => ({
            ...dish,
            color: this.getRandomGradient(),
            icon: this.getDishIcon(dish.category),
            // 确保有必要的字段
            waitTime: dish.wait_time || '10-15分钟',
            tags: [dish.taste, dish.category].filter(Boolean),
            // 添加商家名称显示
            store_name: dish.store_name || dish.merchant_name || '未知商家'
          }))
        } else {
          console.log('加载随机菜品失败:', response?.message || '未知错误')
        }
      } catch (error) {
        console.error('加载随机菜品失败:', error)
      }
    },
    
    // 刷新随机菜品
    async refreshRandomDishes() {
      console.log('刷新随机菜品...')
      await this.loadRandomDishes()
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
    },

    // 处理功能卡片点击
    handleFeatureClick(featureId) {
      switch (featureId) {
        case 4: // 我的收藏
          this.navigateToFavorites()
          break
        case 1: // 智能菜品推荐
          this.scrollToAIAssistant()
          break
        case 2: // 热门推荐
          this.scrollToPopularDishes()
          break
        case 3: // 精准筛选
          this.scrollToFilterPanel()
          break
        // 其他功能可以添加对应的处理逻辑
        default:
          console.log(`功能 ${featureId} 被点击`)
      }
    },

    // 导航到收藏页面
    navigateToFavorites() {
      const currentUser = JSON.parse(localStorage.getItem('currentUser'))
      if (!currentUser) {
        this.showLoginModal = true
        return
      }
      this.$router.push('/favorites')
    },

    // 滚动到筛选面板
    scrollToFilterPanel() {
      const filterPanel = document.querySelector('.filter-panel')
      if (filterPanel) {
        filterPanel.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        })
      }
    },

    // 滚动到热门菜品区域
    scrollToPopularDishes() {
      const popularDishesSection = document.querySelector('.popular-dishes-side')
      if (popularDishesSection) {
        popularDishesSection.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        })
      }
    },

    // 获取辣度文本描述
    getSpiceLevelText(level) {
      const spiceLevels = {
        0: this.$t('notSpicy'),
        1: this.$t('mildSpicy'),
        2: this.$t('mediumSpicy'),
        3: this.$t('hotSpicy'),
        4: this.$t('extraSpicy'),
        5: this.$t('extremeSpicy')
      }
      return spiceLevels[level] || this.$t('any')
    },

    // 更新价格范围拉选条的CSS变量
    updateRangeSlider() {
      this.$nextTick(() => {
        const rangeSlider = document.querySelector('.range-slider')
        if (rangeSlider) {
          rangeSlider.style.setProperty('--min-value', this.filters.priceMin)
          rangeSlider.style.setProperty('--max-value', this.filters.priceMax)
        }
      })
    },

    // 更新辣度等级拖动条的进度
    updateSpiceSlider() {
      this.$nextTick(() => {
        const spiceSlider = document.querySelector('.spice-slider')
        if (spiceSlider) {
          const value = this.filters.spiceLevel || 0
          const max = 5
          const progress = (value / max) * 100
          spiceSlider.style.setProperty('--slider-progress', `${progress}%`)
        }
      })
    },

    // 读取用户偏好
    async loadPreferences() {
      const currentUser = JSON.parse(localStorage.getItem('currentUser'))
      if (!currentUser) {
        this.showLoginModal = true
        return
      }
      
      try {
        const response = await userAPI.getPreferences()
        
        if (response.success && response.data) {
          const preferences = response.data
          
          // 更新筛选条件
          this.filters.category = preferences.preferred_categories?.[0] || ''
          this.filters.flavors = preferences.preferred_tastes || []
          this.filters.priceMin = preferences.price_range_min || 0
          this.filters.priceMax = preferences.price_range_max || 100
          this.filters.spiceLevel = preferences.spice_level || 0
          this.filters.hall = preferences.preferred_halls?.[0] || ''
          this.filters.sortBy = preferences.sort_preference || 'created_at'
          this.filters.crowd = preferences.crowd_preference || 'any'
          
          // 更新UI组件
          this.updateSpiceSlider()
          
          alert('偏好设置已加载！')
        } else {
          alert('加载偏好失败: ' + (response.message || '没有找到保存的偏好设置'))
        }
      } catch (error) {
        console.error('加载偏好失败:', error)
        alert('加载偏好失败，请检查网络连接')
      }
    }
  },
  mounted() {
    console.log('用户仪表板已加载')
    // 加载随机菜品数据
    this.loadRandomDishes()
    
    // 初始化价格范围拉选条
    this.updateRangeSlider()
    
    // 初始化辣度等级拖动条
    this.updateSpiceSlider()
    
    // 监听价格变化
    this.$watch(
      () => [this.filters.priceMin, this.filters.priceMax],
      () => {
        this.updateRangeSlider()
      },
      { deep: true }
    )
    
    // 监听辣度等级变化
    this.$watch(
      () => this.filters.spiceLevel,
      () => {
        this.updateSpiceSlider()
      },
      { deep: true }
    )
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
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-top: 30px;
}


.features {
  padding: 60px 0 0 0;
  margin: 0;
}

/* 筛选面板头部 */
.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.filter-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 700;
}

/* 小重置按钮 */
.btn-filter-reset-small {
  padding: 6px 12px;
  border: 1px solid #dc3545;
  border-radius: 4px;
  background: white;
  color: #dc3545;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-filter-reset-small:hover {
  background: #dc3545;
  color: white;
  transform: translateY(-1px);
}

/* 底部按钮区域 */
.filter-bottom-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  align-items: center;
}

/* 精确搜索按钮 - 主题红色，与其他按钮一样大 */
.btn-precise-search {
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  background: #e74c3c;
  color: white;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  flex: 1;
  box-shadow: 0 2px 8px rgba(231, 76, 60, 0.3);
}

.btn-precise-search:hover {
  background: #c0392b;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.4);
}

/* 保存偏好按钮 - 文字和图标红色、边框红色、内容白色 */
.btn-save-preference {
  padding: 10px 16px;
  border: 1px solid #e74c3c;
  border-radius: 6px;
  background: white;
  color: #e74c3c;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  justify-content: center;
}

.btn-save-preference:hover {
  background: #e74c3c;
  color: white;
  transform: translateY(-1px);
}

/* 读取偏好按钮 - 文字和图标红色、边框红色、内容白色 */
.btn-load-preference {
  padding: 10px 16px;
  border: 1px solid #e74c3c;
  border-radius: 6px;
  background: white;
  color: #e74c3c;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  justify-content: center;
}

.btn-load-preference:hover {
  background: #e74c3c;
  color: white;
  transform: translateY(-1px);
}

/* 行内布局样式 */
.filter-row-inline {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  padding: 6px 0;
}

.filter-label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
  min-width: 80px;
  flex-shrink: 0;
}

.filter-select-inline {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 0.9rem;
  background: white;
  transition: border-color 0.3s ease;
  max-width: 300px;
}

.filter-select-inline:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

/* 口味标签行内布局 */
.flavor-tags-inline {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  flex: 1;
}

.flavor-tags-inline .flavor-tag {
  padding: 6px 12px;
  border: 1px solid #dee2e6;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.8rem;
  background: white;
  color: #495057;
}

.flavor-tags-inline .flavor-tag:hover {
  border-color: #e74c3c;
  color: #e74c3c;
}

.flavor-tags-inline .flavor-tag.active {
  background: #e74c3c;
  border-color: #e74c3c;
  color: white;
}

/* 价格范围行内布局 */
.price-range-inline {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.price-symbol {
  color: #e74c3c;
  font-weight: bold;
  font-size: 0.9rem;
}

.price-input-inline {
  flex: 1;
  padding: 6px 10px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  font-size: 0.85rem;
  max-width: 120px;
}

.price-input-inline:focus {
  outline: none;
  border-color: #007bff;
}

/* 辣度等级显示样式 */
.spice-level-display {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.spice-level-value {
  font-weight: bold;
  color: #e74c3c;
  font-size: 1rem;
  min-width: 20px;
  text-align: center;
}

.spice-level-text {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
  min-width: 60px;
  margin-left: -8px;
}

.spice-slider-container {
  flex: 1;
  margin: 0;
  position: relative;
  height: 20px;
  display: flex;
  align-items: center;
  max-width: 300px;
}

.spice-slider {
  width: 100%;
  margin: 0;
  height: 6px;
  background: linear-gradient(to right, #e74c3c 0%, #e74c3c var(--slider-progress, 0%), #e9ecef var(--slider-progress, 0%), #e9ecef 100%);
  border-radius: 3px;
  outline: none;
  position: relative;
  z-index: 1;
}

.spice-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #e74c3c;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 2;
}

.spice-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #e74c3c;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  border: none;
  position: relative;
  z-index: 2;
}

.spice-slider::-webkit-slider-track {
  width: 100%;
  height: 6px;
  background: transparent;
  border-radius: 3px;
  border: none;
}

.spice-slider::-moz-range-track {
  width: 100%;
  height: 6px;
  background: transparent;
  border-radius: 3px;
  border: none;
}

/* 辣度筛选行内布局 */
.spice-level-inline {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.spice-slider-inline {
  flex: 1;
  margin: 0;
}

.spice-level-text {
  font-weight: 600;
  color: #e74c3c;
  font-size: 0.9rem;
  min-width: 60px;
  text-align: center;
}

/* 压缩布局样式 */
.filter-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
  align-items: flex-start;
}

.filter-group.compact {
  flex: 1;
  margin-bottom: 0;
}

.filter-group.compact label,
.filter-group.compact span {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
}

/* 价格范围紧凑布局 */
.price-range-compact {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.price-range-compact .range-inputs {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 0;
}

.price-range-compact .range-inputs input {
  flex: 1;
  padding: 6px 10px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  font-size: 0.85rem;
}

.price-range-compact .price-display {
  text-align: center;
  font-weight: bold;
  color: #e74c3c;
  font-size: 0.85rem;
  margin-top: 0;
}

/* 辣度筛选紧凑布局 */
.spice-level-compact {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: 0;
}

.spice-level-compact .spice-slider {
  width: 100%;
  margin: 0;
}

.spice-level-compact .spice-value {
  text-align: center;
  font-weight: bold;
  color: #e74c3c;
  margin-top: 0;
  font-size: 0.85rem;
}

/* 口味标签紧凑布局 */
.flavor-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 6px;
}

.flavor-tag {
  padding: 4px 10px;
  border: 1px solid #dee2e6;
  border-radius: 16px;
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

/* AI聊天框菜品展示样式 */
.ai-dishes-container {
  margin-top: 8px;
  border-top: 1px solid #e9ecef;
  padding-top: 8px;
}

.ai-dishes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin-top: 10px;
}

.ai-dish-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
}

.ai-dish-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.ai-dish-image {
  height: 120px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.ai-dish-rating {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.7);
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 4px;
}

.ai-dish-image i {
  font-size: 2rem;
  opacity: 0.9;
}

.ai-dish-info {
  padding: 16px;
}

.ai-dish-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.ai-dish-price {
  font-size: 1.2rem;
  font-weight: bold;
  color: #e74c3c;
  margin: 0 0 8px 0;
}

.ai-dish-description {
  font-size: 0.9rem;
  color: #6c757d;
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.ai-dish-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}

.ai-dish-taste {
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.ai-dish-canteen {
  color: #6c757d;
  font-size: 0.8rem;
  font-weight: 500;
}

.ai-dish-actions {
  display: flex;
  gap: 8px;
}

.ai-dish-btn {
  flex: 1;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.ai-order-btn {
  background: #28a745;
  color: white;
}

.ai-order-btn:hover {
  background: #1e7e34;
  transform: translateY(-1px);
}

.ai-favorite-btn {
  background: #6c757d;
  color: white;
}

.ai-favorite-btn:hover {
  background: #545b62;
  transform: translateY(-1px);
}

/* 简化版AI聊天框菜品展示样式 */
.ai-dishes-container {
  margin-top: 8px;
  border-top: 1px solid #e9ecef;
  padding-top: 8px;
}

.ai-dishes-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ai-dish-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.ai-dish-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.ai-dish-image {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.ai-dish-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.ai-dish-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.ai-dish-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.ai-dish-price {
  font-size: 0.95rem;
  font-weight: bold;
  color: #e74c3c;
  margin: 0;
}

.ai-dish-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: #6c757d;
}

.ai-dish-description {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0;
}

.ai-dish-canteen {
  background: #f8f9fa;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  color: #495057;
  margin-left: 8px;
}

/* AI对话框中的推荐理由和收藏按钮在同一行的样式 */
.ai-dish-reason-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-top: 4px;
}

.ai-dish-reason {
  font-size: 0.7rem;
  color: #28a745;
  background: #f0fff4;
  padding: 3px 6px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 3px;
  border-left: 2px solid #28a745;
  flex: 1;
  max-width: 70%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ai-dish-reason i {
  color: #28a745;
  font-size: 0.65rem;
}

.ai-dish-action-btn {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  font-size: 0.7rem;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}

.ai-favorite-btn {
  background: #e74c3c;
  color: white;
  box-shadow: 0 1px 3px rgba(231, 76, 60, 0.3);
}

.ai-favorite-btn:hover {
  background: #c0392b;
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(231, 76, 60, 0.4);
}

/* 用户输入框样式 */
.user-input-container {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 12px;
  padding: 12px 16px;
  margin: 8px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.user-input-icon {
  width: 32px;
  height: 32px;
  background: #007bff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.user-input-text {
  flex: 1;
}

.user-input-text p {
  margin: 0;
  color: #2c3e50;
  font-weight: 500;
  line-height: 1.4;
}

/* API状态信息样式 */
.api-status {
  font-size: 0.7rem;
  color: #6c757d;
  text-align: right;
  margin-top: 4px;
  padding: 2px 8px;
  background: rgba(108, 117, 125, 0.1);
  border-radius: 4px;
  display: inline-block;
  max-width: 100%;
  word-wrap: break-word;
  box-sizing: border-box;
}

/* AI消息容器样式 */
.message.ai-message .message-content {
  position: relative;
  padding-bottom: 8px; /* 为状态信息预留空间 */
}

.message.ai-message .message-content > p {
  margin-bottom: 4px;
}

/* 热门菜品标题和刷新按钮样式 */
.popular-dishes-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.refresh-btn {
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(231, 76, 60, 0.3);
}

.refresh-btn:hover {
  background: #c0392b;
  transform: rotate(180deg);
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.4);
}

.refresh-btn i {
  font-size: 0.9rem;
}

/* 商家名称样式 */
.dish-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 8px 0;
  font-size: 0.85rem;
  color: #6c757d;
}

.dish-store {
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 8px;
  border-radius: 12px;
  font-weight: 500;
  font-size: 0.8rem;
}

.dish-wait-time {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #6c757d;
}

/* 口味标签和收藏按钮在同一行的样式 */
.dish-tags-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin: 8px 0;
}

.dish-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  flex: 1;
}

.dish-tag {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
}

.dish-tag.spicy {
  background: #ffe6e6;
  color: #d63031;
}

.dish-tag.cheap {
  background: #e6f7ff;
  color: #1890ff;
}

.dish-tag:not(.spicy):not(.cheap) {
  background: #f8f9fa;
  color: #6c757d;
}

/* 缩小收藏按钮样式 */
.dish-btn.small {
  padding: 6px 12px;
  font-size: 0.75rem;
  min-width: auto;
  white-space: nowrap;
  flex-shrink: 0;
}

.dish-btn.secondary.small {
  background: #e74c3c;
  color: white;
  border: none;
  box-shadow: 0 2px 4px rgba(231, 76, 60, 0.3);
}

.dish-btn.secondary.small:hover {
  background: #c0392b;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(231, 76, 60, 0.4);
}

/* 用户偏好开关样式 */
.preference-toggle {
  margin-bottom: 12px;
  padding: 8px 0;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-size: 0.9rem;
  color: #2c3e50;
  font-weight: 500;
}

.toggle-checkbox {
  display: none;
}

.toggle-slider {
  position: relative;
  width: 44px;
  height: 22px;
  background-color: #ccc;
  border-radius: 22px;
  transition: background-color 0.3s ease;
}

.toggle-slider:before {
  content: '';
  position: absolute;
  width: 18px;
  height: 18px;
  left: 2px;
  top: 2px;
  background-color: white;
  border-radius: 50%;
  transition: transform 0.3s ease;
}

.toggle-checkbox:checked + .toggle-slider {
  background-color: #e74c3c;
}

.toggle-checkbox:checked + .toggle-slider:before {
  transform: translateX(22px);
}

.toggle-text {
  font-size: 0.85rem;
  color: #495057;
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
  
  .ai-dishes-grid {
    grid-template-columns: 1fr;
  }
  
  .ai-dish-actions {
    flex-direction: column;
  }
  
  .popular-dishes-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .refresh-btn {
    align-self: flex-start;
  }
  
  .dish-meta {
    flex-wrap: wrap;
    gap: 8px;
  }
}
</style>
