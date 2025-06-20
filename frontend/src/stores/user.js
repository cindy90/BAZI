// frontend/src/stores/user.js
import { defineStore } from 'pinia';
import { login as apiLogin, registerUser as apiRegisterUser } from '../services/auth';
import { ElMessage } from 'element-plus';
import router from '../router'; // 稍后会创建这个文件

export const useUserStore = defineStore('user', {
    state: () => ({
        token: localStorage.getItem('access_token') || null,
        user: JSON.parse(localStorage.getItem('user_info')) || null, // 假设也会存储user信息
    }),
    getters: {
        isLoggedIn: (state) => !!state.token,
        getUserInfo: (state) => state.user,
    },
    actions: {
        async login(username, password) {
            try {
                const data = await apiLogin(username, password);
                this.token = data.access_token;
                // 在实际项目中，登录成功后通常会有一个 /users/me 或类似的API来获取用户详细信息
                // 暂时这里假设登录接口返回的用户信息足够，或者只保存token
                // 如果后端/auth/token只返回token，你需要另一个API获取用户信息
                this.user = { username: username }; // 简化处理，实际应从后端获取完整用户对象

                localStorage.setItem('access_token', this.token);
                localStorage.setItem('user_info', JSON.stringify(this.user)); // 存储简化用户数据

                ElMessage.success('登录成功！');
                router.push('/'); // 登录成功后跳转到首页
            } catch (error) {
                // Axios 拦截器已经处理了 ElMessage 提示，这里只需处理路由或更具体的逻辑
                console.error('登录操作失败', error);
                throw error; // 重新抛出错误，让调用者知道失败
            }
        },
        async register(userData) {
            try {
                const response = await apiRegisterUser(userData);
                ElMessage.success('注册成功！请登录。');
                router.push('/login'); // 注册成功后跳转到登录页
                return response;
            } catch (error) {
                console.error('注册操作失败', error);
                throw error;
            }
        },
        logout() {
            this.token = null;
            this.user = null;
            localStorage.removeItem('access_token');
            localStorage.removeItem('user_info');
            ElMessage.info('您已退出登录。');
            router.push('/login'); // 退出登录后跳转到登录页
        },
        loadUserFromLocalStorage() {
            // 在应用初始化时调用，从本地存储恢复状态
            const token = localStorage.getItem('access_token');
            const userInfo = localStorage.getItem('user_info');
            if (token && userInfo) {
                this.token = token;
                this.user = JSON.parse(userInfo);
            }
        },
    },
});