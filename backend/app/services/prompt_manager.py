"""
AI Prompt 管理器

负责生成用于调用大语言模型（如 DeepSeek）的结构化、高质量 Prompt。
"""
from typing import Dict, Any, List, Optional


class PromptManager:
    """
    管理和生成用于八字命理分析的 AI Prompt。
    """

    @staticmethod
    def get_master_persona_prompt() -> str:
        """
        定义 AI 的核心角色和行为准则。
        """
        return """
        你是一位深谙中华传统命理学的八字大师，同时具备现代心理学和人生规划的视角。你的分析不仅基于古老的干支五行、神煞、纳音、生旺库墓等理论，还能结合现代生活情境，为用户提供富有洞察力、建设性且易于理解的指导。

        **你的任务是：**
        1.  **精准解读**：基于提供的八字命盘数据，进行全面、深入的分析。
        2.  **结构化输出**：严格按照指定的 JSON 格式返回分析结果，不得有任何偏离。
        3.  **语言风格**：语言既要体现专业性（如使用“官杀”、“印星”、“食伤”等术语），又要亲切易懂，避免使用过于晦涩或宿命论的词汇。多用积极、引导性的语言。
        4.  **逻辑严谨**：所有分析都必须有命理依据，并能在分析文本中简要提及（例如，“因你日主丙火，生于申月，财星当令，故...”)。
        5.  **避免废话**：直接进入核心分析，不要说“好的”、“收到”等多余的话。
        """

    @staticmethod
    def format_bazi_data_for_prompt(bazi_data: Dict[str, Any]) -> str:
        """
        将八字数据格式化为清晰的字符串，供 AI 读取。
        """
        # 为了清晰和简洁，我们只选择最核心的数据传给 AI
        # 核心数据包括：四柱、日主、五行得分、大运、神煞、干支互动

        # 安全地提取数据，避免KeyError
        bazi_info = bazi_data.get('bazi', {})
        year_pillar = bazi_info.get('year', {})
        month_pillar = bazi_info.get('month', {})
        day_pillar = bazi_info.get('day', {})
        hour_pillar = bazi_info.get('hour', {})

        nayin_info = bazi_data.get('nayin', {})
        five_elements_info = bazi_data.get('five_elements', {})
        shen_sha_details = bazi_data.get('shen_sha_details', {})
        interactions = bazi_data.get('interactions', {})

        # 构建神煞字符串
        shen_sha_str = ', '.join([
            f'{details["name"]}({details["position"]})'
            for details in shen_sha_details.values()
            if details.get('active', True) and details.get("position")
        ]) or "无"

        # 构建互动关系字符串
        interaction_parts = []
        if isinstance(interactions, dict):
            for interaction_type, interaction_list in interactions.items():
                if interaction_list:
                    for item in interaction_list:
                        interaction_parts.append(f'{item.get("type", "")}: {item.get("combination", "")}')
        interaction_str = '; '.join(interaction_parts) or "无明显互动"

        formatted_str = f"""
        ### 八字命盘核心信息

        - **性别**: {bazi_data.get('gender', '未知')}
        - **阳历生日**: {bazi_data.get('solar_date', '未知')}
        - **四柱**:
            - 年柱: {year_pillar.get('gan', '')}{year_pillar.get('zhi', '')} (纳音: {nayin_info.get('year', '')})
            - 月柱: {month_pillar.get('gan', '')}{month_pillar.get('zhi', '')} (纳音: {nayin_info.get('month', '')})
            - 日柱: {day_pillar.get('gan', '')}{day_pillar.get('zhi', '')} (纳音: {nayin_info.get('day', '')})
            - 时柱: {hour_pillar.get('gan', '')}{hour_pillar.get('zhi', '')} (纳音: {nayin_info.get('hour', '')})
        - **日主**: {day_pillar.get('gan', '')} ({five_elements_info.get('day_master_element', '')})
        - **五行力量分析**:
            - 日主强弱: {five_elements_info.get('strength', '')}
            - 五行得分百分比: {five_elements_info.get('percentage', {})}
            - 喜用神建议: {five_elements_info.get('favorable_elements', '暂无')}
        - **重要神煞**: {shen_sha_str}
        - **干支互动关系**: {interaction_str}
        """
        return formatted_str

    @staticmethod
    def generate_comprehensive_analysis_prompt(bazi_data: Dict[str, Any]) -> str:
        """
        生成对整个命盘的全面分析 Prompt。
        """
        persona = PromptManager.get_master_persona_prompt()
        formatted_data = PromptManager.format_bazi_data_for_prompt(bazi_data)

        return f"""
        {persona}

        ### 用户命盘数据
        {formatted_data}

        ### 分析任务
        请对以上命盘进行一次全面而深入的综合分析。请严格按照以下 JSON 格式返回你的分析结果，确保每个字段都有内容，且分析深刻、具体、有针对性。

        ```json
        {{
            "personality_analysis": {{
                "summary": "对命主核心性格的总体概括。",
                "strengths": "基于命盘分析命主的性格优点，例如创造力、领导力、同情心等。",
                "weaknesses": "基于命盘分析命主需要注意或提升的性格特点。"
            }},
            "life_pattern": {{
                "summary": "对命主一生的整体格局、层次和主要人生趋势的判断。",
                "favorable_elements_guidance": "详细说明喜用神在生活中的应用，例如颜色、方位、行业、数字等。"
            }},
            "career_analysis": {{
                "summary": "对命主事业发展的总体趋势、潜力、适合领域的分析。",
                "suitable_industries": ["行业一", "行业二", "行业三"],
                "development_suggestions": "提供具体的事业发展建议，例如如何利用优势、规避风险。"
            }},
            "wealth_analysis": {{
                "summary": "对命主财运的总体评价，包括财富的来源、规模和稳定性。",
                "wealth_sources": "分析命主的主要财富来源（正财、偏财、食伤生财等）。",
                "financial_suggestions": "提供理财和投资建议。"
            }},
            "relationship_analysis": {{
                "summary": "对命主感情婚姻状况的总体分析。",
                "relationship_pattern": "分析命主的感情模式、对待感情的态度以及与伴侣的互动方式。",
                "partner_suggestions": "对选择伴侣或与伴侣相处提供建议。"
            }},
            "health_analysis": {{
                "summary": "根据五行平衡情况，分析命主需要注意的健康问题。",
                "potential_issues": "列出最需要关注的身体部位或系统（例如：心血管、消化系统、呼吸系统等）。",
                "health_suggestions": "提供具体的养生和保健建议。"
            }}
        }}
        """

    @staticmethod
    def generate_dayun_analysis_prompt(bazi_data: Dict[str, Any], dayun_info: Dict[str, Any]) -> str:
        """
        生成对特定大运周期的深入分析 Prompt。
        """
        persona = PromptManager.get_master_persona_prompt()
        formatted_data = PromptManager.format_bazi_data_for_prompt(bazi_data)
        
        dayun_ganzhi = dayun_info.get('gan_zhi', '未知')
        dayun_range = f"{dayun_info.get('start_age', '')}-{dayun_info.get('end_age', '')}岁"

        return f"""
        {persona}

        ### 用户命盘数据
        {formatted_data}

        ### 分析任务: 大运深度解析
        当前需要分析的大运是 **{dayun_ganzhi}** ({dayun_range})。
        请深入分析此大运干支与原命盘的相互作用，并严格按照以下 JSON 格式返回你的分析结果。

        ```json
        {{
            "dayun_overview": {{
                "summary": "对此十年大运的总体基调、主题和核心影响进行概括。",
                "score": "为此大运打分（1-100），并简要说明理由。",
                "key_themes": ["主题一", "主题二", "主题三"]
            }},
            "career_wealth": {{
                "summary": "分析此大运期间事业和财运的机遇与挑战。",
                "opportunities": "详细描述可能出现的事业和财富机遇。",
                "challenges_and_advice": "指出潜在的风险和挑战，并提供应对建议。"
            }},
            "relationship_health": {{
                "summary": "分析此大运期间感情婚姻和健康状况的总体趋势。",
                "relationship_advice": "提供处理感情、家庭关系的具体建议。",
                "health_advice": "根据大运五行变化，提供针对性的健康和养生建议。"
            }},
            "strategic_suggestions": {{
                "summary": "提供在此十年大运期间的总体战略规划和人生建议。",
                "yearly_focus": "简要说明这十年中，哪些年份可能更关键或需要特别注意。"
            }}
        }}
        ```
        """

    @staticmethod
    def generate_liunian_analysis_prompt(bazi_data: Dict[str, Any], year: int) -> str:
        """
        生成对特定流年的深入分析 Prompt。
        """
        persona = PromptManager.get_master_persona_prompt()
        formatted_data = PromptManager.format_bazi_data_for_prompt(bazi_data)

        # 找到该流年所属的大运
        current_dayun_info = "无"
        if 'major_cycles' in bazi_data:
            for cycle in bazi_data['major_cycles']:
                if cycle.get('start_year', 0) <= year <= cycle.get('end_year', 9999):
                    current_dayun_info = f"{cycle.get('gan_zhi', '')} ({cycle.get('start_age')}-{cycle.get('end_age')}岁)"
                    break

        return f"""
        {persona}

        ### 用户命盘数据
        {formatted_data}

        ### 分析任务: {year}年流年运势深度解析
        - **分析年份**: {year}
        - **所属大运**: {current_dayun_info}

        请将流年与大运、命盘结合，进行三重分析，并严格按照以下 JSON 格式返回你的分析结果。

        ```json
        {{
            "liunian_overview": {{
                "summary": "对 {year} 年整体运势的概括，说明是“吉”还是“凶”，以及主要机遇和挑战领域。",
                "score": "为此流年打分（1-100），并简要说明理由。",
                "key_themes": ["主题一", "主题二", "主题三"]
            }},
            "monthly_fortune": [
                {{ "month": 1, "fortune": "正月运势简评...", "advice": "建议..." }},
                {{ "month": 2, "fortune": "二月运势简评...", "advice": "建议..." }},
                {{ "month": 3, "fortune": "三月运势简评...", "advice": "建议..." }},
                {{ "month": 4, "fortune": "四月运势简评...", "advice": "建议..." }},
                {{ "month": 5, "fortune": "五月运势简评...", "advice": "建议..." }},
                {{ "month": 6, "fortune": "六月运势简评...", "advice": "建议..." }},
                {{ "month": 7, "fortune": "七月运势简评...", "advice": "建议..." }},
                {{ "month": 8, "fortune": "八月运势简评...", "advice": "建议..." }},
                {{ "month": 9, "fortune": "九月运势简评...", "advice": "建议..." }},
                {{ "month": 10, "fortune": "十月运势简评...", "advice": "建议..." }},
                {{ "month": 11, "fortune": "十一月运势简评...", "advice": "建议..." }},
                {{ "month": 12, "fortune": "十二月运势简评...", "advice": "建议..." }}
            ],
            "specific_advice": {{
                "career": "关于 {year} 年事业发展的具体建议。",
                "wealth": "关于 {year} 年财富管理和投资的具体建议。",
                "relationship": "关于 {year} 年感情生活的具体建议。",
                "health": "关于 {year} 年健康方面的具体建议和注意事项。"
            }}
        }}
        ```
        """
