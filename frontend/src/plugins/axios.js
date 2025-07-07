// frontend/src/plugins/axios.js
import axios from 'axios';
import { ElMessage } from 'element-plus'; // 假设 Element Plus 已经安装

// 创建 Axios 实例
const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000/api/v1', // 后端 API 的基础 URL
    timeout: 60000, // 请求超时时间（60秒，支持AI分析）
    headers: {
        'Content-Type': 'application/json',
    },
});

// 请求拦截器：在发送请求前检查并添加 JWT Token
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器：统一处理错误
axiosInstance.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // 只有当 error.response 存在时才处理
        if (error.response) {
            const { status, data } = error.response;
            let errorMessage = '未知错误，请重试';

            if (data && data.detail) {
                // FastAPI 的 HTTPException 通常会在 detail 字段返回错误信息
                if (typeof data.detail === 'string') {
                    errorMessage = data.detail;
                } else if (Array.isArray(data.detail)) {
                    // 如果是 Pydantic 校验错误，detail 是一个列表
                    errorMessage = data.detail.map(err => `${err.loc.join('.')} - ${err.msg}`).join('; ');
                }
            } else if (error.message) {
                errorMessage = error.message;
            }

            // 特殊处理 401 Unauthorized
            if (status === 401) {
                ElMessage.error('认证失败，请重新登录。');
                localStorage.removeItem('access_token');
                // 重定向到登录页面 (假设路由是 /login)
                // 注意: 这里不能直接使用 useRouter，因为这个文件不是 Vue 组件
                // 实际项目中，通常会在某个全局的 Vue 插件或路由守卫中处理 401 跳转
                // 或者让调用方（service 层）处理重定向
                // 为了简化，这里先只清除 token 并给出提示。
                // 真正的重定向将在 Pinia store 的 logout action 或路由守卫中实现。
            } else if (status === 400) {
                ElMessage.warning(`请求错误: ${errorMessage}`);
            } else if (status === 404) {
                ElMessage.error(`资源未找到: ${errorMessage}`);
            } else if (status === 500) {
                ElMessage.error(`服务器内部错误: ${errorMessage}`);
            } else {
                ElMessage.error(`错误 (${status}): ${errorMessage}`);
            }
        } else {
            // 处理网络错误等情况
            ElMessage.error('网络错误或服务器无响应，请检查您的网络连接。');
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;