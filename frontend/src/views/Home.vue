<template>  <div class="home-container">
    <el-card class="home-card">
      <h1>欢迎来到八字算命应用！</h1>
      <p>您已成功登录。</p>
      <p>在这里您可以查询您的八字信息和运势，体验传统易经算卦。</p>
      
      <!-- 功能按钮区域 -->
      <div class="function-buttons">
        <el-button 
          type="primary" 
          size="large"
          @click="goToBaziCalculator"
          class="feature-btn"
        >
          <i class="el-icon-calendar"></i>
          八字排盘
        </el-button>
        
        <el-button 
          type="success" 
          size="large"
          @click="goToIChingCalculator"
          class="feature-btn"
        >
          <i class="el-icon-magic-stick"></i>
          易经算卦
        </el-button>
      </div>
      
      <!-- 功能介绍 -->
      <div class="features-intro">
        <div class="feature-item">
          <h4>📅 八字排盘</h4>
          <p>根据您的出生信息，分析八字命理、大运流年，了解人生运势走向。</p>
        </div>
        <div class="feature-item">
          <h4>🔮 易经算卦</h4>
          <p>运用古老的易经智慧，为您解答人生疑惑，指引人生方向。</p>
        </div>
      </div>
      
      <el-button type="info" @click="handleLogout" class="logout-btn">
        <i class="el-icon-switch-button"></i>
        退出登录
      </el-button>
    </el-card>
  </div>
</template>

<script setup>
import { useUserStore } from '../stores/user';
import { useRouter } from 'vue-router'; // 导入 useRouter
import { ElButton, ElCard } from 'element-plus'; // 导入 Element Plus 组件

const userStore = useUserStore();
const router = useRouter(); // 获取路由实例

const handleLogout = () => {
  userStore.logout();
};

const goToBaziCalculator = () => {
  router.push('/bazi/calculate'); // <-- 确保这函数存在！
};

const goToIChingCalculator = () => {
  router.push('/iching/calculate');
};
</script>

<style scoped>
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  text-align: center;
  padding: 20px;
}

.home-card {
  padding: 50px;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 700px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

h1 {
  color: #333;
  margin-bottom: 15px;
  font-size: 32px;
  font-weight: bold;
}

p {
  color: #666;
  margin-bottom: 20px;
  font-size: 16px;
  line-height: 1.6;
}

.function-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin: 40px 0;
  flex-wrap: wrap;
}

.feature-btn {
  padding: 15px 30px;
  font-size: 16px;
  border-radius: 25px;
  min-width: 150px;
  height: 50px;
  transition: all 0.3s ease;
}

.feature-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.features-intro {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin: 30px 0;
  text-align: left;
}

.feature-item {
  padding: 20px;
  background: linear-gradient(45deg, #f8f9ff 0%, #fff5f5 100%);
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.feature-item h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 18px;
}

.feature-item p {
  margin: 0;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.logout-btn {
  margin-top: 30px;
  padding: 10px 25px;
  border-radius: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-card {
    padding: 30px 20px;
    margin: 0 10px;
  }
  
  .function-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .feature-btn {
    width: 100%;
    max-width: 250px;
  }
  
  .features-intro {
    grid-template-columns: 1fr;
  }
  
  h1 {
    font-size: 24px;
  }
}
</style>