import { createStore } from 'vuex'

export default createStore({
  state: {
    // 用户认证状态
    user: {
      isAuthenticated: false,
      type: null, // 'user' 或 'merchant'
      info: null
    },
    // 网络状态
    network: {
      isOnline: navigator.onLine
    },
    // UI状态
    ui: {
      showLoginModal: false,
      loginModalTab: 'user-login'
    }
  },
  mutations: {
    // 设置用户认证状态
    SET_USER_AUTH(state, { isAuthenticated, type, info }) {
      state.user.isAuthenticated = isAuthenticated
      state.user.type = type
      state.user.info = info
    },
    // 清除用户认证状态
    CLEAR_USER_AUTH(state) {
      state.user.isAuthenticated = false
      state.user.type = null
      state.user.info = null
    },
    // 设置网络状态
    SET_NETWORK_STATUS(state, isOnline) {
      state.network.isOnline = isOnline
    },
    // 设置登录模态框显示状态
    SET_LOGIN_MODAL(state, { show, tab }) {
      state.ui.showLoginModal = show
      if (tab) {
        state.ui.loginModalTab = tab
      }
    }
  },
  actions: {
    // 用户登录
    login({ commit }, { type, userInfo }) {
      commit('SET_USER_AUTH', {
        isAuthenticated: true,
        type,
        info: userInfo
      })
      
      // 保存到localStorage
      localStorage.setItem('currentUser', JSON.stringify({
        type,
        ...userInfo
      }))
    },
    // 用户登出
    logout({ commit }) {
      commit('CLEAR_USER_AUTH')
      localStorage.removeItem('currentUser')
    },
    // 检查本地存储的用户信息
    checkLocalStorage({ commit }) {
      const currentUser = JSON.parse(localStorage.getItem('currentUser'))
      if (currentUser) {
        commit('SET_USER_AUTH', {
          isAuthenticated: true,
          type: currentUser.type,
          info: currentUser
        })
      }
    },
    // 更新网络状态
    updateNetworkStatus({ commit }, isOnline) {
      commit('SET_NETWORK_STATUS', isOnline)
    },
    // 显示登录模态框
    showLoginModal({ commit }, tab = 'user-login') {
      commit('SET_LOGIN_MODAL', { show: true, tab })
    },
    // 隐藏登录模态框
    hideLoginModal({ commit }) {
      commit('SET_LOGIN_MODAL', { show: false })
    }
  },
  getters: {
    // 获取用户认证状态
    isAuthenticated: state => state.user.isAuthenticated,
    // 获取用户类型
    userType: state => state.user.type,
    // 获取用户信息
    userInfo: state => state.user.info,
    // 获取网络状态
    isOnline: state => state.network.isOnline,
    // 获取登录模态框状态
    showLoginModal: state => state.ui.showLoginModal,
    // 获取登录模态框当前标签页
    loginModalTab: state => state.ui.loginModalTab
  }
})
