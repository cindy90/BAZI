<template>
  <div class="iching-container">
    <el-card class="iching-card">
      <template #header>
        <div class="card-header">
          <h2>📯 易经算卦</h2>
          <p>通过古老的易经智慧，为您解答人生疑惑</p>
        </div>
      </template>

      <!-- 算卦表单 -->
      <el-form 
        v-if="!showResult" 
        :model="form" 
        :rules="rules" 
        ref="formRef" 
        label-width="120px"
        class="iching-form"
      >
        <el-form-item label="占卜问题" prop="question" required>
          <el-input
            v-model="form.question"
            type="textarea"
            :rows="3"
            placeholder="请输入您想要占卜的问题，例如：近期工作运势如何？感情发展怎样？"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="算卦方式" prop="method">
          <el-radio-group v-model="form.method">
            <el-radio label="coins">掷币法（推荐）</el-radio>
            <el-radio label="time">时间起卦</el-radio>
            <el-radio label="number">数字起卦</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item v-if="form.method === 'number'" label="起卦数字" prop="numbers">
          <el-input-number
            v-for="(num, index) in form.numbers"
            :key="index"
            v-model="form.numbers[index]"
            :min="1"
            :max="999"
            :placeholder="`数字${index + 1}`"
            style="margin-right: 10px; margin-bottom: 10px;"
          />
          <div style="margin-top: 10px; color: #909399; font-size: 12px;">
            请输入3个数字用于起卦计算
          </div>
        </el-form-item>

        <el-form-item label="问卦者信息" prop="gender">
          <el-radio-group v-model="form.gender">
            <el-radio label="male">男</el-radio>
            <el-radio label="female">女</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="补充说明">
          <el-input
            v-model="form.additional_info"
            type="textarea"
            :rows="2"
            placeholder="可选：补充您的具体情况或背景信息"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-form-item>
          <el-button 
            type="primary" 
            @click="submitDivination" 
            :loading="loading"
            size="large"
            style="width: 200px;"
          >
            <i class="el-icon-magic-stick"></i>
            {{ loading ? '正在占卜...' : '开始占卜' }}
          </el-button>
          <el-button @click="resetForm" style="margin-left: 15px;">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 算卦结果 -->
      <div v-if="showResult" class="result-container">
        <div class="result-header">
          <h3>🔮 占卜结果</h3>
          <el-button @click="backToForm" style="float: right;">重新占卜</el-button>
        </div>

        <div class="divination-info">
          <p><strong>问题：</strong>{{ divinationResult.question }}</p>
          <p><strong>占卜时间：</strong>{{ formatTime(divinationResult.divination_time) }}</p>
          <p><strong>算卦方式：</strong>{{ getMethodName(divinationResult.divination_method) }}</p>
        </div>

        <!-- 主卦显示 -->
        <el-card class="hexagram-card" v-if="divinationResult.primary_hexagram">
          <template #header>
            <h4>🔯 主卦：{{ divinationResult.primary_hexagram.name }}</h4>
          </template>
          
          <div class="hexagram-lines">
            <div 
              v-for="line in divinationResult.primary_hexagram.lines.slice().reverse()" 
              :key="line.number"
              class="hexagram-line"
              :class="{ 'changing-line': line.is_changing }"
            >
              <span class="line-number">第{{ line.number }}爻</span>
              <div class="line-symbol">
                <span v-if="line.yin_yang === '阳'" class="yang-line">———</span>
                <span v-else class="yin-line">— —</span>
                <span v-if="line.is_changing" class="changing-mark">变</span>
              </div>
              <span class="line-desc">{{ line.description }}</span>
            </div>
          </div>
        </el-card>

        <!-- 变卦显示 -->
        <el-card 
          class="hexagram-card" 
          v-if="divinationResult.changing_hexagram && hasChangingLines"
        >
          <template #header>
            <h4>🔄 变卦：{{ divinationResult.changing_hexagram.name }}</h4>
          </template>
          
          <div class="hexagram-lines">
            <div 
              v-for="line in divinationResult.changing_hexagram.lines.slice().reverse()" 
              :key="line.number"
              class="hexagram-line"
            >
              <span class="line-number">第{{ line.number }}爻</span>
              <div class="line-symbol">
                <span v-if="line.yin_yang === '阳'" class="yang-line">———</span>
                <span v-else class="yin-line">— —</span>
              </div>
              <span class="line-desc">{{ line.description }}</span>
            </div>
          </div>
        </el-card>

        <!-- 解读结果 -->
        <el-card class="interpretation-card" v-if="divinationResult.interpretation">
          <template #header>
            <h4>📜 卦象解读</h4>
          </template>
          
          <div class="interpretation-content">
            <div class="interpretation-item">
              <h5>🎯 整体含义</h5>
              <p>{{ divinationResult.interpretation.overall_meaning }}</p>
            </div>

            <div class="interpretation-item" v-if="divinationResult.interpretation.fortune_analysis">
              <h5>💫 运势分析</h5>
              <p>{{ divinationResult.interpretation.fortune_analysis }}</p>
            </div>

            <div class="interpretation-item" v-if="divinationResult.interpretation.advice">
              <h5>💡 建议指导</h5>
              <p>{{ divinationResult.interpretation.advice }}</p>
            </div>

            <div class="interpretation-item" v-if="divinationResult.interpretation.changing_lines_analysis">
              <h5>🔄 变爻分析</h5>
              <p>{{ divinationResult.interpretation.changing_lines_analysis }}</p>
            </div>

            <div class="interpretation-item final-guidance">
              <h5>🌟 综合指导</h5>
              <p>{{ divinationResult.interpretation.final_guidance }}</p>
            </div>
          </div>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axiosInstance from '../../plugins/axios'

// 响应式数据
const loading = ref(false)
const showResult = ref(false)
const formRef = ref()

// 表单数据
const form = reactive({
  question: '',
  method: 'coins',
  numbers: [1, 2, 3],
  gender: 'male',
  additional_info: ''
})

// 算卦结果
const divinationResult = ref({})

// 表单验证规则
const rules = {
  question: [
    { required: true, message: '请输入占卜问题', trigger: 'blur' },
    { min: 5, message: '问题至少需要5个字符', trigger: 'blur' }
  ],
  method: [
    { required: true, message: '请选择算卦方式', trigger: 'change' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ]
}

// 计算属性
const hasChangingLines = computed(() => {
  if (!divinationResult.value.primary_hexagram) return false
  return divinationResult.value.primary_hexagram.lines.some(line => line.is_changing)
})

// 方法
const getMethodName = (method) => {
  const methodMap = {
    'coins': '掷币法',
    'time': '时间起卦',
    'number': '数字起卦',
    'yarrow': '蓍草法'
  }
  return methodMap[method] || method
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN')
}

const submitDivination = async () => {
  try {
    // 表单验证
    const valid = await formRef.value.validate()
    if (!valid) return

    loading.value = true

    // 准备请求数据
    const requestData = {
      question: form.question,
      divination_method: form.method,
      method: form.method,
      gender: form.gender,
      divination_time: new Date().toISOString(),
      birth_info: {
        gender: form.gender
      }
    }

    // 如果是数字起卦，添加数字
    if (form.method === 'number') {
      requestData.numbers = form.numbers
      requestData.manual_numbers = form.numbers
    }

    // 如果有补充信息
    if (form.additional_info) {
      requestData.additional_info = form.additional_info
    }

    console.log('发送占卜请求:', requestData)    // 发送请求到后端
    const response = await axiosInstance.post('/iching/test-divine', requestData)
    
    if (response.data.status === 'success') {
      divinationResult.value = response.data.result
      showResult.value = true
      ElMessage.success('占卜完成！')
    } else {
      throw new Error(response.data.message || '占卜失败')
    }

  } catch (error) {
    console.error('占卜错误:', error)
    ElMessage.error(error.response?.data?.detail || error.message || '占卜过程中出现错误')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  formRef.value?.resetFields()
  form.question = ''
  form.method = 'coins'
  form.numbers = [1, 2, 3]
  form.gender = 'male'
  form.additional_info = ''
}

const backToForm = () => {
  showResult.value = false
  divinationResult.value = {}
}
</script>

<style scoped>
.iching-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.iching-card {
  max-width: 800px;
  width: 100%;
  border-radius: 15px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.card-header {
  text-align: center;
}

.card-header h2 {
  color: #333;
  margin-bottom: 8px;
  font-size: 28px;
}

.card-header p {
  color: #666;
  font-size: 14px;
}

.iching-form {
  margin-top: 20px;
}

.result-container {
  margin-top: 20px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f0f0;
}

.result-header h3 {
  color: #333;
  margin: 0;
}

.divination-info {
  background: #f8f9ff;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.divination-info p {
  margin: 5px 0;
  color: #555;
}

.hexagram-card {
  margin-bottom: 20px;
  border-radius: 12px;
}

.hexagram-card :deep(.el-card__header) {
  background: linear-gradient(45deg, #ff9a9e 0%, #fecfef 100%);
  color: white;
}

.hexagram-card h4 {
  margin: 0;
  font-size: 18px;
}

.hexagram-lines {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.hexagram-line {
  display: flex;
  align-items: center;
  padding: 8px;
  background: #fafafa;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.hexagram-line.changing-line {
  background: #fff7e6;
  border-left: 4px solid #faad14;
}

.line-number {
  width: 60px;
  font-weight: bold;
  color: #666;
  font-size: 12px;
}

.line-symbol {
  width: 80px;
  text-align: center;
  font-family: monospace;
  font-size: 16px;
  font-weight: bold;
  position: relative;
}

.yang-line {
  color: #1890ff;
}

.yin-line {
  color: #722ed1;
}

.changing-mark {
  position: absolute;
  top: -5px;
  right: -10px;
  background: #faad14;
  color: white;
  font-size: 10px;
  padding: 1px 4px;
  border-radius: 3px;
}

.line-desc {
  flex: 1;
  color: #333;
  font-size: 13px;
}

.interpretation-card {
  border-radius: 12px;
}

.interpretation-card :deep(.el-card__header) {
  background: linear-gradient(45deg, #a8edea 0%, #fed6e3 100%);
  color: #333;
}

.interpretation-content {
  line-height: 1.6;
}

.interpretation-item {
  margin-bottom: 20px;
  padding: 15px;
  background: #fafafa;
  border-radius: 8px;
  border-left: 4px solid #1890ff;
}

.interpretation-item h5 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 16px;
}

.interpretation-item p {
  margin: 0;
  color: #555;
  line-height: 1.8;
}

.final-guidance {
  background: linear-gradient(45deg, #fff5f5 0%, #f0f9ff 100%);
  border-left-color: #722ed1;
}

.final-guidance h5 {
  color: #722ed1;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .iching-container {
    padding: 10px;
  }
  
  .hexagram-line {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .line-number, .line-symbol {
    width: auto;
    margin-bottom: 5px;
  }
}
</style>
