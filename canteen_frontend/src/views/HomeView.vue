<template>
  <div class="home">
    <!-- 顶部导航栏 -->
    <AppHeader @show-login-modal="handleShowLoginModal" />
    
    <!-- 主内容区 -->
    <main class="main">
      <!-- 英雄区域 -->
      <section class="hero">
        <div class="container">
          <div class="hero-content">
            <h1 class="hero-title"><span>{{ $t('heroTitle') }}</span></h1>
            <p class="hero-subtitle">{{ $t('heroSubtitle') }}</p>
            <div class="search-box">
              <input 
                type="text" 
                :placeholder="$t('searchPlaceholder')" 
                class="search-input"
                v-model="searchQuery"
              >
              <button class="search-btn" @click="handleSearch">
                <i class="fas fa-search"></i>
                {{ $t('smartRecommendation') }}
              </button>
            </div>
          </div>
          <div class="hero-image">
            <div class="hero-image-content"></div>
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
    </main>

    <!-- 页脚 -->
    <AppFooter />

    <!-- 登录/注册模态框 -->
    <LoginModal 
      :show="showLoginModal" 
      :initial-tab="loginModalType"
      @close="handleCloseModal"
      @login-success="handleLoginSuccess"
    />

    <!-- 网络状态提示 -->
    <NetworkStatus />
  </div>
</template>

<script>
import AppHeader from '@/components/Header.vue'
import AppFooter from '@/components/Footer.vue'
import LoginModal from '@/components/LoginModal.vue'
import NetworkStatus from '@/components/NetworkStatus.vue'

export default {
  name: 'HomeView',
  components: {
    AppHeader,
    AppFooter,
    LoginModal,
    NetworkStatus
  },
  data() {
    return {
      searchQuery: '',
      showLoginModal: false,
      loginModalType: 'user-login', // 默认登录类型
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
      ]
    }
  },
  methods: {
    handleSearch() {
      if (this.searchQuery.trim()) {
        console.log('搜索关键词:', this.searchQuery)
        // 这里可以添加搜索逻辑
      }
    },
    handleShowLoginModal(loginType) {
      console.log('HomeView: 接收到登录类型:', loginType)
      
      // 将Header中的类型映射到LoginModal的标签
      let modalTab = 'user-login'
      if (loginType === 'merchant') {
        modalTab = 'merchant-login'
      } else if (loginType === 'register') {
        modalTab = 'register'
      }
      
      this.loginModalType = modalTab
      this.showLoginModal = true
      console.log('HomeView: 设置模态框标签为:', modalTab)
    },
    handleCloseModal() {
      this.showLoginModal = false
    },
    handleLoginSuccess(userData) {
      console.log('HomeView: 登录成功，用户数据:', userData)
      // 登录成功后关闭模态框
      this.showLoginModal = false
      // 这里可以添加其他登录成功后的逻辑
      // Header组件会自动通过localStorage检测到登录状态变化
    }
  },
  mounted() {
    // 这里可以添加其他初始化逻辑
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main {
  flex: 1;
}
</style>
