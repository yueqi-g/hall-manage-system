<template>
  <header class="header">
    <div class="container">
      <div class="logo">
        <i class="fas fa-utensils"></i>
        <span>{{ $t('logo') }}</span>
      </div>
      <nav class="nav">
        <a href="#" class="nav-link active">{{ $t('navHome') }}</a>
        <!-- 新增核心功能导航 -->
        <a href="#features" class="nav-link" @click.prevent="scrollToSection('features')">
          {{ $t('coreFeatures') }}
        </a>
        <!-- 新增美食助手导航 -->
        <a href="#ai-assistant" class="nav-link" @click.prevent="scrollToSection('ai-assistant')">
          {{ $t('aiFoodAssistant') }}
        </a>
      </nav>
      <div class="header-actions">
        <button class="icon-btn notification-btn" @click="showNotification">
          <i class="fas fa-bell"></i>
        </button>
        <div class="user-menu">
          <button class="user-btn" @click="toggleUserDropdown">
            <template v-if="isLoggedIn">
              <i class="fas fa-user-circle"></i>
              <span>{{ currentUser.username }}</span>
              <i class="fas fa-chevron-down"></i>
            </template>
            <template v-else>
              <i class="fas fa-user"></i>
              <span>{{ $t('loginRegister') }}</span>
            </template>
          </button>
          <div class="user-dropdown" :class="{ show: showUserDropdown }">
            <template v-if="isLoggedIn">
              <!-- 已登录用户菜单 -->
              <a href="#" class="dropdown-item" @click.prevent="showFavorites">
                <i class="fas fa-heart"></i>
                {{ $t('myFavorites') }}
              </a>
              <a href="#" class="dropdown-item" @click.prevent="showOrders">
                <i class="fas fa-receipt"></i>
                {{ $t('myOrders') }}
              </a>
              <div class="dropdown-divider"></div>
              <a href="#" class="dropdown-item" @click.prevent="logout">
                <i class="fas fa-sign-out-alt"></i>
                {{ $t('logout') }}
              </a>
            </template>
            <template v-else>
              <!-- 未登录用户菜单 -->
              <a href="#" class="dropdown-item" @click.prevent="showLoginModal('user')">
                <i class="fas fa-user"></i>
                {{ $t('userLogin') }}
              </a>
              <a href="#" class="dropdown-item" @click.prevent="showLoginModal('merchant')">
                <i class="fas fa-store"></i>
                {{ $t('merchantLogin') }}
              </a>
              <a href="#" class="dropdown-item" @click.prevent="showLoginModal('register')">
                <i class="fas fa-user-plus"></i>
                {{ $t('registerAccount') }}
              </a>
            </template>
          </div>
        </div>
        <div class="language-switcher">
          <button class="language-btn" @click="toggleLanguageDropdown">
            <i class="fas fa-globe"></i>
            <span>{{ currentLanguage }}</span>
            <i class="fas fa-chevron-down"></i>
          </button>
          <div class="language-dropdown" :class="{ show: showLanguageDropdown }">
            <a 
              href="#" 
              class="dropdown-item" 
              :class="{ active: currentLanguage === '简体中文' }"
              @click.prevent="changeLanguage('zh-CN', '简体中文')"
            >
              简体中文
            </a>
            <a 
              href="#" 
              class="dropdown-item" 
              :class="{ active: currentLanguage === '繁體中文' }"
              @click.prevent="changeLanguage('zh-TW', '繁體中文')"
            >
              繁體中文
            </a>
            <a 
              href="#" 
              class="dropdown-item" 
              :class="{ active: currentLanguage === 'English' }"
              @click.prevent="changeLanguage('en', 'English')"
            >
              English
            </a>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { userAPI, authAPI, ordersAPI } from '@/services/api'

export default {
  name: 'AppHeader',
  data() {
    return {
      showUserDropdown: false,
      showLanguageDropdown: false,
      currentLanguage: '简体中文',
      languages: [
        { code: 'zh-CN', name: '简体中文' },
        { code: 'zh-TW', name: '繁體中文' },
        { code: 'en', name: 'English' }
      ],
      // 新增用户状态数据
      currentUser: null,
      isLoggedIn: false,
      userFavorites: [],
      userOrders: []
    }
  },
  methods: {
    // 新增滚动到指定区域的方法
    scrollToSection(sectionId) {
      const element = document.getElementById(sectionId)
      if (element) {
        element.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        })
        
        // 更新导航激活状态
        this.updateActiveNav(sectionId)
      }
    },
    
    // 更新导航激活状态
    updateActiveNav(activeSection) {
      const navLinks = document.querySelectorAll('.nav-link')
      navLinks.forEach(link => {
        link.classList.remove('active')
        if (link.getAttribute('href') === `#${activeSection}`) {
          link.classList.add('active')
        }
      })
    },
    showNotification() {
      alert(this.$t('noNewMessages'))
    },
    toggleUserDropdown() {
      console.log('toggleUserDropdown called, current state:', this.showUserDropdown)
      this.showUserDropdown = !this.showUserDropdown
      console.log('toggleUserDropdown new state:', this.showUserDropdown)
      // 关闭语言下拉框
      this.showLanguageDropdown = false
    },
    toggleLanguageDropdown() {
      this.showLanguageDropdown = !this.showLanguageDropdown
      // 关闭用户下拉框
      this.showUserDropdown = false
    },
    showLoginModal(type) {
      console.log('Header组件: 触发show-login-modal事件，类型:', type)
      // 触发全局事件显示登录模态框，并传递具体的登录类型
      this.$emit('show-login-modal', type)
      console.log('Header组件: 事件已触发，等待父组件响应，类型:', type)
      this.showUserDropdown = false
    },
    changeLanguage(code, name) {
      this.currentLanguage = name
      this.showLanguageDropdown = false
      console.log('切换语言:', code, name)
      // 使用Vue I18n切换语言
      this.$i18n.locale = code
      localStorage.setItem('userLocale', code)
    },
    closeDropdowns() {
      this.showUserDropdown = false
      this.showLanguageDropdown = false
    },
    // 新增登录状态管理方法
    async checkLoginStatus() {
      // 后端未提供 /user/profile/ 接口，这里直接使用本地存储判定登录状态
      const userData = localStorage.getItem('currentUser')
      if (userData) {
        this.currentUser = JSON.parse(userData)
        this.isLoggedIn = true
      } else {
        this.clearUserData()
      }
    },
    
    // 登录成功处理
    handleLoginSuccess(userData) {
      this.currentUser = userData
      this.isLoggedIn = true
      this.showUserDropdown = false
      // 加载用户收藏和订单数据
      this.loadUserData()
    },
    
    // 加载用户数据
    async loadUserData() {
      if (this.isLoggedIn) {
        try {
          // 加载收藏数据
          const favoritesResponse = await userAPI.getFavorites()
          if (favoritesResponse.success) {
            this.userFavorites = favoritesResponse.data.favorites
          }
          
          // 加载订单数据
          const ordersResponse = await ordersAPI.getOrders()
          if (ordersResponse.success) {
            this.userOrders = ordersResponse.data.orders
          }
        } catch (error) {
          console.error('加载用户数据失败:', error)
        }
      }
    },
    
    // 退出登录
    async logout() {
      try {
        await authAPI.logout()
      } catch (error) {
        console.error('退出登录失败:', error)
      } finally {
        this.clearUserData()
        this.showUserDropdown = false
        alert(this.$t('logoutSuccess'))
        // 跳转到首页
        if (this.$route.path !== '/') {
          this.$router.push('/')
        }
      }
    },
    
    // 清除用户数据
    clearUserData() {
      localStorage.removeItem('token')
      localStorage.removeItem('currentUser')
      this.currentUser = null
      this.isLoggedIn = false
      this.userFavorites = []
      this.userOrders = []
    },
    
    // 跳转到收藏页面
    showFavorites() {
      console.log('=== 跳转到收藏页面 ===')
      console.log('当前登录状态:', this.isLoggedIn)
      console.log('当前用户:', this.currentUser)
      
      if (!this.isLoggedIn) {
        alert(this.$t('pleaseLogin'))
        this.showUserDropdown = false
        return
      }
      
      // 直接跳转到收藏页面，收藏页面会在加载时自动发送请求
      this.$router.push('/favorites')
      this.showUserDropdown = false
    },
    
    // 显示订单页面
    showOrders() {
      if (this.userOrders.length > 0) {
        alert(`您有 ${this.userOrders.length} 个订单`)
      } else {
        alert(this.$t('noOrders'))
      }
      this.showUserDropdown = false
    }
  },
  mounted() {
    // 初始化时检查登录状态
    this.checkLoginStatus()
    
    // 点击页面其他地方关闭下拉框
    document.addEventListener('click', (event) => {
      if (!this.$el.contains(event.target)) {
        this.closeDropdowns()
      }
    })
  },
  beforeUnmount() {
    document.removeEventListener('click', this.closeDropdowns)
  }
}
</script>

<style scoped>
/* Header组件的特定样式，全局样式已在style.css中定义 */
/* 这里只保留Vue组件特有的样式，避免重复定义 */

/* 调试样式 - 确保下拉菜单能够显示 */
.user-dropdown {
  display: none;
}

.user-dropdown.show {
  display: block !important;
}
</style>
