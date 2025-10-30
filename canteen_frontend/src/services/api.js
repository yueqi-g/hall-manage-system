import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 添加请求日志
api.interceptors.request.use(
  (config) => {
    console.log('API请求:', config.method?.toUpperCase(), config.url, config.data)
    return config
  },
  (error) => {
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)

// 请求拦截器 - 添加token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 统一处理错误
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response) {
      // 服务器返回错误状态码
      const { status, data } = error.response
      switch (status) {
        case 401:
          // Token过期，清除本地存储并跳转到登录页
          localStorage.removeItem('token')
          localStorage.removeItem('currentUser')
          window.location.href = '/'
          break
        case 403:
          console.error('权限不足:', data.message)
          break
        case 404:
          console.error('资源不存在:', data.message)
          break
        case 422:
          console.error('参数验证失败:', data.message)
          break
        default:
          console.error('服务器错误:', data.message)
      }
    } else if (error.request) {
      // 请求未收到响应
      console.error('网络错误: 请检查网络连接')
    } else {
      // 请求配置错误
      console.error('请求配置错误:', error.message)
    }
    return Promise.reject(error)
  }
)


// 认证相关API
export const authAPI = {
  // 用户登录
  userLogin: (data) => api.post('/auth/user-login/', data),
  
  // 商家登录
  merchantLogin: (data) => api.post('/auth/merchant-login/', data),
  
  // 用户注册
  register: (data) => api.post('/auth/register/', data),
  
  
  // 退出登录
  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('currentUser')
    return Promise.resolve()
  }
}

// 用户相关API
export const userAPI = {
  // 获取用户信息
  getProfile: () => api.get('/user/profile/'),
  
  // 获取用户收藏（已废弃，请使用 favoritesAPI.getFavorites）
  getFavorites: () => {
    console.warn('userAPI.getFavorites 已废弃，请使用 favoritesAPI.getFavorites')
    return favoritesAPI.getFavorites()
  },
  
  // 更新用户偏好
  updatePreferences: (data) => {
    // 从localStorage获取当前用户ID并添加到请求数据中
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}')
    console.log('当前用户信息:', currentUser)
    const payload = {
      userId: currentUser.id || currentUser.userId || '1', // 尝试多种可能的用户ID字段
      preferences: data
    }
    console.log('发送偏好更新请求:', payload)
    return api.put('/user/preferences/', payload)
  },
  
  // 获取用户偏好
  getPreferences: () => {
    // 从localStorage获取当前用户ID并添加到查询参数中
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}')
    console.log('当前用户信息:', currentUser)
    const userId = currentUser.id || currentUser.userId || '1' // 尝试多种可能的用户ID字段
    console.log('获取用户偏好，用户ID:', userId)
    return api.get('/user/preferences/', { params: { userId } })
  }
}

// 菜品相关API
export const dishesAPI = {
  // 菜品搜索
  search: (params) => api.get('/dishes/search', { params }),
  
  // 搜索建议
  searchSuggestions: (params) => api.get('/dishes/suggestions', { params }),
  
  // 菜品筛选
  filter: (params) => api.get('/dishes/filter', { params }),
  
  // AI智能推荐
  aiRecommend: (data) => api.post('/dishes/ai-recommend', data),
  
  // 热门推荐
  getPopular: () => api.get('/dishes/popular'),
  
  // 随机菜品
  getRandom: (params) => api.get('/dishes/random', { params }),
  
  // 菜品详情
  getDetail: (id) => api.get(`/dishes/${id}`)
}

// 订单相关API
export const ordersAPI = {
  // 下单菜品
  createOrder: (data) => api.post('/orders/create/', data),
  
  // 获取订单列表
  getOrders: () => api.get('/user/orders/')
}

// 收藏相关API
export const favoritesAPI = {
  // 收藏菜品
  addFavorite: (data) => {
    // 从localStorage获取当前用户ID并添加到请求数据中
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}')
    console.log('当前用户信息:', currentUser)
    const payload = {
      ...data,
      userId: currentUser.id || currentUser.userId || '1' // 尝试多种可能的用户ID字段
    }
    console.log('发送收藏请求:', payload)
    return api.post('/favorites/add/', payload)
  },
  
  // 获取收藏列表
  getFavorites: () => {
    // 从localStorage获取当前用户ID并添加到查询参数中
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}')
    console.log('当前用户信息:', currentUser)
    const userId = currentUser.id || currentUser.userId || '1' // 尝试多种可能的用户ID字段
    console.log('获取收藏列表，用户ID:', userId)
    return api.get('/favorites/', { params: { userId } })
  },
  
  // 移除收藏
  removeFavorite: (favoriteId) => {
    // 从localStorage获取当前用户ID并添加到查询参数中
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}')
    console.log('当前用户信息:', currentUser)
    const userId = currentUser.id || currentUser.userId || '1' // 尝试多种可能的用户ID字段
    console.log('移除收藏，用户ID:', userId, '收藏ID:', favoriteId)
    return api.delete(`/favorites/${favoriteId}/`, { params: { userId } })
  }
}

// 商家管理API
export const merchantAPI = {
  // 菜品管理
  getDishes: (merchantId) => {
    const params = {}
    if (Number.isFinite(merchantId)) params.merchant = merchantId
    return api.get('/merchants/dishes', { params })
  },
  addDish: (data) => api.post('/merchants/dishes/add', data),
  updateDish: (id, data) => api.put(`/merchants/dishes/${id}`, data),
  deleteDish: (id) => api.delete(`/merchants/dishes/${id}/delete`),
  // 查找商家
  findMerchants: (params) => api.get('/merchants/', { params }),
  
  // 客流量管理
  updateTraffic: (merchantId, data) => {
    // 添加merchant_id到请求数据中
    const payload = {
      merchant_id: merchantId,
      ...data
    }
    return api.post('/merchants/traffic', payload)
  },
  getStats: () => Promise.resolve({ success: false, message: '未实现' })
}

// 数据统计API
export const statsAPI = {
  // 实时客流量
  getTraffic: () => api.get('/stats/traffic/')
}

export default api
