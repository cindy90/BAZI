<template>
  <div class="bazi-result-container">
    <el-card class="result-card" v-if="baziData">
      <template #header>
        <div class="card-header">
          <span>八字排盘结果</span>
          <el-button type="primary" @click="goBackToCalculator" class="back-button">返回排盘</el-button>
        </div>
      </template>      <el-descriptions title="基本信息" border :column="2" class="mb-20">
        <el-descriptions-item label="姓名">{{ baziData.original_name || '未填写' }}</el-descriptions-item>
        <el-descriptions-item label="性别">{{ baziData.original_gender || '未选择' }}</el-descriptions-item>
        <el-descriptions-item label="出生时间">{{ baziData.birth_datetime_display || '暂无' }}</el-descriptions-item>
        <el-descriptions-item label="出生地点">{{ baziData.original_birth_place || '未填写' }}</el-descriptions-item>
        <!-- 地理位置信息 -->
        <el-descriptions-item label="地理位置" v-if="baziData.location_info">
          <div v-if="baziData.location_info.province || baziData.location_info.city">
            <span>{{ baziData.location_info.province }}{{ baziData.location_info.city }}</span>
            <span v-if="baziData.location_info.longitude && baziData.location_info.latitude">
              ({{ baziData.location_info.longitude.toFixed(4) }}°E, {{ baziData.location_info.latitude.toFixed(4) }}°N)
            </span>
          </div>
        </el-descriptions-item>
        <!-- 真太阳时校正信息 -->
        <el-descriptions-item label="真太阳时校正" v-if="baziData.location_info && baziData.location_info.correction_applied">
          <div>
            <p>校正前：{{ baziData.location_info.original_time ? new Date(baziData.location_info.original_time).toLocaleString() : '暂无' }}</p>
            <p>校正后：{{ baziData.location_info.corrected_time ? new Date(baziData.location_info.corrected_time).toLocaleString() : '暂无' }}</p>
            <p>经度时差：{{ baziData.location_info.longitude_diff_minutes ? baziData.location_info.longitude_diff_minutes.toFixed(1) : '0' }}分钟</p>
            <p>均时差：{{ baziData.location_info.equation_of_time_minutes ? baziData.location_info.equation_of_time_minutes.toFixed(1) : '0' }}分钟</p>
          </div>
        </el-descriptions-item>
        <el-descriptions-item label="生肖">{{ baziData.zodiac_sign || '暂无' }}</el-descriptions-item>
        <el-descriptions-item label="日主五行">{{ baziData.day_master_element || '暂无' }}</el-descriptions-item>
        <el-descriptions-item label="日主旺衰">{{ baziData.day_master_strength || '暂无数据' }}</el-descriptions-item>
      </el-descriptions>

      <el-descriptions title="四柱干支" border :column="4" class="mb-20">
        <el-descriptions-item label="年柱">{{ baziData.bazi_characters.year_stem }}{{ baziData.bazi_characters.year_branch }}</el-descriptions-item>
        <el-descriptions-item label="月柱">{{ baziData.bazi_characters.month_stem }}{{ baziData.bazi_characters.month_branch }}</el-descriptions-item>
        <el-descriptions-item label="日柱">{{ baziData.bazi_characters.day_stem }}{{ baziData.bazi_characters.day_branch }}</el-descriptions-item>
        <el-descriptions-item label="时柱">{{ baziData.bazi_characters.hour_stem }}{{ baziData.bazi_characters.hour_branch }}</el-descriptions-item>
      </el-descriptions>

      <h3 class="section-title">五行得分</h3>
      <el-descriptions v-if="Object.keys(baziData.five_elements_score).length > 0" border :column="5" class="mb-20">
        <el-descriptions-item label="金">{{ baziData.five_elements_score.金 || 0 }}</el-descriptions-item>
        <el-descriptions-item label="木">{{ baziData.five_elements_score.木 || 0 }}</el-descriptions-item>
        <el-descriptions-item label="水">{{ baziData.five_elements_score.水 || 0 }}</el-descriptions-item>
        <el-descriptions-item label="火">{{ baziData.five_elements_score.火 || 0 }}</el-descriptions-item>
        <el-descriptions-item label="土">{{ baziData.five_elements_score.土 || 0 }}</el-descriptions-item>
      </el-descriptions>
      <p v-else class="section-placeholder">五行得分：暂无数据</p>

      <h3 class="section-title">四柱详细信息</h3>
      <el-descriptions border :column="2" class="mb-20">
        <el-descriptions-item label="年柱信息">
          <p>天干十神：{{ baziData.gan_zhi_info.year_pillar.ten_god || '暂无' }}</p>
          <p>地支藏干：{{ baziData.gan_zhi_info.year_pillar.hidden_stems || '暂无' }}</p>
          <p>纳音：{{ baziData.na_yin.year_na_yin || '暂无' }}</p>
        </el-descriptions-item>
        <el-descriptions-item label="月柱信息">
          <p>天干十神：{{ baziData.gan_zhi_info.month_pillar.ten_god || '暂无' }}</p>
          <p>地支藏干：{{ baziData.gan_zhi_info.month_pillar.hidden_stems || '暂无' }}</p>
          <p>纳音：{{ baziData.na_yin.month_na_yin || '暂无' }}</p>
        </el-descriptions-item>
        <el-descriptions-item label="日柱信息">
          <p>天干十神：{{ baziData.gan_zhi_info.day_pillar.ten_god || '暂无' }}</p>
          <p>地支藏干：{{ baziData.gan_zhi_info.day_pillar.hidden_stems || '暂无' }}</p>
          <p>纳音：{{ baziData.na_yin.day_na_yin || '暂无' }}</p>
        </el-descriptions-item>
        <el-descriptions-item label="时柱信息">
          <p>天干十神：{{ baziData.gan_zhi_info.hour_pillar.ten_god || '暂无' }}</p>
          <p>地支藏干：{{ baziData.gan_zhi_info.hour_pillar.hidden_stems || '暂无' }}</p>
          <p>纳音：{{ baziData.na_yin.hour_na_yin || '暂无' }}</p>
        </el-descriptions-item>
      </el-descriptions>      <h3 class="section-title">宫位信息</h3>
      <el-descriptions v-if="baziData.palace_info && (baziData.palace_info.tai_yuan || baziData.palace_info.ming_gong || baziData.palace_info.shen_gong || baziData.palace_info.gong)" border :column="3" class="mb-20">
        <el-descriptions-item label="胎元">{{ baziData.palace_info.tai_yuan || '暂无' }} ({{ baziData.palace_info.tai_yuan_na_yin || '暂无' }})</el-descriptions-item>
        <el-descriptions-item label="命宫">{{ baziData.palace_info.ming_gong || '暂无' }} ({{ baziData.palace_info.ming_gong_na_yin || '暂无' }})</el-descriptions-item>
        <el-descriptions-item label="身宫">{{ baziData.palace_info.shen_gong || '暂无' }} ({{ baziData.palace_info.shen_gong_na_yin || '暂无' }}) 
          <span v-if="baziData.palace_info.shen_gong_location">- 位于{{ baziData.palace_info.shen_gong_location }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="胎息">{{ baziData.palace_info.tai_xi || '暂无' }} ({{ baziData.palace_info.tai_xi_na_yin || '暂无' }})</el-descriptions-item>
        <el-descriptions-item label="方位">{{ baziData.palace_info.direction || '暂无' }}</el-descriptions-item>
      </el-descriptions>
      <p v-else class="section-placeholder">宫位信息：暂无数据</p>

      <!-- 十二宫位详细信息 -->
      <h3 class="section-title">十二宫位详细信息</h3>
      <div v-if="baziData.palace_info && baziData.palace_info.twelve_palaces" class="twelve-palaces-container mb-20">
        <el-row :gutter="20">
          <el-col :span="12" v-for="(palaceInfo, palaceName) in baziData.palace_info.twelve_palaces" :key="palaceName" class="palace-item-col">
            <el-card class="palace-card" shadow="hover">
              <template #header>
                <div class="palace-header">
                  <span class="palace-name">{{ palaceName }}</span>
                  <span class="palace-ganzhi">{{ palaceInfo.gan_zhi || '暂无' }}</span>
                </div>
              </template>
              <div class="palace-content">
                <p><strong>天干：</strong>{{ palaceInfo.gan || '暂无' }}</p>
                <p><strong>地支：</strong>{{ palaceInfo.zhi || '暂无' }}</p>
                <p class="palace-description">{{ palaceInfo.description || '暂无描述' }}</p>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <p v-else class="section-placeholder">十二宫位信息：暂无数据</p>      <h3 class="section-title">大运信息</h3>
      <!-- 大运分析质量统计 -->
      <div v-if="baziData.major_cycles && baziData.major_cycles.length > 0" class="mb-20">
        <el-alert 
          :title="`大运分析统计：${detailedAnalysisCount}/${baziData.major_cycles.length} 个大运包含详细分析 (${(detailedAnalysisCount/baziData.major_cycles.length*100).toFixed(0)}%)`"
          :type="detailedAnalysisCount >= baziData.major_cycles.length * 0.8 ? 'success' : detailedAnalysisCount >= baziData.major_cycles.length * 0.5 ? 'warning' : 'info'"
          show-icon
          :closable="false">          <template #default>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span>AI增强分析: {{ aiEnhancedCount }}/{{ baziData.major_cycles.length }} 个</span>              <el-button v-if="detailedAnalysisCount < baziData.major_cycles.length" size="small" type="primary" 
                         @click="regenerateDetailedAnalysis" 
                         :loading="regeneratingAnalysis"
                         :disabled="regeneratingAnalysis">
                🔄 {{ regeneratingAnalysis ? '生成中...' : '重新生成完整分析' }}
              </el-button>
            </div>
            <!-- 重新生成进度提示 -->
            <div v-if="regeneratingAnalysis" style="margin-top: 15px; padding: 15px; background: #fff3cd; border-radius: 6px;">
              <div style="display: flex; align-items: center; gap: 10px; color: #856404;">
                <div style="font-size: 20px;">⏳</div>
                <div>
                  <p style="margin: 0; font-weight: bold;">正在重新生成所有大运的AI详细分析...</p>
                  <p style="margin: 5px 0 0 0; font-size: 13px;">这可能需要30-60秒时间，请耐心等待</p>
                </div>
              </div>
            </div>
          </template>
        </el-alert>
      </div>
      
      <div v-if="baziData.major_cycles && baziData.major_cycles.length > 0" class="major-cycles-container mb-20">
        <!-- 传统大运表格 - 简洁视图 -->
        <el-table :data="baziData.major_cycles" border style="width: 100%" class="mb-20" v-if="!showDetailedDayun">
          <el-table-column prop="start_year" label="开始年份" width="100">
              <template #default="{ row }">{{ row.start_year || '暂无' }}</template>
          </el-table-column>
          <el-table-column prop="end_year" label="结束年份" width="100">
              <template #default="{ row }">{{ row.end_year || '暂无' }}</template>
          </el-table-column>
          <el-table-column prop="gan_zhi" label="大运干支" width="100"></el-table-column>
          <el-table-column prop="start_age" label="起运年龄" width="100">
              <template #default="{ row }">{{ row.start_age || '暂无' }}</template>
          </el-table-column>
          <el-table-column label="十神" width="100">
               <template #default="{ row }">{{ row.shishen || row.ten_gods_gan || '暂无' }}</template>
          </el-table-column>
          <el-table-column prop="hidden_stems_zhi" label="地支藏干" width="120">
               <template #default="{ row }">{{ row.hidden_stems_zhi || '暂无' }}</template>
          </el-table-column>
          <el-table-column label="分析方法" width="120">
               <template #default="{ row }">
                 <el-tag v-if="row.analysis_method === 'comprehensive'" type="success" size="small">高级分析</el-tag>
                 <el-tag v-else-if="row.calculation_method === 'traditional_precise'" type="primary" size="small">传统精准</el-tag>
                 <el-tag v-else type="info" size="small">基础分析</el-tag>
               </template>
          </el-table-column>
        </el-table>
        
        <!-- 高级大运详细分析 - 卡片视图 -->
        <div v-if="showDetailedDayun" class="detailed-dayun-cards">
          <el-row :gutter="20">
            <el-col :span="24" v-for="(cycle, index) in baziData.major_cycles.slice(0, 6)" :key="index" class="mb-20">
              <el-card class="dayun-card" shadow="hover">
                <template #header>
                  <div class="dayun-header">
                    <span class="dayun-title">大运 {{ index + 1 }}: {{ cycle.gan_zhi }}</span>
                    <div class="dayun-basic">
                      <el-tag type="primary" size="small">{{ cycle.start_age }}岁 - {{ parseInt(cycle.start_age) + 9 }}岁</el-tag>
                      <el-tag type="success" size="small">{{ cycle.start_year }} - {{ cycle.end_year }}</el-tag>
                      <el-tag v-if="cycle.shishen" type="warning" size="small">{{ cycle.shishen }}</el-tag>
                    </div>
                  </div>
                </template>
                
                <div class="dayun-content">
                  <!-- 五行变化 -->
                  <div v-if="cycle.main_wuxing && cycle.main_wuxing.length > 0" class="dayun-section">
                    <h4>🌟 主导五行</h4>
                    <div class="wuxing-tags">
                      <el-tag v-for="wuxing in cycle.main_wuxing" :key="wuxing" 
                              :type="getWuxingTagType(wuxing)" size="small" class="mr-5">
                        {{ wuxing }}
                      </el-tag>
                    </div>
                  </div>
                  
                  <!-- 五行平衡分析 -->
                  <div v-if="cycle.balance_analysis" class="dayun-section">
                    <h4>⚖️ 平衡分析</h4>
                    <p class="analysis-text">{{ cycle.balance_analysis }}</p>
                  </div>
                  
                  <!-- 互动关系 -->
                  <div v-if="cycle.interactions && cycle.interactions.length > 0" class="dayun-section">
                    <h4>🔄 互动关系</h4>
                    <div class="interactions-grid">
                      <div v-for="(interaction, idx) in cycle.interactions.slice(0, 4)" :key="idx" class="interaction-item">
                        <el-tag :type="getInteractionTagType(interaction.influence)" size="small" class="mb-5">
                          {{ interaction.pillar }}{{ interaction.type }}
                        </el-tag>
                        <span class="interaction-desc">{{ interaction.relation }}</span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 趋势分析 -->
                  <div v-if="cycle?.trend" class="dayun-section">
                    <h4>📈 运势趋势</h4>
                    <p class="trend-text">{{ cycle.trend }}</p>
                  </div>
                  
                  <!-- 建议 -->
                  <div v-if="cycle?.advice" class="dayun-section">
                    <h4>💡 建议指导</h4>
                    <p class="advice-text">{{ cycle.advice }}</p>
                  </div>
                    <!-- DeepSeek深度分析 -->
                  <div v-if="cycle?.deep_analysis" class="dayun-section">
                    <h4>🧠 AI深度解读</h4>
                    <div class="deep-analysis-content">
                      <p class="deep-analysis-text">{{ cycle.deep_analysis }}</p>
                      <div v-if="cycle?.deepseek_enhanced" class="ai-badge">
                        <el-tag type="success" size="small" round>✨ AI增强分析</el-tag>
                      </div>
                    </div>
                  </div>                  <!-- 缺失分析提示和操作 -->
                  <div v-if="!cycle?.trend && !cycle?.advice && !cycle?.deep_analysis" class="dayun-section">
                    <el-alert 
                      title="此大运暂无详细分析" 
                      type="info" 
                      show-icon 
                      description="当前大运缺少AI增强分析内容。这可能是因为使用了快速计算模式。">
                    </el-alert>
                    <div style="margin-top: 10px;">
                      <el-button 
                        size="small" 
                        type="primary" 
                        @click="requestDetailedAnalysisForCycle(cycle)"
                        :loading="loadingSingleDayun.has(cycle.gan_zhi)"
                        :disabled="loadingSingleDayun.has(cycle.gan_zhi)"
                      >
                        🔮 {{ loadingSingleDayun.has(cycle.gan_zhi) ? 'AI分析中...' : '获取详细分析' }}
                      </el-button>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
        
        <!-- 切换按钮 -->
        <div class="dayun-toggle">
          <el-button @click="showDetailedDayun = !showDetailedDayun" type="primary">
            {{ showDetailedDayun ? '简洁视图' : '详细分析' }}
          </el-button>
        </div>
      </div>
      <p v-else class="section-placeholder">大运信息：暂无数据</p><div v-if="baziData.current_year_fortune && (baziData.current_year_fortune.year || baziData.current_year_fortune.gan_zhi || baziData.current_year_fortune.analysis)" class="mb-20">
        <h3 class="section-title">当年运势 ({{ baziData.current_year_fortune.year }}年)</h3>
        
        <!-- 基础信息 -->
        <el-descriptions border :column="3" class="mb-20">
          <el-descriptions-item label="年份">{{ baziData.current_year_fortune.year || '暂无' }}</el-descriptions-item>
          <el-descriptions-item label="流年干支">{{ baziData.current_year_fortune.gan_zhi || '暂无' }}</el-descriptions-item>
          <el-descriptions-item label="年龄">{{ baziData.current_year_fortune.age || '暂无' }}岁</el-descriptions-item>
        </el-descriptions>        
        <p class="basic-analysis"><strong>基础分析：</strong>{{ baziData.current_year_fortune.analysis || '暂无' }}</p>
          <!-- AI解读按钮 -->
        <div class="ai-analysis-section" style="text-align: center; margin: 20px 0;">
          <el-button 
            v-if="!hasDetailedAnalysis"
            type="success" 
            size="large"
            @click="generateDetailedAnalysis"
            :loading="loadingDetailedAnalysis"
            :disabled="loadingDetailedAnalysis"
            style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); border: none;"
          >
            🧠 {{ loadingDetailedAnalysis ? 'AI分析中...' : '获取AI解读' }}
          </el-button>
          <el-button 
            v-else
            type="warning" 
            size="large"
            @click="generateDetailedAnalysis"
            :loading="loadingDetailedAnalysis"
            :disabled="loadingDetailedAnalysis"
          >
            🔄 {{ loadingDetailedAnalysis ? 'AI分析中...' : '重新分析' }}
          </el-button>
        </div>

        <!-- AI分析进度提示 -->
        <div v-if="loadingDetailedAnalysis" class="ai-progress" style="text-align: center; margin: 20px 0; padding: 20px; background: #fff3cd; border-radius: 8px;">
          <div style="font-size: 24px; color: #856404; margin-bottom: 10px;">⏳</div>
          <p style="margin: 0; color: #856404;">AI正在深度分析您的八字运势，请耐心等待...</p>
          <p style="margin: 5px 0 0 0; color: #6c757d; font-size: 14px;">这可能需要10-30秒时间</p>
        </div>
        
        <!-- 详细分析（如果有的话） -->
        <div v-if="baziData.current_year_fortune.detailed_analysis && Object.keys(baziData.current_year_fortune.detailed_analysis).length > 0" class="detailed-fortune-analysis">
          <h4 class="detailed-title">详细运势解读</h4>
          
          <el-collapse accordion class="fortune-collapse">            <el-collapse-item name="overall" v-if="baziData.current_year_fortune.detailed_analysis.overall_fortune">
              <template #title>
                <span class="collapse-title">🌟 整体运势概况</span>
              </template>
              <div class="analysis-content">{{ baziData.current_year_fortune.detailed_analysis.overall_fortune }}</div>
            </el-collapse-item>
            
            <el-collapse-item name="career" v-if="baziData.current_year_fortune.detailed_analysis.career_wealth">
              <template #title>
                <span class="collapse-title">💼 事业财运</span>
              </template>
              <div class="analysis-content">{{ baziData.current_year_fortune.detailed_analysis.career_wealth }}</div>
            </el-collapse-item>
            
            <el-collapse-item name="love" v-if="baziData.current_year_fortune.detailed_analysis.love_marriage">
              <template #title>
                <span class="collapse-title">💕 感情婚姻</span>
              </template>
              <div class="analysis-content">{{ baziData.current_year_fortune.detailed_analysis.love_marriage }}</div>
            </el-collapse-item>
            
            <el-collapse-item name="health" v-if="baziData.current_year_fortune.detailed_analysis.health">
              <template #title>
                <span class="collapse-title">🏥 健康状况</span>
              </template>
              <div class="analysis-content">{{ baziData.current_year_fortune.detailed_analysis.health }}</div>
            </el-collapse-item>
            
            <!-- 新增专业分析框架字段 -->
            <el-collapse-item name="strategic" v-if="baziData.current_year_fortune.detailed_analysis.strategic_guidance">
              <template #title>
                <span class="collapse-title">🎯 战略规划</span>
              </template>
              <div class="analysis-content">{{ baziData.current_year_fortune.detailed_analysis.strategic_guidance }}</div>
            </el-collapse-item>
            
            <el-collapse-item name="practical" v-if="baziData.current_year_fortune.detailed_analysis.practical_advice">
              <template #title>
                <span class="collapse-title">🛠️ 实用调节</span>
              </template>
              <div class="analysis-content">{{ baziData.current_year_fortune.detailed_analysis.practical_advice }}</div>
            </el-collapse-item>
            
            <el-collapse-item name="timeframes" v-if="baziData.current_year_fortune.detailed_analysis.key_timeframes">
              <template #title>
                <span class="collapse-title">⏰ 重要时机</span>
              </template>
              <div class="analysis-content">{{ baziData.current_year_fortune.detailed_analysis.key_timeframes }}</div>
            </el-collapse-item>
            
            <el-collapse-item name="agency" v-if="baziData.current_year_fortune.detailed_analysis.personal_agency">
              <template #title>
                <span class="collapse-title">🎪 个人能动性</span>
              </template>
              <div class="analysis-content">{{ baziData.current_year_fortune.detailed_analysis.personal_agency }}</div>
            </el-collapse-item>
            
            <!-- 兼容旧字段 -->
            <el-collapse-item name="reminders" v-if="baziData.current_year_fortune.detailed_analysis.special_reminders">
              <template #title>
                <span class="collapse-title">⚠️ 特别提醒</span>
              </template>
              <div class="analysis-content">{{ baziData.current_year_fortune.detailed_analysis.special_reminders }}</div>
            </el-collapse-item>
            
            <el-collapse-item name="suggestions" v-if="baziData.current_year_fortune.detailed_analysis.improvement_suggestions">
              <template #title>
                <span class="collapse-title">🔮 开运建议</span>
              </template>
              <div class="analysis-content">{{ baziData.current_year_fortune.detailed_analysis.improvement_suggestions }}</div>
            </el-collapse-item>
              <!-- 处理通用分析字段 -->
            <el-collapse-item name="general" v-if="baziData.current_year_fortune.detailed_analysis.overall_analysis">
              <template #title>
                <span class="collapse-title">📖 综合分析</span>
              </template>
              <div class="analysis-content">{{ baziData.current_year_fortune.detailed_analysis.overall_analysis }}</div>
            </el-collapse-item>
            
            <el-collapse-item name="note" v-if="baziData.current_year_fortune.detailed_analysis.note">
              <template #title>
                <span class="collapse-title">📝 备注信息</span>
              </template>
              <div class="analysis-content">{{ baziData.current_year_fortune.detailed_analysis.note }}</div>
            </el-collapse-item>
            
            <!-- 动态显示其他未知字段 -->
            <template v-for="(value, key) in getOtherAnalysisFields()" :key="key">
              <el-collapse-item :name="key" v-if="value">
                <template #title>
                  <span class="collapse-title">🔍 {{ getFieldDisplayName(key) }}</span>
                </template>
                <div class="analysis-content">{{ value }}</div>
              </el-collapse-item>
            </template>
          </el-collapse>
        </div>
        
        <!-- 如果没有详细分析，显示获取按钮 -->
        <div v-else class="no-detailed-analysis">
          <el-alert 
            title="详细运势解读" 
            type="info" 
            description="点击下方按钮获取AI智能分析的详细运势解读，包括事业、财运、感情、健康等多个方面的专业指导。"
            show-icon
            :closable="false"
            class="mb-15"
          />
          <el-button type="primary" @click="generateDetailedAnalysis" :loading="loadingDetailedAnalysis">
            <i class="el-icon-magic-stick"></i>
            获取详细运势解读
          </el-button>
        </div>
      </div>
      <p v-else class="section-placeholder">当年运势：暂无数据</p>

    </el-card>

    <el-empty description="无排盘结果，请返回排盘" v-else></el-empty>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { ElMessage, ElButton, ElCard, ElDescriptions, ElDescriptionsItem, ElTable, ElTableColumn, ElEmpty, ElAlert, ElCollapse, ElCollapseItem } from 'element-plus';
import { useRouter } from 'vue-router';
import axios from '../../plugins/axios';

const baziData = ref(null);
const router = useRouter();
const loadingDetailedAnalysis = ref(false);
const showDetailedDayun = ref(true); // 控制大运详细视图，默认显示详细分析
const regeneratingAnalysis = ref(false); // 重新生成分析的加载状态
const loadingSingleDayun = ref(new Set()); // 记录正在加载的单个大运

// 计算属性：是否已有详细分析
const hasDetailedAnalysis = computed(() => {
  return baziData.value?.current_year_fortune?.detailed_analysis && 
         Object.keys(baziData.value.current_year_fortune.detailed_analysis).length > 0;
});

// 计算属性：大运详细分析统计
const detailedAnalysisCount = computed(() => {
  if (!baziData.value?.major_cycles) return 0;
  return baziData.value.major_cycles.filter(cycle => 
    cycle?.trend || cycle?.advice || cycle?.deep_analysis
  ).length;
});

const aiEnhancedCount = computed(() => {
  if (!baziData.value?.major_cycles) return 0;
  return baziData.value.major_cycles.filter(cycle => cycle?.deepseek_enhanced).length;
});

onMounted(() => {
  const storedResult = localStorage.getItem('lastBaziResult');
  if (storedResult) {
    try {
      baziData.value = JSON.parse(storedResult);
      console.log('Parsed Bazi Data in BaziResult.vue:', baziData.value);
    } catch (e) {
      ElMessage.error('解析排盘结果失败，请重新排盘。');
      console.error(e);
      router.push({ name: 'BaziCalculator' });
    }
  } else {
    ElMessage.warning('没有找到排盘结果，请先进行排盘。');
    router.push({ name: 'BaziCalculator' });
  }
});

const goBackToCalculator = () => {
  router.push({ name: 'BaziCalculator' });
};

// 生成详细运势分析
const generateDetailedAnalysis = async () => {
  if (!baziData.value) {
    ElMessage.error('八字数据不完整，无法生成详细分析');
    return;
  }
  
  loadingDetailedAnalysis.value = true;
  try {
    // 构建请求数据 - 使用保存的原始数据
    const requestData = {
      name: baziData.value.original_name || "用户",
      gender: baziData.value.original_gender || "男",
      birth_datetime: baziData.value.birth_datetime_display || "1990-01-01T12:00:00+08:00",
      is_solar_time: true // 默认使用真太阳时
    };
    
    console.log('Requesting current year AI analysis with data:', requestData);
    
    // 调用新的AI分析端点
    const response = await axios.post('/bazi/current-year-ai-analysis', requestData);
    
    if (response.data && response.data.success && response.data.detailed_analysis) {
      // 更新本地数据
      baziData.value.current_year_fortune.detailed_analysis = response.data.detailed_analysis;
      
      // 更新localStorage
      localStorage.setItem('lastBaziResult', JSON.stringify(baziData.value));
      
      ElMessage.success('AI详细运势分析已生成！');
    } else {
      const errorMsg = response.data?.message || '获取到的分析数据格式不正确';
      ElMessage.warning(errorMsg);
      
      // 如果有错误信息，仍然显示基础分析
      if (response.data?.detailed_analysis) {
        baziData.value.current_year_fortune.detailed_analysis = response.data.detailed_analysis;
        localStorage.setItem('lastBaziResult', JSON.stringify(baziData.value));
      }
    }
    
  } catch (error) {
    console.error('获取详细分析失败:', error);
    ElMessage.error(error.response?.data?.detail || '获取详细分析失败，请稍后重试');  } finally {
    loadingDetailedAnalysis.value = false;
  }
};

// 获取五行标签类型
const getWuxingTagType = (wuxing) => {
  const types = {
    '金': 'warning',
    '木': 'success', 
    '水': 'info',
    '火': 'danger',
    '土': 'primary'
  };
  return types[wuxing] || 'default';
};

// 获取互动关系标签类型
const getInteractionTagType = (influence) => {
  if (influence && influence.includes('正面')) {
    return 'success';
  } else if (influence && influence.includes('负面')) {
    return 'danger';
  } else {
    return 'info';
  }
};

// 获取其他未标准化的分析字段
const getOtherAnalysisFields = () => {
  if (!baziData.value?.current_year_fortune?.detailed_analysis) return {};
  
  const analysis = baziData.value.current_year_fortune.detailed_analysis;
  const standardFields = [
    'overall_fortune', 'career_wealth', 'love_marriage', 'health',
    'strategic_guidance', 'practical_advice', 'key_timeframes', 'personal_agency',
    'special_reminders', 'improvement_suggestions', 'overall_analysis', 'note'
  ];
  
  const otherFields = {};
  for (const [key, value] of Object.entries(analysis)) {
    if (!standardFields.includes(key) && value) {
      otherFields[key] = value;
    }
  }
  
  return otherFields;
};

// 获取字段显示名称
const getFieldDisplayName = (key) => {
  const nameMap = {
    'summary': '总结概述',
    'conclusion': '结论',
    'recommendations': '建议',
    'warnings': '注意事项',
    'additional_info': '补充信息',
    'special_notes': '特别说明',
    'future_outlook': '未来展望',
    'monthly_fortune': '月度运势',
    'lucky_colors': '幸运色彩',
    'lucky_numbers': '幸运数字',
    'favorable_directions': '有利方位'
  };
  return nameMap[key] || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
};

// 重新生成详细分析
const regenerateDetailedAnalysis = async () => {
  if (!baziData.value) {
    ElMessage.error('八字数据不完整，无法重新生成分析');
    return;
  }
  
  regeneratingAnalysis.value = true;
  ElMessage.info('正在重新计算大运详细分析，请稍候...');
  
  try {
    // 重新调用完整分析API
    const requestData = {
      name: baziData.value.original_name || '用户',
      gender: baziData.value.original_gender || '男',
      birth_datetime: baziData.value.birth_datetime_display,
      is_solar_time: true
    };
    
    console.log('Regenerating complete dayun analysis with data:', requestData);
    
    const response = await axios.post('/bazi/calculate-dayun-test', requestData);
    const newResult = response.data;
    
    if (newResult && newResult.major_cycles) {
      // 更新存储的数据
      const updatedResult = {
        ...baziData.value,
        major_cycles: newResult.major_cycles,
        // 保持其他字段不变
      };
      
      baziData.value = updatedResult;
      localStorage.setItem('lastBaziResult', JSON.stringify(updatedResult));
      
      // 统计新的分析结果
      const newDetailedCount = newResult.major_cycles.filter(cycle => 
        cycle?.trend || cycle?.advice || cycle?.deep_analysis
      ).length;
      const newAiCount = newResult.major_cycles.filter(cycle => cycle?.deepseek_enhanced).length;
      
      ElMessage.success(`大运详细分析已更新！生成了 ${newDetailedCount} 个详细分析，其中 ${newAiCount} 个包含AI增强分析`);
    } else {
      ElMessage.warning('重新生成的数据格式异常，请稍后重试');
    }
    
  } catch (error) {
    console.error('重新生成分析失败:', error);
    
    if (error.response?.status === 504 || error.code === 'ECONNABORTED') {
      ElMessage.warning('AI分析超时，可能只有部分大运包含详细分析。您可以使用单个大运分析功能补充');
    } else {
      ElMessage.error(error.response?.data?.detail || '重新生成分析失败，请稍后重试');
    }
  } finally {
    regeneratingAnalysis.value = false;
  }
};

// 为单个大运请求详细分析
const requestDetailedAnalysisForCycle = async (cycle) => {
  if (!baziData.value) {
    ElMessage.error('八字数据不完整，无法生成分析');
    return;
  }
  
  // 添加到加载状态
  loadingSingleDayun.value.add(cycle.gan_zhi);
  ElMessage.info(`正在为大运 ${cycle.gan_zhi} 生成AI详细分析...`);
  
  try {
    // 构建请求数据
    const requestData = {
      name: baziData.value.original_name || "用户",
      gender: baziData.value.original_gender || "男", 
      birth_datetime: baziData.value.birth_datetime_display,
      dayun_gan_zhi: cycle.gan_zhi,
      start_age: cycle.start_age,
      end_age: parseInt(cycle.start_age) + 9,
      is_solar_time: true
    };
      console.log('Requesting single dayun analysis:', requestData);
    
    // 调用单个大运分析端点 - 使用查询参数
    const params = new URLSearchParams({
      cycle_gan_zhi: cycle.gan_zhi,
      cycle_start_year: cycle.start_year || String(new Date().getFullYear() - (parseInt(cycle.start_age) || 0)),
      cycle_end_year: cycle.end_year || String(new Date().getFullYear() - (parseInt(cycle.start_age) || 0) + 9)
    });
    
    const response = await axios.post(`/bazi/single-dayun-analysis?${params.toString()}`, requestData);
    
    if (response.data && response.data.success) {
      // 找到对应的大运并更新分析内容
      const cycleIndex = baziData.value.major_cycles.findIndex(c => c.gan_zhi === cycle.gan_zhi);
      if (cycleIndex !== -1) {
        // 更新大运的分析内容
        const updatedCycle = {
          ...baziData.value.major_cycles[cycleIndex],
          trend: response.data.analysis.trend || '',
          advice: response.data.analysis.advice || '',
          deep_analysis: response.data.analysis.deep_analysis || '',
          deepseek_enhanced: true,
          analysis_method: 'comprehensive'
        };
        
        baziData.value.major_cycles[cycleIndex] = updatedCycle;
        
        // 更新localStorage
        localStorage.setItem('lastBaziResult', JSON.stringify(baziData.value));
        
        ElMessage.success(`大运 ${cycle.gan_zhi} 的AI详细分析已生成！`);
      } else {
        ElMessage.warning('无法找到对应的大运周期');
      }
    } else {
      const errorMsg = response.data?.message || '分析生成失败';
      ElMessage.warning(errorMsg);
    }
    
  } catch (error) {
    console.error('生成单个大运分析失败:', error);
    
    if (error.response?.status === 504 || error.code === 'ECONNABORTED') {
      ElMessage.warning('AI分析超时，请稍后重试或使用重新生成完整分析功能');
    } else {
      ElMessage.error(error.response?.data?.detail || '生成分析失败，请稍后重试');
    }
  } finally {
    // 从加载状态中移除
    loadingSingleDayun.value.delete(cycle.gan_zhi);
  }
};
</script>

<style scoped>
/* ... (样式部分保持不变，包括 .section-placeholder) ... */
.bazi-result-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 20px;
}

.result-card {
  width: 900px;
  max-width: 95%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 20px;
}

.back-button {
    margin-left: 20px;
}

.section-title {
    margin-top: 30px;
    margin-bottom: 15px;
    color: #303133;
    font-size: 18px;
    border-left: 4px solid #409EFF;
    padding-left: 10px;
}

.section-placeholder {
    text-align: center;
    color: #909399;
    padding: 10px 0;
    border: 1px dashed #DCDFE6;
    border-radius: 4px;
    margin-bottom: 20px;
}

.mb-20 {
    margin-bottom: 20px;
}

.el-descriptions-item__content p {
    margin: 0;
    line-height: 1.5;
}

/* 十二宫位样式 */
.twelve-palaces-container {
    padding: 10px 0;
}

.palace-item-col {
    margin-bottom: 20px;
}

.palace-card {
    height: 100%;
    transition: all 0.3s;
}

.palace-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.palace-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.palace-name {
    font-weight: bold;
    color: #303133;
    font-size: 16px;
}

.palace-ganzhi {
    color: #409EFF;
    font-weight: bold;
    font-size: 14px;
    background: #f0f9ff;
    padding: 2px 8px;
    border-radius: 4px;
}

.palace-content {
    font-size: 14px;
    line-height: 1.6;
}

.palace-content p {
    margin: 8px 0;
}

.palace-description {
    color: #606266;
    font-size: 13px;
    margin-top: 12px;
    padding-top: 8px;
    border-top: 1px solid #f0f0f0;
    line-height: 1.5;
}

/* 当年运势详细分析样式 */
.basic-analysis {
    margin: 15px 0;
    padding: 12px;
    background: #f8f9fa;
    border-radius: 6px;
    color: #606266;
    line-height: 1.6;
}

.detailed-fortune-analysis {
    margin-top: 20px;
}

.detailed-title {
    color: #303133;
    font-size: 16px;
    font-weight: bold;
    margin: 15px 0 10px 0;
    border-left: 4px solid #409EFF;
    padding-left: 10px;
}

.fortune-collapse {
    margin-top: 15px;
}

.collapse-title {
    font-weight: 600;
    color: #303133;
    font-size: 15px;
}

.analysis-content {
    color: #606266;
    line-height: 1.8;
    padding: 15px 20px;
    background: #fafbfc;
    border-radius: 6px;
    margin: 10px 0;
    border-left: 3px solid #409EFF;
    white-space: pre-line;
}

.no-detailed-analysis {
    margin-top: 20px;
    text-align: center;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 8px;
}

.mb-15 {
    margin-bottom: 15px;
}

/* 大运详细分析样式 */
.major-cycles-container {
  margin: 20px 0;
}

.dayun-toggle {
  margin: 20px 0;
  text-align: center;
}

.detailed-dayun-cards {
  margin: 20px 0;
}

.dayun-card {
  border-radius: 8px;
  transition: all 0.3s ease;
}

.dayun-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.dayun-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.dayun-title {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.dayun-basic {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.dayun-content {
  padding: 0;
}

.dayun-section {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.dayun-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.dayun-section h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: bold;
  color: #409EFF;
}

.wuxing-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.interactions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
}

.interaction-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px;
  background: #f8f9fa;
  border-radius: 4px;
}

.interaction-desc {
  font-size: 12px;
  color: #606266;
}

.analysis-text, .trend-text, .advice-text {
  margin: 0;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 4px;
  color: #606266;
  line-height: 1.6;
  font-size: 14px;
}

.trend-text {
  background: #e8f4fd;
  border-left: 4px solid #409EFF;
}

.advice-text {
  background: #f0f9ff;
  border-left: 4px solid #67C23A;
}

.deep-analysis-content {
  position: relative;
}

.deep-analysis-text {
  margin: 0;
  padding: 12px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  line-height: 1.8;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.ai-badge {
  position: absolute;
  top: -8px;
  right: 8px;
}

.ai-badge .el-tag {
  background: linear-gradient(45deg, #FFD700, #FFA500);
  border: none;
  color: #333;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(255, 215, 0, 0.3);
}

.mr-5 {
  margin-right: 5px;
}

.mb-5 {
  margin-bottom: 5px;
}
</style>