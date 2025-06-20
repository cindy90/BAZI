// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '../stores/user';
import authRoutes from './modules/auth';
import userRoutes from './modules/user'; // 暂时为空
import Home from '../views/Home.vue';
import NotFound from '../views/NotFound.vue';

// 定义所有路由
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }, // 首页需要登录
  },
  ...authRoutes, // 展开认证相关的路由
  ...userRoutes, // 展开用户相关的路由（目前为空）
  {
    path: '/:pathMatch(.*)*', // 404 页面
    name: 'NotFound',
    component: NotFound,
    meta: { requiresAuth: false },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 全局前置守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore(); // 获取 Pinia Store 实例

  // 每次路由跳转前，尝试从本地存储加载用户状态
  if (!userStore.isLoggedIn) { // 只有在未登录状态才尝试加载，避免重复加载
    userStore.loadUserFromLocalStorage();
  }

  const requiresAuth = to.meta.requiresAuth;
  const isLoggedIn = userStore.isLoggedIn;

  if (requiresAuth && !isLoggedIn) {
    // 如果路由需要认证但用户未登录，重定向到登录页
    next('/login');
  } else if (isLoggedIn && (to.name === 'Login' || to.name === 'Register')) {
    // 如果用户已登录但尝试访问登录或注册页，重定向到主页
    next('/');
  } else {
    // 否则，正常导航
    next();
  }
});

export default router;