    @staticmethod
    def _generate_shensha_predictions(predictions: Dict[str, List[str]], liunian_shensha: List[Dict[str, Any]]):
        """根据神煞标签生成预测 - 完全数据驱动，无硬编码"""
        try:
            # 神煞标签到预测类型的映射
            tag_predictions = {
                # 贵人类
                "贵人": {
                    "career": ["工作上有权威人士相助，困难时期更容易获得帮助"],
                    "timing": ["贵人相助，重要时机把握更准确"]
                },
                "助力": {
                    "career": ["得到他人帮助，事业发展更顺利"],
                    "strategy": ["善用人际关系，寻求贵人支持"]
                },
                "提携": {
                    "career": ["有长辈或上司提携，职业发展有贵人相助"],
                    "timing": ["适合寻求指导和建议的时期"]
                },
                # 文昌类
                "文昌": {
                    "career": ["学习考试运势极佳，文思敏捷"],
                    "strategy": ["可报考各类证书或学历提升"]
                },
                "智慧": {
                    "career": ["思维敏捷，决策明智"],
                    "strategy": ["发挥智慧优势，从事脑力工作"]
                },
                "学业": {
                    "career": ["学习运势佳，适合深造或培训"],
                    "strategy": ["投资教育和技能提升"]
                },
                # 驿马类
                "变动": {
                    "career": ["有出行、迁移或职业变动机会"],
                    "strategy": ["可考虑异地发展或职业转换"]
                },
                "出行": {
                    "career": ["出差或异地工作机会增多"],
                    "strategy": ["把握出行机会，拓展视野"]
                },
                "活跃": {
                    "career": ["工作活跃，变化较多"],
                    "timing": ["适合主动出击的时期"]
                },
                # 桃花类
                "魅力": {
                    "relationship": ["桃花运旺盛，感情生活活跃"],
                    "timing": ["感情运势在春夏季更为活跃"]
                },
                "异性缘": {
                    "relationship": ["异性缘佳，感情机会增多"],
                    "strategy": ["把握感情机会，但要理性选择"]
                },
                "人缘": {
                    "relationship": ["人际关系和谐，社交活跃"],
                    "career": ["人缘好有助于事业发展"]
                },
                # 华盖类
                "艺术": {
                    "career": ["适合学术研究或艺术创作"],
                    "strategy": ["发挥创意才能，从事文化艺术相关工作"]
                },
                "才华": {
                    "career": ["才华得到发挥，创作灵感丰富"],
                    "strategy": ["发挥个人特长，展示才华"]
                },
                "宗教": {
                    "career": ["适合从事宗教或哲学相关工作"],
                    "strategy": ["可深入学习宗教或哲学"]
                },
                # 负面标签
                "虚空": {
                    "warning": ["投资需格外谨慎，避免空想"],
                    "strategy": ["脚踏实地，避免过于理想化的计划"]
                },
                "失落": {
                    "warning": ["容易感到失落，需要心理调节"],
                    "strategy": ["保持积极心态，寻求支持"]
                },
                "不实": {
                    "warning": ["避免虚假投资，注意识别真伪"],
                    "strategy": ["谨慎决策，多方核实"]
                },
                # 劫煞类
                "奔波": {
                    "warning": ["需防小人，财物安全要注意"],
                    "strategy": ["低调行事，避免炫富，加强风险防范"]
                },
                "劳碌": {
                    "health": ["注意身体健康，避免过度劳累"],
                    "strategy": ["合理安排工作和休息"]
                },
                # 领导类
                "领导": {
                    "career": ["领导能力得到发挥，团队凝聚力强"],
                    "strategy": ["发挥组织协调能力，可承担团队领导角色"]
                },
                "权威": {
                    "career": ["权威地位提升，管理能力增强"],
                    "strategy": ["善用权威影响力，但要避免专横"]
                },
                "统帅": {
                    "career": ["统帅能力突出，适合管理岗位"],
                    "strategy": ["发挥领导才能，带领团队发展"]
                },
                # 禄神类
                "财富": {
                    "wealth": ["财运亨通，收入稳定增长"],
                    "strategy": ["把握财富机会，稳健投资"]
                },
                "享受": {
                    "wealth": ["生活品质提升，享受丰富"],
                    "strategy": ["适度享受，但要控制消费"]
                },
                "地位": {
                    "career": ["社会地位提升，受人尊敬"],
                    "strategy": ["维护良好形象，承担社会责任"]
                }
            }
            
            # 遍历流年神煞，根据标签生成预测
            for shensha in liunian_shensha:
                shensha_name = shensha.get("name", "")
                positive_tags = shensha.get("positive_tags", [])
                negative_tags = shensha.get("negative_tags", [])
                
                # 处理正面标签
                for tag in positive_tags:
                    if tag in tag_predictions:
                        tag_prediction = tag_predictions[tag]
                        for category, messages in tag_prediction.items():
                            for message in messages:
                                enhanced_message = f"流年逢{shensha_name}，{message}"
                                if enhanced_message not in predictions[category]:
                                    predictions[category].append(enhanced_message)
                
                # 处理负面标签
                for tag in negative_tags:
                    if tag in tag_predictions:
                        tag_prediction = tag_predictions[tag]
                        for category, messages in tag_prediction.items():
                            for message in messages:
                                enhanced_message = f"流年逢{shensha_name}，{message}"
                                if enhanced_message not in predictions[category]:
                                    predictions[category].append(enhanced_message)
                
                # 特殊处理：如果神煞有特定的相互作用标签
                all_tags = positive_tags + negative_tags
                if "冲动" in all_tags:
                    predictions["warning"].append(f"流年逢{shensha_name}，行动力增强但易冲动，需要理性决策")
                if "合动" in all_tags:
                    predictions["strategy"].append(f"流年逢{shensha_name}，动力较稳定，适合稳健发展")
                if "虚动" in all_tags:
                    predictions["warning"].append(f"流年逢{shensha_name}，动中有阻，需要耐心等待")
                if "有制" in all_tags:
                    predictions["strategy"].append(f"流年逢{shensha_name}，有制化力量，反主权威发挥")
                if "无制" in all_tags:
                    predictions["warning"].append(f"流年逢{shensha_name}，无制化，需要克制冲动")
                if "得用" in all_tags:
                    predictions["strategy"].append(f"流年逢{shensha_name}，为喜用神，作用力增强")
                if "失用" in all_tags:
                    predictions["warning"].append(f"流年逢{shensha_name}，为忌神，影响力减弱")
                
        except Exception as e:
            logger.error(f"生成神煞预测失败: {e}")
            predictions["warning"].append("神煞分析出现异常，请谨慎参考")
