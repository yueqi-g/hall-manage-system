<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style>
/* 导入全局样式 */
@import url('./assets/css/merchant.css');
@import url('./assets/css/user.css');
@import url('./assets/css/style.css');
@import url('./assets/css/auth.css');

/* 导入Google字体 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

/* 导入Font Awesome图标 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

#app {
  font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #333;
  background-color: #f8f9fa;
  min-height: 100vh;
}

/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f8f9fa;
  overflow-x: hidden;
}
</style>
