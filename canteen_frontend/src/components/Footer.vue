<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h3>{{ $t('appName') }}</h3>
          <p>{{ $t('footerDescription') }}</p>
        </div>
        <div class="footer-section">
          <h4>{{ $t('quickLinks') }}</h4>
          <ul>
            <li><a href="#">{{ $t('home') }}</a></li>
            <li><a href="#">{{ $t('explore') }}</a></li>
            <li><a href="#">{{ $t('navigation') }}</a></li>
            <li><a href="#">{{ $t('about') }}</a></li>
          </ul>
        </div>
        <div class="footer-section">
          <h4>{{ $t('contactUs') }}</h4>
          <ul>
            <li><i class="fas fa-envelope"></i>https://www.sjtu.edu.cn/</li>
            <li><i class="fas fa-phone"></i>54749110</li>
            <li><i class="fas fa-map-marker-alt"></i>上海交通大学</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2025 {{ $t('appName') }} {{ $t('copyright') }}</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter'
}
</script>

<style scoped>
/* Footer组件的特定样式，全局样式已在style.css中定义 */
/* 这里只保留Vue组件特有的样式，避免重复定义 */
</style>
