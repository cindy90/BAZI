<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <span>用户登录</span>
        </div>
      </template>
      <el-form :model="form" :rules="rules" ref="ruleFormRef" label-width="0px">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" clearable></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" show-password></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" class="login-button">登录</el-button>
        </el-form-item>
        <el-form-item>
          <el-link type="primary" @click="$router.push('/register')">没有账号？立即注册</el-link>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useUserStore } from '../../stores/user';
import { ElMessage } from 'element-plus';

const userStore = useUserStore();
const ruleFormRef = ref(null);

const form = reactive({
  username: '',
  password: '',
});

const rules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
  ],
});

const handleLogin = async () => {
  if (!ruleFormRef.value) return;
  await ruleFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await userStore.login(form.username, form.password);
        // 登录成功后，Pinia Store 中的 action 已经处理了跳转和 ElMessage 提示
      } catch (error) {
        console.error('登录请求失败:', error);
        // 错误信息已由 Axios 拦截器和 ElMessage 处理，这里可以不显示额外提示
      }
    } else {
      ElMessage.warning('请检查表单输入。');
      return false;
    }
  });
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh; /* 使容器占据整个视口高度 */
  background-color: #f0f2f5; /* 轻微背景色 */
}

.login-card {
  width: 380px; /* 卡片宽度 */
  max-width: 90%; /* 适应小屏幕 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  border-radius: 8px; /* 圆角 */
}

.card-header {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

.login-button {
  width: 100%;
}

.el-link {
  text-align: center;
  display: block; /* 使链接居中 */
  margin-top: 10px;
}
</style>