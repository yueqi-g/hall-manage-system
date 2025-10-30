<template>
  <div class="search-results-page">
    <AppHeader />
    
    <!-- 搜索头部 -->
    <section class="search-header">
      <div class="container">
        <div class="back-btn" @click="$router.go(-1)">
          <i class="fas fa-arrow-left"></i>
          返回
        </div>
        <div class="search-info">
          <h1 id="searchTitle">{{ searchTitle }}</h1>
          <p id="searchSummary" class="search-summary">{{ searchSummary }}</p>
        </div>
      </div>
    </section>

    <main class="search-results">
      <div class="container">
        <!-- 筛选侧边栏 -->
        <aside class="search-sidebar">
          <div class="filter-section">
            <h3>筛选条件</h3>
            
            <!-- 品类筛选 -->
            <div class="filter-group">
              <label>品类</label>
              <select v-model="filters.category" class="filter-select">
                <option value="">全部品类</option>
                <option value="饭">饭</option>
                <option value="面">面</option>
                <option value="饺子">饺子</option>
                <option value="其他">其他</option>
              </select>
            </div>
            
            <!-- 口味偏好筛选 -->
            <div class="filter-group">
              <label>口味偏好</label>
              <div class="flavor-tags">
                <span 
                  v-for="flavor in flavorOptions" 
                  :key="flavor.value"
                  class="flavor-tag" 
                  :class="{ active: filters.flavors.includes(flavor.value) }"
                  @click="toggleFlavor(flavor.value)"
                >
                  {{ flavor.label }}
                </span>
              </div>
            </div>
            
            <!-- 价格范围筛选 -->
            <div class="filter-group">
              <label>价格范围</label>
              <div class="range-inputs">
                <input 
                  type="number" 
                  placeholder="最低价" 
                  min="0" 
                  max="100"
                  v-model.number="filters.priceMin"
                  class="price-input"
                >
                <span class="range-separator">-</span>
                <input 
                  type="number" 
                  placeholder="最高价" 
                  min="0" 
                  max="100"
                  v-model.number="filters.priceMax"
                  class="price-input"
                >
              </div>
              <div class="price-display">¥{{ filters.priceMin || 0 }} - ¥{{ filters.priceMax || 100 }}</div>
            </div>
            
            <!-- 辣度筛选 -->
            <div class="filter-group">
              <label>最大辣度等级</label>
              <div class="spice-level-filter">
                <input 
                  type="range" 
                  v-model.number="filters.spiceLevel"
                  min="0" 
                  max="5" 
                  step="1"
                  class="spice-slider"
                >
                <div class="spice-labels">
                  <span>0</span>
                  <span>1</span>
                  <span>2</span>
                  <span>3</span>
                  <span>4</span>
                  <span>5</span>
                </div>
                <div class="spice-value">
                  {{ filters.spiceLevel === '' ? '不限' : `辣度 ≤ ${filters.spiceLevel}` }}
                </div>
              </div>
            </div>
            
            <!-- 人流量筛选 -->
            <div class="filter-group">
              <label>人流量（食堂筛选）</label>
              <div class="crowd-level">
                <div class="crowd-option">
                  <input 
                    type="radio" 
                    id="crowd-any" 
                    value="any"
                    v-model="filters.crowd"
                  >
                  <label for="crowd-any">不限</label>
                </div>
                <div class="crowd-option">
                  <input 
                    type="radio" 
                    id="crowd-low" 
                    value="low"
                    v-model="filters.crowd"
                  >
                  <label for="crowd-low">人少</label>
                </div>
                <div class="crowd-option">
                  <input 
                    type="radio" 
                    id="crowd-medium" 
                    value="medium"
                    v-model="filters.crowd"
                  >
                  <label for="crowd-medium">适中</label>
                </div>
                <div class="crowd-option">
                  <input 
                    type="radio" 
                    id="crowd-high" 
                    value="high"
                    v-model="filters.crowd"
                  >
                  <label for="crowd-high">人多</label>
                </div>
              </div>
            </div>
            
            <!-- 食堂筛选 -->
            <div class="filter-group">
              <label>食堂选择</label>
              <select v-model="filters.hall" class="filter-select">
                <option value="">全部食堂</option>
                <option value="一食堂">一食堂</option>
                <option value="二食堂">二食堂</option>
                <option value="三食堂">三食堂</option>
                <option value="四食堂">四食堂</option>
              </select>
            </div>
            
            <!-- 排序方式 -->
            <div class="filter-group">
              <label>排序方式</label>
              <select v-model="sortBy" class="filter-select">
                <option value="default">默认排序</option>
                <option value="price">价格从低到高</option>
                <option value="-price">价格从高到低</option>
                <option value="-rating">评分最高</option>
                <option value="created_at">最新上架</option>
              </select>
            </div>
            
            <div class="filter-actions">
              <button class="btn-apply-filter" @click="applyResultFilters">
                <i class="fas fa-search"></i> 应用筛选
              </button>
              <button class="btn-reset-filter" @click="resetFilters">
                <i class="fas fa-undo"></i> 重置
              </button>
            </div>
            
            <!-- 用户偏好按钮 -->
            <div class="preference-actions">
              <button class="btn-save-preference" @click="savePreferences">
                <i class="fas fa-heart"></i> 保存偏好
              </button>
              <button class="btn-load-preference" @click="loadPreferences">
                <i class="fas fa-download"></i> 读取偏好
              </button>
            </div>
          </div>
        </aside>

        <!-- 结果列表 -->
        <section class="results-main">
          <div class="results-header">
            <div class="results-count">
              找到 <span id="resultsCount">{{ searchResults.length }}</span> 个结果
            </div>
            <div class="view-options">
              <button 
                class="view-btn" 
                :class="{ active: currentView === 'grid' }" 
                data-view="grid"
                @click="switchView('grid')"
              >
                <i class="fas fa-th"></i>
              </button>
              <button 
                class="view-btn" 
                :class="{ active: currentView === 'list' }" 
                data-view="list"
                @click="switchView('list')"
              >
                <i class="fas fa-list"></i>
              </button>
            </div>
          </div>

          <!-- 结果容器 -->
          <div class="results-container" :class="currentView === 'grid' ? 'results-grid' : 'results-list'" id="resultsContainer">
            <!-- 网格视图 -->
            <div v-if="currentView === 'grid'" class="results-grid">
              <div 
                v-for="dish in searchResults" 
                :key="dish.id"
                class="result-item"
                :data-dish-id="dish.id"
                :class="{ highlighted: highlightedDishId === dish.id }"
              >
                <div class="result-image" :style="{ background: getDishColor(dish.id) }">
                  <i :class="getDishIcon(dish.id)"></i>
                  <div class="result-rating">
                    <i class="fas fa-star"></i> {{ dish.rating }}
                  </div>
                </div>
                <div class="result-content">
                  <!-- 第一行：菜品名称和价格 -->
                  <div class="result-header">
                    <h3 class="result-name">{{ dish.name }}</h3>
                    <div class="result-price">¥{{ dish.price }}</div>
                  </div>
                  
                  <!-- 第二行：等待时间和所属食堂 -->
                  <div class="result-meta">
                    <span class="result-wait-time">
                      <i class="fas fa-clock"></i> {{ dish.wait_time || dish.waitTime }}分钟
                    </span>
                    <span class="result-canteen">
                      <i class="fas fa-store"></i> {{ dish.canteen }}<span v-if="dish.store_name"> - {{ dish.store_name }}</span>
                    </span>
                  </div>
                  
                  <!-- 第三、四行：描述和标签（左半边） + 收藏按钮（右半边） -->
                  <div class="result-bottom-section">
                    <div class="result-left-content">
                      <!-- 第三行：描述 -->
                      <p class="result-description">{{ dish.description }}</p>
                      
                      <!-- 第四行：标签 -->
                      <div class="result-tags">
                        <span 
                          v-for="tag in getDishTags(dish)" 
                          :key="tag"
                          class="result-tag"
                          :class="{ spicy: tag === '辣' || tag === '麻辣' }"
                        >
                          {{ tag }}
                        </span>
                      </div>
                    </div>
                    <div class="result-actions">
                      <button class="btn-favorite-large" @click.stop="addToFavorites(dish.id)">
                        <i class="fas fa-heart"></i> 收藏
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 列表视图 -->
            <div v-else class="results-list">
              <div 
                v-for="dish in searchResults" 
                :key="dish.id"
                class="result-item-simple"
              >
                <div class="simple-item-header">
                  <div class="simple-item-icon" :style="{ background: getDishColor(dish.id) }">
                    <i :class="getDishIcon(dish.id)"></i>
                  </div>
                  <div class="simple-item-info">
                    <div class="simple-item-main">
                      <h4 class="simple-item-name">{{ dish.name }}</h4>
                      <span class="simple-item-merchant">{{ dish.merchant }}</span>
                    </div>
                    <div class="simple-item-details">
                      <span class="simple-item-price">¥{{ dish.price }}</span>
                      <span class="simple-item-rating">
                        <i class="fas fa-star"></i> {{ dish.rating }}
                      </span>
                      <span class="simple-item-wait">
                        <i class="fas fa-clock"></i> {{ dish.wait_time || dish.waitTime }}分钟
                      </span>
                    </div>
                  </div>
                  <div class="simple-item-actions">
                    <button class="btn-simple-primary" @click.stop="switchToGridViewAndHighlight(dish.id)">查看详情</button>
                  </div>
                </div>
                <div class="simple-item-footer">
                  <div class="simple-item-tags">
                    <span 
                      v-for="tag in getDishTags(dish)" 
                      :key="tag"
                      class="simple-tag"
                    >
                      {{ tag }}
                    </span>
                  </div>
                  <div class="simple-item-canteen">
                    <i class="fas fa-store"></i> {{ dish.canteen }}<span v-if="dish.store_name"> - {{ dish.store_name }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 无结果提示 -->
          <div class="no-results" v-if="!loading && searchResults.length === 0">
            <i class="fas fa-search"></i>
            <h3>没有找到相关结果</h3>
            <p>请尝试调整搜索条件或筛选条件</p>
            <button class="btn-primary" @click="$router.push('/user/dashboard')">返回首页</button>
          </div>

          <!-- 分页 -->
          <div class="pagination" v-if="searchResults.length > 0">
            <!-- 分页组件可以根据需要实现 -->
          </div>
        </section>
      </div>
    </main>
    
    <AppFooter />
    <LoginModal v-if="showLoginModal" @close="showLoginModal = false" />
  </div>
</template>

<script>
import AppHeader from '@/components/Header.vue'
import AppFooter from '@/components/Footer.vue'
import LoginModal from '@/components/LoginModal.vue'
import { dishesAPI, userAPI, favoritesAPI } from '@/services/api'

export default {
  name: 'SearchResults',
  components: {
    AppHeader,
    AppFooter,
    LoginModal
  },
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      loading: false,
      showLoginModal: false,
      currentView: 'grid', // grid 或 list
      highlightedDishId: null,
      
      // 搜索相关
      searchTitle: '搜索结果',
      searchSummary: '',
      sortBy: 'default',
      
      // 筛选条件
      filters: {
        category: '',
        flavors: [],
        priceMin: 0,
        priceMax: 100,
        crowd: 'any',
        spiceLevel: '',
        hall: ''
      },
      
      // 口味选项
      flavorOptions: [
        { value: '辣', label: '辣' },
        { value: '咸', label: '咸' },
        { value: '淡', label: '淡' },
        { value: '酸甜', label: '酸甜' }
      ]
    }
  },
  computed: {
    hasActiveFilters() {
      return this.filters.category || 
             this.filters.flavors.length > 0 || 
             this.filters.priceMin > 0 || 
             this.filters.priceMax < 50 ||
             this.filters.crowd !== 'any' ||
             this.filters.spiceLevel !== '' ||
             this.filters.hall !== ''
    }
  },
  methods: {
    // 初始化搜索页面
    initSearchPage() {
      const query = this.$route.query
      const searchType = query.type
      
      console.log('SearchResults - 接收到的URL参数:', query)
      
      if (searchType === 'keyword') {
        this.searchQuery = query.q || ''
        this.displayKeywordResults(this.searchQuery)
        
        // 关键词搜索也可能带有筛选条件
        if (query.price_min) this.filters.priceMin = Number(query.price_min)
        if (query.price_max) this.filters.priceMax = Number(query.price_max)
        if (query.spice_level) this.filters.spiceLevel = query.spice_level
        if (query.crowd_level) this.filters.crowd = query.crowd_level
        if (query.hall) this.filters.hall = query.hall
      } else if (searchType === 'filter') {
        // 筛选搜索，从URL读取所有筛选条件
        this.filters = {
          category: query.category || '',
          flavors: query.tastes ? query.tastes.split(',') : [],
          priceMin: query.price_min ? Number(query.price_min) : 0,
          priceMax: query.price_max ? Number(query.price_max) : 100,
          crowd: query.crowd_level || 'any',
          spiceLevel: query.spice_level || '',
          hall: query.hall || ''
        }
        
        // 读取排序方式
        if (query.ordering) {
          this.sortBy = query.ordering
        }
        
        console.log('SearchResults - 解析后的筛选条件:', this.filters)
        
        this.displayFilterResults(this.filters)
      }
      
      this.performSearch()
    },
    
    // 显示关键词搜索结果信息
    displayKeywordResults(query) {
      this.searchTitle = `搜索："${query}"`
      this.searchSummary = '根据您的搜索关键词找到的相关菜品'
    },
    
    // 显示筛选搜索结果信息
    displayFilterResults(filters) {
      this.searchTitle = '精确筛选结果'
      
      let summary = '筛选条件：'
      const conditions = []
      
      // 品类筛选条件
      if (filters.category) {
        conditions.push(`品类：${filters.category}`)
      }
      
      // 口味偏好筛选条件
      if (filters.flavors.length > 0) {
        conditions.push(`口味：${filters.flavors.join('、')}`)
      }
      
      // 价格范围筛选条件
      if (filters.priceMin > 0 || filters.priceMax < 100) {
        conditions.push(`价格：¥${filters.priceMin || 0}-¥${filters.priceMax || 100}`)
      }
      
      // 辣度等级筛选条件
      if (filters.spiceLevel !== '') {
        const spiceText = this.getSpiceLevelText(filters.spiceLevel)
        conditions.push(`辣度：${spiceText}`)
      }
      
      // 人流量筛选条件
      if (filters.crowd && filters.crowd !== 'any') {
        conditions.push(`人流量：${this.getCrowdName(filters.crowd)}`)
      }
      
      // 食堂筛选条件
      if (filters.hall) {
        conditions.push(`食堂：${filters.hall}`)
      }
      
      // 排序方式
      if (this.sortBy && this.sortBy !== 'default') {
        const sortText = this.getSortText(this.sortBy)
        conditions.push(`排序：${sortText}`)
      }
      
      this.searchSummary = summary + conditions.join('，')
    },
    
    // 执行搜索
    async performSearch() {
      this.loading = true
      
      try {
        const searchType = this.$route.query.type
        let response
        
        // 构建通用参数
        const params = {
          ordering: this.sortBy || 'default',
          price_min: this.filters.priceMin,
          price_max: this.filters.priceMax
        }
        
        // 添加可选筛选条件
        if (this.filters.spiceLevel !== '') params.spice_level = this.filters.spiceLevel
        if (this.filters.crowd !== 'any') params.crowd_level = this.filters.crowd
        if (this.filters.hall) params.hall = this.filters.hall
        if (this.filters.category) params.category = this.filters.category
        if (this.filters.flavors.length > 0) params.tastes = this.filters.flavors.join(',')
        
        console.log('SearchResults - 执行搜索，参数:', params)
        
        if (searchType === 'keyword') {
          // 关键词搜索
          params.q = this.searchQuery
          response = await dishesAPI.search(params)
        } else {
          // 筛选搜索
          response = await dishesAPI.filter(params)
        }
        
        console.log('SearchResults - 搜索响应:', response)
        
        if (response.success) {
          this.searchResults = response.data.dishes || []
          console.log(`SearchResults - 找到 ${this.searchResults.length} 个结果`)
        } else {
          console.error('搜索失败:', response.message)
          this.searchResults = []
        }
      } catch (error) {
        console.error('搜索错误:', error)
        this.searchResults = []
      } finally {
        this.loading = false
      }
    },
    
    // 模拟数据（备用）
    getMockResults() {
      return [
        {
          id: 1,
          name: "麻辣香锅",
          merchant: "第二食堂 - 川味小厨",
          price: 22,
          rating: 4.8,
          description: "香辣可口，配料丰富，多种食材任你选择。采用四川正宗调料，麻辣鲜香，回味无穷。",
          canteen: "第二食堂",
          waitTime: "10-15分钟",
          tags: ["辣", "推荐", "麻辣", "香锅"],
          category: "hotpot"
        },
        {
          id: 2,
          name: "重庆小面",
          merchant: "第一食堂 - 面食之家",
          price: 15,
          rating: 4.6,
          description: "正宗重庆风味，面条劲道，汤底浓郁，麻辣鲜香。配以特制肉酱和花生碎，味道层次丰富。",
          canteen: "第一食堂",
          waitTime: "5-8分钟",
          tags: ["辣", "面食", "重庆风味"],
          category: "noodle"
        }
      ]
    },
    
    // 切换视图
    switchView(viewType) {
      this.currentView = viewType
    },
    
    // 切换到网格视图并高亮指定菜品
    switchToGridViewAndHighlight(dishId) {
      this.currentView = 'grid'
      this.highlightedDishId = dishId
      
      // 滚动到对应位置
      this.$nextTick(() => {
        const element = document.querySelector(`[data-dish-id="${dishId}"]`)
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
      })
    },
    
    // 应用筛选
    applyResultFilters() {
      console.log('SearchResults - 应用筛选条件:', {
        filters: this.filters,
        sortBy: this.sortBy
      })
      this.performSearch()
    },
    
    // 切换口味选择
    toggleFlavor(flavor) {
      const index = this.filters.flavors.indexOf(flavor)
      if (index > -1) {
        this.filters.flavors.splice(index, 1)
      } else {
        this.filters.flavors.push(flavor)
      }
    },
    
    // 重置筛选
    resetFilters() {
      this.filters = {
        category: '',
        flavors: [],
        priceMin: 0,
        priceMax: 100,
        crowd: 'any',
        spiceLevel: '',
        hall: ''
      }
      this.sortBy = 'default'
      console.log('SearchResults - 重置筛选条件')
      this.performSearch()
    },
    
    // 获取菜品图标
    getDishIcon(dishId) {
      const iconMap = {
        1: 'fa-pepper-hot',
        2: 'fa-bacon',
        3: 'fa-fish',
        4: 'fa-egg',
        5: 'fa-drumstick-bite',
        6: 'fa-utensils'
      }
      return `fas ${iconMap[dishId] || 'fa-utensils'}`
    },
    
    // 获取菜品颜色
    getDishColor(dishId) {
      const colorMap = {
        1: '#ff6b6b',
        2: '#a1c4fd',
        3: '#4ecdc4',
        4: '#fad0c4',
        5: '#ff9a9e',
        6: '#a1c4fd'
      }
      return `linear-gradient(45deg, ${colorMap[dishId] || '#ffecd2'}, #fbc2eb)`
    },
    
    // 工具函数
    getCategoryName(category) {
      const categoryMap = {
        'rice': '米饭类',
        'noodle': '面食类',
        'snack': '小吃类',
        'drink': '饮品类',
        'breakfast': '早餐类',
        'hotpot': '火锅类'
      }
      return categoryMap[category] || category
    },
    
    getFlavorName(flavor) {
      const flavorMap = {
        'spicy': '辣',
        'sour': '酸',
        'sweet': '甜',
        'salty': '咸',
        'light': '清淡',
        'heavy': '重口味'
      }
      return flavorMap[flavor] || flavor
    },
    
    getCrowdName(crowd) {
      const crowdMap = {
        'low': '稀少',
        'medium': '适中',
        'high': '拥挤'
      }
      return crowdMap[crowd] || crowd
    },
    
    // 获取辣度等级文本描述
    getSpiceLevelText(level) {
      const spiceLevels = {
        0: '不辣',
        1: '微辣',
        2: '中辣',
        3: '辣',
        4: '特辣',
        5: '变态辣'
      }
      return spiceLevels[level] || `辣度 ≤ ${level}`
    },
    
    // 获取排序方式文本描述
    getSortText(sortBy) {
      const sortMap = {
        'default': '默认排序',
        'price': '价格从低到高',
        '-price': '价格从高到低',
        '-rating': '评分最高',
        'created_at': '最新上架'
      }
      return sortMap[sortBy] || sortBy
    },
    
    // 下单
    async orderDish(dishId) {
      const currentUser = JSON.parse(localStorage.getItem('currentUser'))
      if (!currentUser) {
        this.showLoginModal = true
        return
      }
      
      try {
        const response = await dishesAPI.createOrder({
          dishId: dishId,
          quantity: 1
        })
        
        if (response.success) {
          alert(`下单成功！订单号: ${response.data.orderId}`)
        } else {
          alert('下单失败: ' + (response.message || '未知错误'))
        }
      } catch (error) {
        console.error('下单失败:', error)
        alert('下单失败，请检查网络连接')
      }
    },
    
    // 收藏
    async addToFavorites(dishId) {
      const currentUser = JSON.parse(localStorage.getItem('currentUser'))
      if (!currentUser) {
        this.showLoginModal = true
        return
      }
      
      try {
        const response = await favoritesAPI.addFavorite({
          dishId: dishId
        })
        
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
          sort_preference: this.sortBy,
          
          // 人流量偏好
          crowd_preference: this.filters.crowd,
          
          // 饮食限制（暂时为空）
          dietary_restrictions: []
        }
        
        console.log('SearchResults - 保存偏好数据:', preferences)
        
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
          this.filters.spiceLevel = preferences.spice_level || ''
          this.filters.hall = preferences.preferred_halls?.[0] || ''
          this.sortBy = preferences.sort_preference || 'default'
          this.filters.crowd = preferences.crowd_preference || 'any'
          
          alert('偏好设置已加载！')
        } else {
          alert('加载偏好失败: ' + (response.message || '没有找到保存的偏好设置'))
        }
      } catch (error) {
        console.error('加载偏好失败:', error)
        alert('加载偏好失败，请检查网络连接')
      }
    },
    
    // 获取菜品标签
    getDishTags(dish) {
      const tags = []
      
      // 从taste字段添加口味标签
      if (dish.taste) {
        tags.push(dish.taste)
      }
      
      // 从category字段添加品类标签
      if (dish.category) {
        tags.push(dish.category)
      }
      
      // 根据辣度等级添加辣度标签
      if (dish.spice_level > 0) {
        const spiceLevels = ['微辣', '中辣', '辣', '特辣', '变态辣']
        if (dish.spice_level <= spiceLevels.length) {
          tags.push(spiceLevels[dish.spice_level - 1])
        } else {
          tags.push('辣')
        }
      }
      
      // 如果评分高，添加推荐标签
      if (dish.rating >= 4.5) {
        tags.push('高分')
      }
      
      // 如果等待时间小于2分钟，添加快速标签
      if (dish.wait_time && dish.wait_time <= 2) {
        tags.push('快速')
      }
      
      return tags
    }
  },
  mounted() {
    this.initSearchPage()
  }
}
</script>

<style scoped>
/* 搜索头部样式 */
.search-header {
  background: linear-gradient(135deg,rgb(242, 188, 205) 50%,rgb(232, 204, 232) 100%);
  color: white;
  padding: 30px 0;
}

.search-header .container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.search-info h1 {
  margin: 0 0 8px 0;
  font-size: 2rem;
  font-weight: 700;
}

.search-summary {
  margin: 0;
  opacity: 0.9;
  font-size: 1rem;
}

/* 主内容区域 */
.search-results {
  padding: 30px 0;
  min-height: 80vh;
}

.container {
  display: flex;
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 筛选侧边栏 */
.search-sidebar {
  width: 280px;
  flex-shrink: 0;
}

.filter-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.filter-section h3 {
  margin: 0 0 20px 0;
  font-size: 1.2rem;
  color: #333;
  border-bottom: 2px solid #e74c3c;
  padding-bottom: 8px;
}

.filter-group {
  margin-bottom: 20px;
}

.filter-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #555;
}

.filter-select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
}

.canteen-checkboxes {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.canteen-checkboxes label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: normal;
  cursor: pointer;
}

.filter-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.btn-apply-filter,
.btn-reset-filter {
  width: 100%;
  border: none;
  padding: 12px;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-weight: 600;
}

.btn-apply-filter {
  background: #e74c3c;
  color: white;
}

.btn-apply-filter:hover {
  background: #c0392b;
  transform: translateY(-1px);
}

.btn-reset-filter {
  background: #6c757d;
  color: white;
}

.btn-reset-filter:hover {
  background: #545b62;
  transform: translateY(-1px);
}

/* 价格范围筛选样式 */
.range-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
}

.price-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
}

.range-separator {
  color: #6c757d;
  font-weight: bold;
}

.price-display {
  text-align: center;
  font-weight: bold;
  color: #e74c3c;
  margin-top: 8px;
  font-size: 0.95rem;
}

/* 辣度筛选样式 */
.spice-level-filter {
  margin-top: 8px;
}

.spice-slider {
  width: 100%;
  margin: 10px 0;
  cursor: pointer;
}

.spice-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #6c757d;
  margin-top: 5px;
}

.spice-value {
  text-align: center;
  font-weight: bold;
  color: #e74c3c;
  margin-top: 8px;
  font-size: 0.9rem;
}

/* 人流量筛选样式 */
.crowd-level {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
}

.crowd-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.crowd-option input[type="radio"] {
  margin: 0;
  cursor: pointer;
}

.crowd-option label {
  margin: 0;
  cursor: pointer;
  font-weight: normal;
  color: #555;
}

/* 结果主区域 */
.results-main {
  flex: 1;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.results-count {
  font-size: 1.1rem;
  color: #666;
}

.results-count span {
  font-weight: 700;
  color: #e74c3c;
}

.view-options {
  display: flex;
  gap: 5px;
  background: #f8f9fa;
  padding: 4px;
  border-radius: 8px;
}

.view-btn {
  padding: 8px 12px;
  border: none;
  background: none;
  cursor: pointer;
  border-radius: 6px;
  color: #666;
  transition: all 0.3s ease;
}

.view-btn.active {
  background: white;
  color: #e74c3c;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 网格视图 */
.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.result-item {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.result-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.result-item.highlighted {
  border: 2px solid #e74c3c;
  transform: scale(1.02);
}

.result-image {
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: white;
  position: relative;
}

.result-rating {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.9);
  padding: 4px 8px;
  border-radius: 15px;
  font-weight: 600;
  color: #e74c3c;
  font-size: 0.8rem;
}

.result-content {
  padding: 12px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.result-name {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  flex: 1;
}

.result-price {
  font-size: 1.3rem;
  font-weight: 700;
  color: #e74c3c;
  margin-left: 10px;
}

/* 第二行：等待时间和所属食堂 */
.result-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
  font-size: 0.85rem;
  color: #888;
}

.result-wait-time,
.result-canteen {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 第三、四行：描述和标签（左半边） + 收藏按钮（右半边） */
.result-bottom-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 15px;
  min-height: 40px;
}

.result-left-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.result-description {
  margin: 0;
  font-size: 0.85rem;
  color: #666;
  line-height: 1.3;
  min-height: 20px;
}

.result-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin: 0;
}

.result-tag {
  background: #f8f9fa;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  color: #666;
}

.result-tag.spicy {
  background: #ffe8e6;
  color: #e74c3c;
}

.result-actions {
  flex-shrink: 0;
  display: flex;
  align-items: flex-start;
}

.result-name {
  margin: 0 0 5px 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.result-merchant {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
}

.result-price {
  font-size: 1.3rem;
  font-weight: 700;
  color: #e74c3c;
}

.result-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
  font-size: 0.85rem;
  color: #888;
}

.result-description {
  margin: 0 0 15px 0;
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}

.result-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 15px;
}

.result-tag {
  background: #f8f9fa;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  color: #666;
}

.result-tag.spicy {
  background: #ffe8e6;
  color: #e74c3c;
}

.result-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.btn-primary {
  flex: 1;
  background: #e74c3c;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.3s ease;
}

.btn-primary:hover {
  background: #c0392b;
}

.btn-secondary {
  background: #f8f9fa;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 6px;
  cursor: pointer;
  color: #666;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: #e9ecef;
}

/* 大号收藏按钮样式 */
.btn-favorite-large {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-width: 100px;
  min-height: 50px;
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
}

.btn-favorite-large:hover {
  background: #c0392b;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(231, 76, 60, 0.4);
}

.btn-favorite-large i {
  font-size: 1.1rem;
}

/* 列表视图 */
.results-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.result-item-simple {
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.result-item-simple:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.simple-item-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 10px;
}

.simple-item-icon {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  flex-shrink: 0;
}

.simple-item-info {
  flex: 1;
}

.simple-item-main {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.simple-item-name {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.simple-item-merchant {
  font-size: 0.9rem;
  color: #666;
}

.simple-item-details {
  display: flex;
  gap: 15px;
  font-size: 0.85rem;
  color: #888;
}

.simple-item-price {
  color: #e74c3c;
  font-weight: 600;
}

.simple-item-actions {
  display: flex;
  gap: 8px;
}

.btn-simple-primary {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.btn-simple-secondary {
  background: #f8f9fa;
  border: 1px solid #ddd;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  color: #666;
  font-size: 0.8rem;
}

.simple-item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.simple-item-tags {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.simple-tag {
  background: #f8f9fa;
  padding: 2px 6px;
  border-radius: 8px;
  font-size: 0.75rem;
  color: #666;
}

.simple-item-canteen {
  font-size: 0.8rem;
  color: #888;
}

/* 无结果提示 */
.no-results {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.no-results i {
  font-size: 4rem;
  color: #ccc;
  margin-bottom: 1rem;
}

.no-results h3 {
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
}

.no-results p {
  margin: 0 0 2rem 0;
  font-size: 1rem;
}

/* 用户偏好按钮样式 */
.preference-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  border-top: 1px solid #e9ecef;
  padding-top: 15px;
}

.btn-save-preference,
.btn-load-preference {
  flex: 1;
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
  justify-content: center;
  gap: 6px;
}

.btn-save-preference:hover,
.btn-load-preference:hover {
  background: #e74c3c;
  color: white;
  transform: translateY(-1px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    flex-direction: column;
    padding: 0 15px;
  }
  
  .search-sidebar {
    width: 100%;
  }
  
  .search-header .container {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }
  
  .results-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .results-grid {
    grid-template-columns: 1fr;
  }
  
  .simple-item-header {
    flex-wrap: wrap;
  }
  
  .simple-item-footer {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
}
</style>
