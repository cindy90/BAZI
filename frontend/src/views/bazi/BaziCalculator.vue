<template>
  <div class="bazi-calculator-container">
    <el-card class="bazi-card">
      <template #header>
        <div class="card-header">
          <span>八字排盘</span>
        </div>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名 (可选)"></el-input>
        </el-form-item>        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="form.gender">
            <el-radio value="男">男</el-radio>
            <el-radio value="女">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="出生日期" prop="birthDate">
          <el-date-picker
            v-model="form.birthDate"
            type="date"
            placeholder="选择日期"
            style="width: 100%;"
          ></el-date-picker>
        </el-form-item>        <el-form-item label="出生时间" prop="birthTime">
          <el-time-picker
            v-model="form.birthTime"
            format="HH:mm"
            placeholder="选择时间"
            style="width: 100%;"
          ></el-time-picker>
        </el-form-item>
        <el-form-item label="出生地点" prop="birthPlace">
          <el-input 
            v-model="form.birthPlace" 
            placeholder="请输入出生地点（如：北京市、上海市）"
            clearable
          >
            <template #prepend>
              <el-icon><Location /></el-icon>
            </template>
          </el-input>
          <div class="form-hint">
            <el-text size="small" type="info">
              输入出生地点有助于进行真太阳时校正，提高排盘准确性
            </el-text>
          </div>
        </el-form-item>
        <el-form-item label="真太阳时">
          <el-switch v-model="form.isSolarTime" inactive-text="否" active-text="是"></el-switch>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" class="submit-button">立即排盘</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { ElMessage, ElLoading } from 'element-plus';
import { Location } from '@element-plus/icons-vue';
import axios from '../../plugins/axios';
import router from '../../router'; // 导入 router

const formRef = ref(null);
const form = reactive({
  name: '',
  gender: '',
  birthDate: null,
  birthTime: null,
  birthPlace: '', // 添加出生地点字段
  isSolarTime: true,
});

const rules = reactive({
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' },
  ],
  birthDate: [
    { required: true, message: '请选择出生日期', trigger: 'change' },
  ],
  birthTime: [
    { required: true, message: '请选择出生时间', trigger: 'change' },
  ],
});

const handleSubmit = async () => {
  console.log("handleSubmit function called"); // 添加日志
  if (!formRef.value) return;
  await formRef.value.validate(async (valid) => {
    if (valid) {
      const loading = ElLoading.service({
        lock: true,
        text: '正在排盘...',
        background: 'rgba(0, 0, 0, 0.7)',
      });

      try {
        const year = form.birthDate.getFullYear();
        const month = form.birthDate.getMonth(); // getMonth() 返回 0-11
        const day = form.birthDate.getDate();
        const hour = form.birthTime.getHours();
        const minute = form.birthTime.getMinutes();
        const second = form.birthTime.getSeconds() || 0; // 默认秒为0

        // 组合日期和时间为本地时间对象
        const birthDateTime = new Date(year, month, day, hour, minute, second);

        // 获取本地时区偏移（分钟），并转换为 "+HH:MM" 或 "-HH:MM" 格式
        const offset = birthDateTime.getTimezoneOffset(); // 距离UTC的分钟数，例如-480 (PDT)
        const offsetAbs = Math.abs(offset);
        const offsetHours = Math.floor(offsetAbs / 60);
        const offsetMinutes = offsetAbs % 60;
        const offsetSign = offset > 0 ? '-' : '+'; // UTC偏移是反向的

        const timezoneOffsetString =
          offsetSign +
          String(offsetHours).padStart(2, '0') +
          ':' +
          String(offsetMinutes).padStart(2, '0');

        // 使用 JavaScript 模板字符串 (` `) 正确拼接所有部分
        const finalBirthDateTimeLocalISO =
          `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}T` +
          `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}:${String(second).padStart(2, '0')}` +
          timezoneOffsetString;
        
        const requestData = {
          name: form.name || null,
          gender: form.gender,
          birth_datetime: finalBirthDateTimeLocalISO,
          birth_place: form.birthPlace || null, // 添加出生地点
          analysis_year: year.toString(), // 当前年份作为分析年份
          is_solar_time: form.isSolarTime,
        };

        console.log("Request Data:", requestData); // 添加日志

        // 使用axios实例进行API调用，确保与其他接口调用方式一致
        const response = await axios.post('/bazi/calculate-dayun-test', requestData);
        
        console.log("Response Data:", response); // 添加日志

        const baziResult = response.data; // 使用axios返回的结果
        // 构建一个包含所有需要的数据的最终对象，确保自定义字段在前，不会被后端同名空字段覆盖
        const finalResultToSave = {
            original_name: form.name || '未填写',
            original_gender: form.gender || '未选择',
            original_birth_place: form.birthPlace || '未填写', // 保存出生地点
            birth_datetime_display: finalBirthDateTimeLocalISO, // 保存用于显示
            ...baziResult, // 展开后端返回的计算结果
        };
        
        console.log('Final object to save to localStorage:', finalResultToSave); // 再次打印确认
        localStorage.setItem('lastBaziResult', JSON.stringify(finalResultToSave));

        ElMessage.success('八字排盘成功！');
        router.push({ name: 'BaziResult' });

      } catch (error) {
        console.error('八字排盘失败:', error); // 增强日志
        if (error.response) {
          // 请求已发出，但服务器响应的状态码不在 2xx 范围内
          console.error('Error Response Data:', error.response.data);
          console.error('Error Response Status:', error.response.status);
          console.error('Error Response Headers:', error.response.headers);
        } else if (error.request) {
          // 请求已发出，但没有收到响应
          console.error('Error Request:', error.request);
        } else {
          // 在设置请求时触发了一个错误
          console.error('Error Message:', error.message);
        }
        const errorMessage = error.response?.data?.detail || error.message || '排盘失败，请稍后再试。';
        ElMessage.error(errorMessage);
      } finally {
        loading.close();
      }
    } else {
      ElMessage.warning('请检查表单输入。');
      return false;
    }
  });
};
</script>

<style scoped>
.bazi-calculator-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
}

.bazi-card {
  width: 480px; /* 适当宽度 */
  max-width: 90%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.card-header {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

.submit-button {
  width: 100%;
  margin-top: 10px;
}

.form-hint {
  margin-top: 5px;
}
</style>