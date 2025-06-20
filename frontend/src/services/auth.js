// frontend/src/services/auth.js
import axiosInstance from '../plugins/axios';

export const login = async (username, password) => {
    try {
        // 使用 URLSearchParams 将数据编码为 application/x-www-form-urlencoded 格式
        const requestBody = new URLSearchParams();
        requestBody.append('username', username);
        requestBody.append('password', password);

        const response = await axiosInstance.post('/auth/token', requestBody, {
            // 明确设置 Content-Type，确保后端正确解析
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });
        return response.data; // 返回包含 access_token 和 token_type 的数据
    } catch (error) {
        console.error('登录操作失败:', error);
        throw error; // 重新抛出错误，让组件层处理
    }
};

export const registerUser = async (userData) => {
    try {
        // 注册接口仍发送 JSON，因为后端 RegisterRequest 接收 JSON
        const response = await axiosInstance.post('/auth/register', userData);
        return response.data;
    } catch (error) {
        console.error('注册操作失败:', error);
        throw error;
    }
};