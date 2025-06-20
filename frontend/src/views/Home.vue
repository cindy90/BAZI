<template>
  <div class="home-container">
    <el-card class="home-card">
      <h1>欢迎来到八字算命应用！</h1>
      <p>您已成功登录。</p>
      <p>在这里您可以查询您的八字信息和运势。</p>
      <el-button type="primary" @click="handleLogout">退出登录</el-button>
    </el-card>
  </div>
</template>

<script setup>
import { useUserStore } from '../stores/user';
import { ElButton, ElCard } from 'element-plus'; // 导入 Element Plus 组件

const userStore = useUserStore();

const handleLogout = () => {
  userStore.logout();
};
</script>

<style scoped>
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #e9eef3;
  text-align: center;
}
.home-card {
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 500px;
  max-width: 90%;
}
h1 {
  color: #333;
  margin-bottom: 20px;
}
p {
  color: #666;
  margin-bottom: 30px;
}
</style>