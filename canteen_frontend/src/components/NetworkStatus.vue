<template>
  <div class="network-status" :class="{ show: isVisible, online: isOnline }">
    <i :class="statusIcon"></i>
    <span>{{ statusMessage }}</span>
  </div>
</template>

<script>
export default {
  name: 'NetworkStatus',
  data() {
    return {
      isVisible: false,
      isOnline: navigator.onLine,
      statusMessage: '',
      hideTimeout: null
    }
  },
  computed: {
    statusIcon() {
      return this.isOnline ? 'fas fa-wifi' : 'fas fa-wifi-slash'
    }
  },
  methods: {
    handleOnline() {
      this.isOnline = true
      this.statusMessage = '网络连接已恢复'
      this.showStatus()
    },
    handleOffline() {
      this.isOnline = false
      this.statusMessage = '网络连接已断开'
      this.showStatus()
    },
    showStatus() {
      this.isVisible = true
      
      // 如果是网络恢复，3秒后自动隐藏
      if (this.isOnline) {
        clearTimeout(this.hideTimeout)
        this.hideTimeout = setTimeout(() => {
          this.isVisible = false
        }, 3000)
      }
    },
    addEventListeners() {
      window.addEventListener('online', this.handleOnline)
      window.addEventListener('offline', this.handleOffline)
    },
    removeEventListeners() {
      window.removeEventListener('online', this.handleOnline)
      window.removeEventListener('offline', this.handleOffline)
    }
  },
  mounted() {
    this.addEventListeners()
    // 初始化状态消息
    this.statusMessage = this.isOnline ? '网络连接正常' : '网络连接已断开'
  },
  beforeUnmount() {
    this.removeEventListeners()
    clearTimeout(this.hideTimeout)
  }
}
</script>

<style scoped>
/* NetworkStatus组件的特定样式，全局样式已在style.css中定义 */
/* 这里只保留Vue组件特有的样式，避免重复定义 */
</style>
