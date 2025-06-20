// frontend/src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // <-- 确保这行存在！
import { createPinia } from 'pinia';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import axiosInstance from './plugins/axios'; // 导入 axios 实例

const app = createApp(App);
const pinia = createPinia();

// 注册全局属性
app.config.globalProperties.$http = axiosInstance;

app.use(router); // <-- 确保这行存在！
app.use(pinia);
app.use(ElementPlus);

app.mount('#app');