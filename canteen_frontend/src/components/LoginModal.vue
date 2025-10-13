<template>
  <div v-if="show" class="modal" @click.self="closeModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ modalTitle }}</h2>
        <button class="close-btn" @click="closeModal">&times;</button>
      </div>
  <div class="modal-body" :class="{ 'scrollable': activeTab === 'register' }">
    <!-- 错误消息显示 -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
    
    <div class="auth-tabs">
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'user-login' }"
        @click="switchTab('user-login')"
      >
        用户登录
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'merchant-login' }"
        @click="switchTab('merchant-login')"
      >
        商家登录
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'register' }"
        @click="switchTab('register')"
      >
        注册
      </button>
    </div>
        
        <!-- 用户登录表单 -->
        <div class="tab-content" :class="{ active: activeTab === 'user-login' }">
          <form class="auth-form" @submit.prevent="handleUserLogin">
            <div class="form-group">
              <label for="username">用户名</label>
              <input 
                type="text" 
                id="username" 
                v-model="userLoginForm.username"
                placeholder="请输入用户名" 
                required
              >
            </div>
            <div class="form-group">
              <label for="password">密码</label>
              <input 
                type="password" 
                id="password" 
                v-model="userLoginForm.password"
                placeholder="请输入密码" 
                required
              >
            </div>
            <button type="submit" class="auth-btn">登录</button>
            <div class="auth-links">
              <a href="#">找回密码</a>
              <a href="#">使用统一身份认证登录</a>
            </div>
          </form>
        </div>
        
        <!-- 商家登录表单 -->
        <div class="tab-content" :class="{ active: activeTab === 'merchant-login' }">
          <form class="auth-form" @submit.prevent="handleMerchantLogin">
            <div class="form-group">
              <label for="merchant-username">商家账号</label>
              <input 
                type="text" 
                id="merchant-username" 
                v-model="merchantLoginForm.username"
                placeholder="请输入商家账号" 
                required
              >
            </div>
            <div class="form-group">
              <label for="merchant-password">密码</label>
              <input 
                type="password" 
                id="merchant-password" 
                v-model="merchantLoginForm.password"
                placeholder="请输入密码" 
                required
              >
            </div>
            <button type="submit" class="auth-btn">商家登录</button>
          </form>
        </div>
        
        <!-- 注册表单 -->
        <div class="tab-content" :class="{ active: activeTab === 'register' }">
          <form class="auth-form" @submit.prevent="handleRegister">
            <div class="form-group">
              <label for="register-type">注册类型</label>
              <select 
                id="register-type" 
                v-model="registerForm.type"
                required
              >
                <option value="">请选择注册类型</option>
                <option value="user">用户账号</option>
                <option value="merchant">商家账号</option>
              </select>
            </div>
            <div class="form-group">
              <label for="register-username">用户名</label>
              <input 
                type="text" 
                id="register-username" 
                v-model="registerForm.username"
                placeholder="请输入用户名" 
                required
              >
            </div>
            <div class="form-group">
              <label for="register-password">密码</label>
              <input 
                type="password" 
                id="register-password" 
                v-model="registerForm.password"
                placeholder="请输入密码" 
                required
              >
            </div>
            <div class="form-group">
              <label for="register-confirm-password">确认密码</label>
              <input 
                type="password" 
                id="register-confirm-password" 
                v-model="registerForm.confirmPassword"
                placeholder="请再次输入密码" 
                required
              >
            </div>
            <div class="form-group">
              <label for="register-email">邮箱</label>
              <input 
                type="email" 
                id="register-email" 
                v-model="registerForm.email"
                placeholder="请输入邮箱" 
                required
              >
            </div>
            
            <!-- 商家注册额外字段 -->
            <div v-if="registerForm.type === 'merchant'" class="merchant-fields">
              <div class="form-group">
                <label for="register-store-name">店铺名称 <span class="required">*</span></label>
                <input 
                  type="text" 
                  id="register-store-name" 
                  v-model="registerForm.storeName"
                  placeholder="请输入您的店铺名称" 
                  required
                >
              </div>
              <div class="form-group">
                <label for="register-canteen">所属食堂 <span class="required">*</span></label>
                <select 
                  id="register-canteen" 
                  v-model="registerForm.canteen"
                  required
                >
                  <option value="">请选择所属食堂</option>
                  <option value="一食堂">一食堂</option>
                  <option value="二食堂">二食堂</option>
                  <option value="三食堂">三食堂</option>
                  <option value="四食堂">四食堂</option>
                  <option value="其他">其他</option>
                </select>
              </div>
            </div>
            
            <button type="submit" class="auth-btn">注册</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api, { authAPI } from '@/services/api'

export default {
  name: 'LoginModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    initialTab: {
      type: String,
      default: 'user-login'
    }
  },
  data() {
    return {
      activeTab: this.initialTab,
      userLoginForm: {
        username: '',
        password: ''
      },
      merchantLoginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        type: '',
        username: '',
        password: '',
        confirmPassword: '',
        email: '',
        storeName: '',
        canteen: ''
      },
      loading: false,
      errorMessage: ''
    }
  },
  computed: {
    modalTitle() {
      switch (this.activeTab) {
        case 'user-login':
          return '用户登录'
        case 'merchant-login':
          return '商家登录'
        case 'register':
          return '注册账号'
        default:
          return '登录/注册'
      }
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
    },
    switchTab(tab) {
      this.activeTab = tab
      // 切换标签页时清空错误消息
      this.errorMessage = ''
    },
    async handleUserLogin() {
      if (this.loading) return
      
      console.log('=== 用户登录调试信息 ===')
      console.log('输入的用户名:', this.userLoginForm.username)
      
      this.loading = true
      this.errorMessage = ''
      
      try {
        const loginData = {
          username: this.userLoginForm.username,
          password: this.userLoginForm.password
        }
        
        console.log('发送登录请求数据:', { ...loginData, password: '***' })
        
        const response = await authAPI.userLogin(loginData)
        
        console.log('收到登录响应:', response)
        
        if (response.success) {
          const { user, token } = response.data
          
          console.log('登录成功，用户信息:', user)
          
          // 保存token和用户信息
          localStorage.setItem('token', token)
          localStorage.setItem('currentUser', JSON.stringify(user))
          
          // 触发登录成功事件
          this.$emit('login-success', user)
          
          // 跳转到用户仪表板
          this.$router.push('/user/dashboard')
          this.$emit('close')
        } else {
          console.log('登录失败，错误信息:', response.message)
          this.errorMessage = response.message || '登录失败'
        }
      } catch (error) {
        console.error('用户登录失败:', error)
        console.log('错误详情:', error.response ? error.response.data : error.message)
        this.errorMessage = '登录失败，请检查用户名和密码'
      } finally {
        this.loading = false
      }
    },
    
    async handleMerchantLogin() {
      if (this.loading) return
      
      this.loading = true
      this.errorMessage = ''
      
      try {
        const response = await authAPI.merchantLogin({
          username: this.merchantLoginForm.username,
          password: this.merchantLoginForm.password
        })
        
        console.log('商家登录响应:', response)
        
        if (response.success) {
          let { merchant, token } = response.data
          console.log('商家信息:', merchant)
          console.log('merchantId:', merchant.merchantId)
          
          // 若后端未返回 merchantId，则尝试根据用户名查询商家并填充
          if (!merchant.merchantId) {
            console.log('merchantId不存在，尝试查询商家信息...')
            try {
              const lookup = await api.get('/merchants/', {
                params: { search: merchant.username }
              })
              console.log('查询商家响应:', lookup)
              const results = Array.isArray(lookup?.results) ? lookup.results : (Array.isArray(lookup) ? lookup : [])
              if (results.length > 0) {
                merchant = { ...merchant, merchantId: results[0].id }
                console.log('找到商家ID:', results[0].id)
              } else {
                console.warn('未找到匹配的商家记录')
                this.errorMessage = '未找到商家信息，请联系管理员'
                this.loading = false
                return
              }
            } catch (e) {
              console.error('查询商家失败:', e)
              this.errorMessage = '无法获取商家信息，请联系管理员'
              this.loading = false
              return
            }
          }
          
          // 保存token和商家信息
          localStorage.setItem('token', token)
          localStorage.setItem('currentUser', JSON.stringify(merchant))
          
          console.log('已保存商家信息到localStorage')
          
          // 触发登录成功事件
          this.$emit('login-success', merchant)
          
          // 跳转到商家仪表板
          this.$router.push('/merchant/dashboard')
          this.$emit('close')
        } else {
          this.errorMessage = response.message || '商家登录失败'
        }
      } catch (error) {
        console.error('商家登录失败:', error)
        this.errorMessage = '商家登录失败，请检查账号和密码'
      } finally {
        this.loading = false
      }
    },
    
    async handleRegister() {
      if (this.loading) return
      
      // 验证密码一致性
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        this.errorMessage = '两次输入的密码不一致'
        return
      }
      
      this.loading = true
      this.errorMessage = ''
      
      try {
        const registerData = {
          type: this.registerForm.type,
          username: this.registerForm.username,
          password: this.registerForm.password,
          confirmPassword: this.registerForm.confirmPassword,
          email: this.registerForm.email
        }
        
        // 如果是商家注册，添加额外字段
        if (this.registerForm.type === 'merchant') {
          if (!this.registerForm.storeName || !this.registerForm.canteen) {
            this.errorMessage = '商家注册需要填写店铺名称和所属食堂'
            this.loading = false
            return
          }
          registerData.storeName = this.registerForm.storeName
          registerData.canteen = this.registerForm.canteen
        }
        
        console.log('=== 注册调试信息 ===')
        console.log('发送注册数据:', { ...registerData, password: '***', confirmPassword: '***' })
        
        const response = await authAPI.register(registerData)
        
        console.log('收到注册响应:', response)
        
        if (response.success) {
          const registeredUsername = this.registerForm.username
          const registeredPassword = this.registerForm.password
          const ismerchant = this.registerForm.type === 'merchant'
          
          alert('注册成功！将自动为您登录...')
          
          // 清空注册表单
          this.registerForm = {
            type: '',
            username: '',
            password: '',
            confirmPassword: '',
            email: '',
            storeName: '',
            canteen: ''
          }
          
          // 自动登录
          if (ismerchant) {
            // 商家登录
            this.merchantLoginForm.username = registeredUsername
            this.merchantLoginForm.password = registeredPassword
            this.activeTab = 'merchant-login'
            // 延迟一下让用户看到切换动画
            setTimeout(() => {
              this.handleMerchantLogin()
            }, 500)
          } else {
            // 用户登录
            this.userLoginForm.username = registeredUsername
            this.userLoginForm.password = registeredPassword
            this.activeTab = 'user-login'
            setTimeout(() => {
              this.handleUserLogin()
            }, 500)
          }
        } else {
          this.errorMessage = response.message || '注册失败'
        }
      } catch (error) {
        console.error('注册失败:', error)
        console.log('错误详情:', error.response ? error.response.data : error.message)
        this.errorMessage = '注册失败，请检查网络连接和输入信息'
      } finally {
        this.loading = false
      }
    }
  },
  watch: {
    initialTab(newTab) {
      this.activeTab = newTab
    }
  }
}
</script>

<style>
/* LoginModal组件使用全局样式，无需重复定义 */
/* 全局样式已在auth.css中定义 */

/* 让注册页在内容超出时可滚动，同时不影响登录页 */
.modal-content {
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  flex: 0 0 auto;
}

.modal-body {
  flex: 1 1 auto;
  overflow: hidden;
}

.modal-body.scrollable {
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}
</style>
