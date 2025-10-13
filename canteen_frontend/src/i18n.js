import { createI18n } from 'vue-i18n'
import { messages } from '@/locales'

// 创建i18n实例
const i18n = createI18n({
  legacy: false, // 使用Composition API模式
  locale: localStorage.getItem('userLocale') || 'zh-CN', // 默认语言
  fallbackLocale: 'zh-CN', // 回退语言
  messages
})

export default i18n
