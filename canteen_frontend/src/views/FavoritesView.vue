<template>
  <div class="favorites-page">
    <AppHeader />
    
    <!-- 收藏头部 -->
    <section class="favorites-header">
      <div class="container">
        <div class="back-btn" @click="$router.go(-1)">
          <i class="fas fa-arrow-left"></i>
          返回
        </div>
        <div class="favorites-info">
          <h1>我的收藏</h1>
          <p class="favorites-summary">您收藏的菜品列表</p>
        </div>
      </div>
    </section>

    <main class="favorites-main">
      <div class="container">
        <!-- 收藏统计 -->
        <div class="favorites-stats" v-if="favorites.length > 0">
          <div class="stat-item">
            <div class="stat-value">{{ favorites.length }}</div>
            <div class="stat-label">收藏总数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ favoriteCategories.length }}</div>
            <div class="stat-label">菜品类别</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ favoriteCanteens.length }}</div>
            <div class="stat-label">涉及食堂</div>
          </div>
        </div>

        <!-- 收藏列表 -->
        <section class="favorites-list">
          <div class="favorites-header">
            <div class="favorites-count">
              共 <span>{{ favorites.length }}</span> 个收藏
            </div>
          </div>

          <!-- 收藏容器 - 使用SearchResults的网格样式 -->
          <div class="favorites-container" id="favoritesContainer">
            <!-- 网格视图 -->
            <div class="favorites-grid">
              <div 
                v-for="favorite in favorites" 
                :key="favorite.id"
                class="favorite-item"
                :data-favorite-id="favorite.id"
              >
                <div class="favorite-image" :style="{ background: getDishColor(favorite.dish_id) }">
                  <i :class="getDishIcon(favorite.dish_id)"></i>
                  <div class="favorite-rating">
                    <i class="fas fa-heart"></i>
                  </div>
                </div>
                <div class="favorite-content">
                  <div class="favorite-header">
                    <div class="favorite-title">
                      <h3 class="favorite-name">{{ favorite.dish_name }}</h3>
                      <p class="favorite-merchant">{{ favorite.store_name }}</p>
                    </div>
                    <div class="favorite-price">¥{{ favorite.price }}</div>
                  </div>
                  <div class="favorite-meta">
                    <span class="favorite-wait-time">
                      <i class="fas fa-clock"></i> {{ favorite.wait_time || '10-15分钟' }}
                    </span>
                    <span class="favorite-canteen">
                      <i class="fas fa-store"></i> {{ favorite.canteen }}
                    </span>
                  </div>
                  <p class="favorite-description">{{ favorite.description }}</p>
                  <div class="favorite-tags">
                    <span 
                      class="favorite-tag"
                      :class="{ spicy: favorite.taste === '辣' || favorite.taste === '麻辣' }"
                    >
                      {{ favorite.taste }}
                    </span>
                    <span class="favorite-tag">
                      {{ favorite.category }}
                    </span>
                    <div class="favorite-actions">
                    <button class="btn-secondary" @click.stop="removeFavorite(favorite.id)">
                      <i class="fas fa-times"></i> 取消收藏
                    </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 无收藏提示 -->
          <div class="no-favorites" v-if="!loading && favorites.length === 0">
            <i class="fas fa-heart"></i>
            <h3>您还没有收藏任何菜品</h3>
            <p>去发现更多美味菜品并收藏吧</p>
            <button class="btn-primary" @click="$router.push('/search')">去发现</button>
          </div>

          <!-- 加载状态 -->
          <div class="loading" v-if="loading">
            <i class="fas fa-spinner fa-spin"></i>
            <p>加载中...</p>
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
import { favoritesAPI, dishesAPI } from '@/services/api'

export default {
  name: 'FavoritesView',
  components: {
    AppHeader,
    AppFooter,
    LoginModal
  },
  data() {
    return {
      favorites: [],
      loading: false,
      showLoginModal: false
    }
  },
  computed: {
    favoriteCategories() {
      const categories = this.favorites.map(f => f.category)
      return [...new Set(categories)]
    },
    favoriteCanteens() {
      const canteens = this.favorites.map(f => f.canteen)
      return [...new Set(canteens)]
    }
  },
  methods: {
    // 加载收藏列表
    async loadFavorites() {
      this.loading = true
      try {
        const response = await favoritesAPI.getFavorites()
        if (response.success) {
          this.favorites = response.data.favorites || []
          console.log(`加载到 ${this.favorites.length} 个收藏`)
        } else {
          console.error('获取收藏列表失败:', response.message)
          this.favorites = []
        }
      } catch (error) {
        console.error('获取收藏列表错误:', error)
        this.favorites = []
      } finally {
        this.loading = false
      }
    },

    // 移除收藏
    async removeFavorite(favoriteId) {
      if (!confirm('确定要取消收藏这个菜品吗？')) {
        return
      }

      try {
        const response = await favoritesAPI.removeFavorite(favoriteId)
        if (response.success) {
          // 从列表中移除
          this.favorites = this.favorites.filter(f => f.id !== favoriteId)
          alert('取消收藏成功')
        } else {
          alert('取消收藏失败: ' + (response.message || '未知错误'))
        }
      } catch (error) {
        console.error('取消收藏失败:', error)
        alert('取消收藏失败，请检查网络连接')
      }
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

    // 查看菜品详情
    viewDishDetails(dishId) {
      this.$router.push(`/dish/${dishId}`)
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
    }
  },
  mounted() {
    this.loadFavorites()
  }
}
</script>

<style scoped>
/* 收藏头部样式 - 使用SearchResults的样式 */
.favorites-header {
  background: linear-gradient(135deg, rgb(251, 176, 204) 50%, #f5576c 100%);
  color: white;
  padding: 30px 0;
}

.favorites-header .container {
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

.favorites-info h1 {
  margin: 0 0 8px 0;
  font-size: 2rem;
  font-weight: 700;
}

.favorites-summary {
  margin: 0;
  opacity: 0.9;
  font-size: 1rem;
}

/* 主内容区域 */
.favorites-main {
  padding: 30px 0;
  min-height: 80vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 收藏统计 */
.favorites-stats {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.stat-item {
  text-align: center;
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #e74c3c;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

/* 收藏列表头部 */
.favorites-list .favorites-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background: none;
  padding: 0;
}

.favorites-count {
  font-size: 1.1rem;
  color: #666;
}

.favorites-count span {
  font-weight: 700;
  color: #e74c3c;
}

/* 收藏网格 - 使用SearchResults的网格样式 */
.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.favorite-item {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.favorite-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.favorite-image {
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: white;
  position: relative;
}

.favorite-rating {
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

.favorite-content {
  padding: 15px;
}

.favorite-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.favorite-name {
  margin: 0 0 5px 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.favorite-merchant {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
}

.favorite-price {
  font-size: 1.3rem;
  font-weight: 700;
  color: #e74c3c;
}

.favorite-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
  font-size: 0.85rem;
  color: #888;
}

.favorite-description {
  margin: 0 0 15px 0;
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}

.favorite-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 15px;
  align-items: center;
  width: 100%;
}

.favorite-tag {
  background: #f8f9fa;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  color: #666;
}

.favorite-tag.spicy {
  background: #ffe8e6;
  color: #e74c3c;
}

.favorite-actions {
  display: inline-flex;
  gap: 10px;
  margin-left: auto;
  vertical-align: middle;
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

/* 无收藏提示 */
.no-favorites {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.no-favorites i {
  font-size: 4rem;
  color: #ccc;
  margin-bottom: 1rem;
}

.no-favorites h3 {
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
}

.no-favorites p {
  margin: 0 0 2rem 0;
  font-size: 1rem;
}

/* 加载状态 */
.loading {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.loading i {
  font-size: 2rem;
  margin-bottom: 1rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .favorites-stats {
    flex-direction: column;
    gap: 20px;
  }
  
  .favorites-grid {
    grid-template-columns: 1fr;
  }
  
  .favorite-actions {
    flex-direction: column;
  }
  
  .favorites-header .container {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }
}
</style>
