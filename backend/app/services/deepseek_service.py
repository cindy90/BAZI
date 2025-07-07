# backend/app/services/deepseek_service.py
import httpx
import json
from typing import Dict, Any, Optional
import os
import re
from datetime import datetime
from fastapi import HTTPException
from .prompt_manager import PromptManager

class DeepSeekService:
    """DeepSeek API服务类，用于生成详细的八字运势解读"""
    
    def __init__(self):
        # 从环境变量或 .env 文件加载DeepSeek API配置
        self.api_key = os.getenv("DEEPSEEK_API_KEY", "")
        self.base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        self.timeout = float(os.getenv("DEEPSEEK_TIMEOUT", "30"))  # 增加到30秒，给AI分析更多时间
        self.temperature = float(os.getenv("DEEPSEEK_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("DEEPSEEK_MAX_TOKENS", "4096")) # 增加Token上限以容纳更复杂的JSON
        
        # 关闭强制模拟数据，使用真实API
        self.force_mock = False
        
        if not self.api_key:
            print("⚠️  DeepSeek API密钥未配置，将使用模拟数据")
            self.force_mock = True
        else:
            print(f"✅ DeepSeek API 已配置 (模型: {self.model}, 温度: {self.temperature})")
            print(f"📡 API地址: {self.base_url}")
            print(f"🔑 API密钥: {self.api_key[:10]}...{self.api_key[-4:] if len(self.api_key) > 14 else 'too_short'}")

    async def generate_comprehensive_analysis(self, bazi_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成对整个命盘的全面分析
        """
        try:
            prompt = PromptManager.generate_comprehensive_analysis_prompt(bazi_data)
            
            if self.api_key and not self.force_mock:
                return await self._call_api_for_structured_json(prompt)
            else:
                # 返回高质量的模拟分析
                return self._get_mock_comprehensive_analysis(bazi_data)
                
        except Exception as e:
            print(f"生成全面分析时发生错误: {e}")
            # 在真实错误场景下，可以返回一个包含错误信息的标准结构
            return {"error": "Failed to generate comprehensive analysis", "details": str(e)}

    async def generate_dayun_analysis(self, bazi_data: Dict[str, Any], dayun_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成对特定大运周期的深入分析
        """
        try:
            prompt = PromptManager.generate_dayun_analysis_prompt(bazi_data, dayun_info)
            
            if self.api_key and not self.force_mock:
                return await self._call_api_for_structured_json(prompt)
            else:
                return self._get_mock_dayun_analysis(dayun_info)
                
        except Exception as e:
            print(f"生成大运深度分析时发生错误: {e}")
            return {"error": "Failed to generate Dayun analysis", "details": str(e)}

    async def generate_liunian_analysis(self, bazi_data: Dict[str, Any], year: int) -> Dict[str, Any]:
        """
        生成对特定流年的深入分析
        """
        try:
            prompt = PromptManager.generate_liunian_analysis_prompt(bazi_data, year)
            
            if self.api_key and not self.force_mock:
                return await self._call_api_for_structured_json(prompt)
            else:
                return self._get_mock_liunian_analysis(year)
                
        except Exception as e:
            print(f"生成流年分析时发生错误: {e}")
            return {"error": "Failed to generate Liunian analysis", "details": str(e)}

    async def generate_detailed_fortune_analysis(self, bazi_data: Dict[str, Any], year: str) -> Dict[str, Any]:
        """
        生成详细的流年运势分析，结合综合分析和流年分析
        """
        try:
            year_int = int(year)
            
            # 如果有API密钥且未强制模拟，调用真实API
            if self.api_key and not self.force_mock:
                # 使用流年分析提示词
                prompt = PromptManager.generate_liunian_analysis_prompt(bazi_data, year_int)
                return await self._call_api_for_structured_json(prompt)
            else:
                # 返回模拟的详细运势分析
                return self._get_mock_detailed_fortune_analysis(bazi_data, year_int)
                
        except Exception as e:
            print(f"生成详细运势分析时发生错误: {e}")
            return {"error": "Failed to generate detailed fortune analysis", "details": str(e)}

    async def _call_api_for_structured_json(self, prompt: str) -> Dict[str, Any]:
        """
        调用 LLM API 并确保返回结构化的 JSON。
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 使用 response_format 强制 JSON 输出
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": PromptManager.get_master_persona_prompt()},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "response_format": {"type": "json_object"} # 强制JSON输出
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data
                )
                response.raise_for_status()  # 如果状态码不是 2xx，则引发异常
                
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # 由于已使用json_object模式，可以直接解析
                return json.loads(content)

            except httpx.HTTPStatusError as e:
                print(f"API 调用失败，状态码: {e.response.status_code}, 响应: {e.response.text}")
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"LLM API call failed: {e.response.text}"
                )
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON 解析失败: {e}")
                print(f"原始响应: {content[:500]}...")
                # 即使在json_object模式下，也可能出现意外的非JSON响应
                return {"error": "Failed to parse LLM response as JSON", "raw_response": content}
            except Exception as e:
                print(f"调用LLM API时发生未知错误: {e}")
                raise HTTPException(status_code=500, detail=f"An unexpected error occurred with the LLM service: {e}")

    # === MOCK DATA METHODS ===

    def _get_mock_comprehensive_analysis(self, bazi_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成模拟的全面分析"""
        return {
            "personality_analysis": {
                "summary": "命主性格稳重，富有责任心，但有时略显固执。",
                "strengths": "诚信、可靠、有毅力。",
                "weaknesses": "缺乏灵活性、不善变通。"
            },
            "life_pattern": {
                "summary": "一生运势平稳，中年后开始走上坡路。",
                "favorable_elements_guidance": "宜多用五行“金”和“水”相关的颜色（白、蓝、黑）、方位（西、北）和行业（金融、贸易）。"
            },
            # ... 其他部分的模拟数据 ...
        }

    def _get_mock_dayun_analysis(self, dayun_info: Dict[str, Any]) -> Dict[str, Any]:
        """生成模拟的大运分析"""
        return {
            "dayun_overview": {
                "summary": f"此 {dayun_info.get('gan_zhi', '')} 大运是人生的重要转折期。",
                "score": "85",
                "key_themes": ["事业突破", "财富增长"]
            },
            # ... 其他部分的模拟数据 ...
        }

    def _get_mock_liunian_analysis(self, year: int) -> Dict[str, Any]:
        """生成模拟的流年分析"""
        return {
            "liunian_overview": {
                "summary": f"{year}年是充满机遇的一年，但也伴随着挑战。",
                "score": "75",
                "key_themes": ["学习成长", "人际关系"]
            },
            "monthly_fortune": [{"month": i, "fortune": f"{i}月运势平稳", "advice": "顺其自然"} for i in range(1, 13)],
            # ... 其他部分的模拟数据 ...
        }

    def _get_mock_detailed_fortune_analysis(self, bazi_data: Dict[str, Any], year: int) -> Dict[str, Any]:
        """生成模拟的详细运势分析"""
        return {
            "detailed_fortune_overview": {
                "year": year,
                "summary": f"{year}年是您人生中的重要转折年份，机遇与挑战并存。",
                "overall_score": "78",
                "key_themes": ["事业发展", "财富增长", "人际关系", "健康调理"]
            },
            "monthly_fortune": [
                {
                    "month": i,
                    "fortune_score": 70 + (i % 3) * 5,
                    "summary": f"{i}月运势{'上升' if i % 2 == 0 else '平稳'}",
                    "advice": f"{i}月宜{'积极进取' if i % 2 == 0 else '稳健保守'}"
                } for i in range(1, 13)
            ],
            "career_analysis": {
                "summary": f"{year}年事业运势整体向好，有晋升机会。",
                "key_opportunities": ["项目合作", "技能提升", "人脉拓展"],
                "challenges": ["竞争激烈", "压力增大"],
                "advice": "把握机遇，稳步前进"
            },
            "wealth_analysis": {
                "summary": f"{year}年财运稳中有升，投资需谨慎。",
                "income_forecast": "正财运佳，偏财运一般",
                "investment_advice": "保守投资，避免高风险项目",
                "favorable_periods": ["3-5月", "9-11月"]
            },
            "relationship_analysis": {
                "summary": f"{year}年人际关系和谐，感情生活美满。",
                "love_fortune": "单身者有桃花运，已婚者感情稳定",
                "family_relations": "家庭和睦，长辈关爱",
                "social_network": "贵人相助，人脉拓展"
            },
            "health_analysis": {
                "summary": f"{year}年健康状况良好，需注意预防。",
                "physical_health": "体质增强，精力充沛",
                "mental_health": "心理平衡，压力可控",
                "prevention_advice": "定期体检，合理作息"
            },
            "lucky_elements": {
                "colors": ["蓝色", "绿色", "白色"],
                "numbers": [1, 6, 8],
                "directions": ["北方", "东方"],
                "months": ["3月", "7月", "10月"]
            },
            "annual_suggestions": [
                "把握机遇，勇于创新",
                "注重健康，平衡工作生活",
                "维护人际关系，扩大社交圈",
                "理性投资，积累财富"
            ],
            "analysis_metadata": {
                "generation_time": datetime.now().isoformat(),
                "analysis_type": "detailed_fortune_mock",
                "bazi_elements": bazi_data.get("day_master_element", "未知")
            }
        }


# 创建全局服务实例
deepseek_service = DeepSeekService()
