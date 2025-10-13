import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserDashboard from '../views/UserDashboard.vue'
import MerchantDashboard from '../views/MerchantDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/user/dashboard',
    name: 'user-dashboard',
    component: UserDashboard
  },
  {
    path: '/merchant/dashboard',
    name: 'merchant-dashboard',
    component: MerchantDashboard
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 路由守卫 - 检查登录状态
router.beforeEach((to, from, next) => {
  // 检查localStorage中的用户信息
  const userData = localStorage.getItem('currentUser')
  
  if (userData) {
    const currentUser = JSON.parse(userData)
    
    // 如果已登录，根据用户类型重定向
    if (currentUser.type === 'user' && to.name !== 'user-dashboard') {
      // 重定向到用户仪表板
      next({ name: 'user-dashboard' })
    } else if (currentUser.type === 'merchant' && to.name !== 'merchant-dashboard') {
      // 重定向到商家仪表板
      next({ name: 'merchant-dashboard' })
    } else {
      next()
    }
  } else {
    // 未登录用户，允许访问首页和其他公共页面
    if (to.name === 'user-dashboard' || to.name === 'merchant-dashboard') {
      // 如果尝试访问仪表板但未登录，重定向到首页
      next({ name: 'home' })
    } else {
      next()
    }
  }
})

export default router
