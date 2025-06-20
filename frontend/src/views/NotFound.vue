<template>
  <div class="not-found-container">
    <el-card class="not-found-card">
      <h1>404</h1>
      <h2>页面未找到</h2>
      <p>抱歉，您访问的页面不存在。</p>
      <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
    </el-card>
  </div>
</template>

<script setup>
import { ElButton, ElCard } from 'element-plus'; // 导入 Element Plus 组件
// 无需其他逻辑，直接使用 $router 跳转
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  text-align: center;
}
.not-found-card {
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 400px;
  max-width: 90%;
}
h1 {
  font-size: 100px;
  color: #409EFF; /* Element Plus primary color */
  margin-bottom: 10px;
}
h2 {
  color: #606266;
  margin-bottom: 20px;
}
p {
  color: #909399;
  margin-bottom: 30px;
}
</style>