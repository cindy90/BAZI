# 🔑 如何配置您的 DeepSeek API 密钥

## 📋 快速配置指南

### 第一步：获取 API 密钥

1. **访问 DeepSeek 平台**

   - 打开浏览器，访问：https://platform.deepseek.com/
   - 点击"注册"或"登录"

2. **注册/登录账户**

   - 使用邮箱或手机号注册
   - 验证账户信息

3. **创建 API 密钥**
   - 登录后进入控制台
   - 找到"API 密钥"或"Keys"选项
   - 点击"创建新密钥"
   - 复制生成的密钥（类似：`sk-xxxxxxxxxxxxxxxxxxxxxxxx`）

### 第二步：配置密钥

1. **找到 .env 文件**

   ```
   八字app项目根目录/.env
   ```

2. **编辑文件内容**
   打开 `.env` 文件，找到这一行：

   ```
   DEEPSEEK_API_KEY=
   ```

   将您的真实 API 密钥填入等号后面：

   ```
   DEEPSEEK_API_KEY=sk-your-actual-api-key-here
   ```

3. **保存文件**
   - Ctrl+S 保存
   - 确保没有额外的空格或引号

### 第三步：验证配置

运行验证脚本：

```bash
python verify_deepseek_config.py
```

看到这个结果表示成功：

```
🎉 恭喜！DeepSeek API 配置完全正确，可以使用 AI 分析功能。
```

## 🔧 当前 .env 文件内容

您的 `.env` 文件应该包含以下内容：

```env
# DeepSeek API 配置
DEEPSEEK_API_KEY=sk-your-actual-api-key-here

# 以下为可选配置，使用默认值即可
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_TIMEOUT=30
DEEPSEEK_TEMPERATURE=0.7
DEEPSEEK_MAX_TOKENS=2000
```

## ⚠️ 重要提醒

### ✅ 正确做法

- 只需要填写 `DEEPSEEK_API_KEY=` 后面的内容
- 保持密钥的完整性，包括 `sk-` 前缀
- 密钥后面不要有多余的空格

### ❌ 常见错误

```env
# 错误：添加了引号
DEEPSEEK_API_KEY="sk-xxxxx"

# 错误：缺少 sk- 前缀
DEEPSEEK_API_KEY=xxxxxxxxxxxxx

# 错误：有多余空格
DEEPSEEK_API_KEY= sk-xxxxx

# 正确格式
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 🚀 测试您的配置

配置完成后，您可以：

1. **验证配置**

   ```bash
   python verify_deepseek_config.py
   ```

2. **测试完整功能**

   ```bash
   python test_deepseek_dayun_integration.py
   ```

3. **启动应用**

   ```bash
   # 后端
   cd backend
   uvicorn app.main:app --reload

   # 前端（新窗口）
   cd frontend
   npm run dev
   ```

## 💡 成功标志

配置成功后，您会看到：

- ✅ 验证脚本显示全部绿色勾号
- ✅ 后端启动时显示：`✅ DeepSeek API 已配置`
- ✅ 八字分析结果中包含 `🧠 AI深度解读` 部分
- ✅ 前端显示 `✨ AI增强分析` 标签

## 🆘 需要帮助？

如果遇到问题：

1. **检查密钥格式**：确保以 `sk-` 开头
2. **检查网络**：确保能访问 DeepSeek API
3. **重启应用**：修改 .env 后需要重启后端服务
4. **查看日志**：检查控制台是否有错误信息

---

**配置完成后，您的八字分析系统将具备强大的 AI 分析能力！** 🎉
