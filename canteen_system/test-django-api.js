#!/usr/bin/env node

/**
 * 测试Django后端API
 * 运行: node test-django-api.js
 */

const axios = require('axios')

// Django后端API配置
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

async function testDjangoAPI() {
  console.log('=== 测试Django后端API ===\n')
  
  try {
    // 1. 测试用户注册
    console.log('1. 测试用户注册...')
    const registerData = {
      username: 'testuser' + Date.now(),
      password: 'password123',
      email: 'test@example.com'
    }
    
    const registerResponse = await api.post('/auth/register/', registerData)
    
    if (registerResponse.data.success) {
      console.log('✅ 用户注册成功:', registerResponse.data.message)
    } else {
      console.log('❌ 用户注册失败:', registerResponse.data.message)
    }
    
    // 2. 测试用户登录
    console.log('\n2. 测试用户登录...')
    const loginResponse = await api.post('/auth/user-login/', {
      username: registerData.username,
      password: registerData.password
    })
    
    if (loginResponse.data.success) {
      console.log('✅ 用户登录成功:', loginResponse.data.message)
      const token = loginResponse.data.data.token
      
      // 3. 测试获取菜品列表
      console.log('\n3. 测试获取菜品列表...')
      const dishesResponse = await api.get('/dishes/')
      
      if (dishesResponse.status === 200) {
        console.log('✅ 获取菜品列表成功，共', dishesResponse.data.results?.length || 0, '个菜品')
      } else {
        console.log('❌ 获取菜品列表失败')
      }
      
      // 4. 测试获取商家列表
      console.log('\n4. 测试获取商家列表...')
      const merchantsResponse = await api.get('/merchants/')
      
      if (merchantsResponse.status === 200) {
        console.log('✅ 获取商家列表成功，共', merchantsResponse.data.results?.length || 0, '个商家')
      } else {
        console.log('❌ 获取商家列表失败')
      }
      
      // 5. 测试AI推荐
      console.log('\n5. 测试AI推荐...')
      const aiResponse = await api.post('/ai-services/recommend_dishes/', {
        query: '麻辣香锅',
        preferences: {
          category: '主食',
          taste: '麻辣'
        }
      })
      
      if (aiResponse.data.success) {
        console.log('✅ AI推荐成功:', aiResponse.data.data.recommendations?.length || 0, '个推荐')
      } else {
        console.log('❌ AI推荐失败')
      }
      
    } else {
      console.log('❌ 用户登录失败:', loginResponse.data.message)
    }
    
    console.log('\n🎉 Django后端API测试完成！')
    
  } catch (error) {
    console.error('❌ 测试过程中出现错误:', error.message)
    if (error.response) {
      console.error('响应状态:', error.response.status)
      console.error('响应数据:', error.response.data)
    }
  }
}

// 运行测试
if (require.main === module) {
  testDjangoAPI().catch(console.error)
}

module.exports = { testDjangoAPI }
