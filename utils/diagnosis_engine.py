"""
诊断引擎 - Gemini版本
使用Google Gemini 2.5 Flash进行智能诊断
"""
import json
import re
import time
from pathlib import Path
from typing import Dict, List, Optional
import google.generativeai as genai
from config import (
    GOOGLE_API_KEY, GEMINI_MODEL, GEMINI_GENERATION_CONFIG, 
    GEMINI_SAFETY_SETTINGS, DIAGNOSIS_RULES_PATH, 
    KNOWLEDGE_BASE_DIR, RETRY_CONFIG, DEBUG
)

class DiagnosisEngine:
    def __init__(self):
        """初始化诊断引擎"""
        self.rules = self.load_diagnosis_rules()
        self.prescription_cache = {}
        self.model = None
        self._init_gemini()
    
    def _init_gemini(self):
        """初始化Gemini模型"""
        try:
            if not GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY未设置")
            
            # 配置Gemini
            genai.configure(api_key=GOOGLE_API_KEY)
            
            # 创建模型实例
            self.model = genai.GenerativeModel(
                model_name=GEMINI_MODEL,
                generation_config=GEMINI_GENERATION_CONFIG,
                safety_settings=GEMINI_SAFETY_SETTINGS
            )
            
            if DEBUG:
                print(f"✅ Gemini模型初始化成功: {GEMINI_MODEL}")
                
        except Exception as e:
            print(f"❌ Gemini模型初始化失败: {e}")
            self.model = None
    
    def load_diagnosis_rules(self) -> Dict:
        """加载诊断规则"""
        try:
            with open(DIAGNOSIS_RULES_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ 诊断规则文件未找到: {DIAGNOSIS_RULES_PATH}")
            return {"problem_categories": []}
        except Exception as e:
            print(f"❌ 加载诊断规则失败: {e}")
            return {"problem_categories": []}
    
    def diagnose(self, user_input: str) -> Optional[Dict]:
        """执行诊断"""
        if not user_input or len(user_input.strip()) < 20:
            return None
        
        if not self.model:
            print("❌ Gemini模型未初始化")
            return None
        
        try:
            # 1. 基于规则的初步匹配
            rule_matches = self._rule_based_matching(user_input)
            
            # 2. 使用Gemini进行智能诊断增强
            ai_analysis = self._gemini_enhanced_diagnosis(user_input, rule_matches)
            
            # 3. 结合规则匹配和AI分析
            final_result = self._combine_results(rule_matches, ai_analysis, user_input)
            
            return final_result
            
        except Exception as e:
            print(f"❌ 诊断过程失败: {e}")
            # 如果AI诊断失败，回退到纯规则匹配
            return self._fallback_diagnosis(user_input)
    
    def _rule_based_matching(self, user_input: str) -> List[Dict]:
        """基于规则的匹配"""
        matches = []
        
        for category in self.rules.get("problem_categories", []):
            for rule in category.get("rules", []):
                score = self._calculate_rule_score(user_input, rule)
                if score >= rule.get("threshold", 8):
                    matches.append({
                        "rule": rule,
                        "score": score,
                        "category": category.get("category_name", "")
                    })
        
        # 按得分排序
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches
    
    def _calculate_rule_score(self, user_input: str, rule: Dict) -> float:
        """计算规则匹配分数"""
        keywords = rule.get("keywords", {})
        total_score = 0
        
        # 基础关键词匹配
        for keyword, weight in keywords.items():
            if keyword.lower() in user_input.lower():
                total_score += weight
        
        # Kevin案例特殊处理
        if rule.get("rule_id") == "RULE_TF01_KEVIN_CASE_ENHANCED":
            kevin_keywords = ["合伙人", "技术合伙人", "产品方向", "分歧", "争论"]
            kevin_matches = sum(1 for kw in kevin_keywords if kw in user_input)
            if kevin_matches >= 3:
                total_score *= 1.5  # Kevin案例加权
        
        # 情感模式匹配
        emotional_patterns = rule.get("emotional_patterns", {})
        for pattern, weight in emotional_patterns.items():
            if self._detect_emotional_pattern(user_input, pattern):
                total_score += weight
        
        return total_score
    
    def _detect_emotional_pattern(self, text: str, pattern: str) -> bool:
        """检测情感模式"""
        pattern_keywords = {
            "愤怒情绪": ["生气", "愤怒", "气愤", "火大"],
            "失望情绪": ["失望", "沮丧", "无奈", "绝望"],
            "困惑情绪": ["困惑", "不理解", "想不通", "搞不懂"],
            "归因他人": ["他", "对方", "不懂", "不理解"],
            "自我合理化": ["我认为", "我觉得", "应该", "明明"]
        }
        
        keywords = pattern_keywords.get(pattern, [])
        return any(keyword in text for keyword in keywords)
    
    def _gemini_enhanced_diagnosis(self, user_input: str, rule_matches: List[Dict]) -> Dict:
        """使用Gemini进行智能诊断增强"""
        try:
            # 构建分析提示
            prompt = self._build_analysis_prompt(user_input, rule_matches)
            
            # 调用Gemini进行分析
            response = self._call_gemini_with_retry(prompt)
            
            # 解析AI分析结果
            return self._parse_ai_analysis(response)
            
        except Exception as e:
            print(f"⚠️ Gemini增强诊断失败: {e}")
            return {}
    
    def _build_analysis_prompt(self, user_input: str, rule_matches: List[Dict]) -> str:
        """构建分析提示词"""
        top_matches = rule_matches[:3] if rule_matches else []
        
        prompt = f"""作为认知偏差分析专家，请分析以下创业者的问题描述：

用户输入：
{user_input}

基础规则匹配到的可能认知陷阱：
{[match['rule']['rule_id'] + ': ' + match['rule']['description'] for match in top_matches]}

请从以下角度进行深度分析：

1. 核心认知偏差类型：识别最根本的思维模式问题
2. 情感状态分析：分析用户的情感倾向和心理状态  
3. 问题层次：区分表面问题和深层认知问题
4. 认知突破点：指出最关键的认知转换点

请以JSON格式返回分析结果：
{{
    "primary_cognitive_trap": "识别出的主要认知陷阱",
    "confidence_score": 0.85,
    "emotional_state": "情感状态描述",
    "core_issue": "核心问题描述",
    "breakthrough_insight": "关键认知突破点",
    "recommended_prescription": "推荐的药方ID"
}}"""
        
        return prompt
    
    def _call_gemini_with_retry(self, prompt: str) -> str:
        """带重试的Gemini调用"""
        max_retries = RETRY_CONFIG["max_retries"]
        retry_delay = RETRY_CONFIG["retry_delay"]
        
        for attempt in range(max_retries):
            try:
                if DEBUG:
                    print(f"🤖 调用Gemini (尝试 {attempt + 1}/{max_retries})")
                
                response = self.model.generate_content(prompt)
                
                if response.text:
                    if DEBUG:
                        print(f"✅ Gemini响应成功")
                    return response.text
                else:
                    raise Exception("Gemini返回空响应")
                    
            except Exception as e:
                print(f"⚠️ Gemini调用失败 (尝试 {attempt + 1}): {e}")
                
                if attempt < max_retries - 1:
                    # 指数退避
                    delay = retry_delay * (2 ** attempt) if RETRY_CONFIG["exponential_backoff"] else retry_delay
                    time.sleep(delay)
                else:
                    raise e
        
        raise Exception("Gemini调用重试次数耗尽")
    
    def _parse_ai_analysis(self, response_text: str) -> Dict:
        """解析AI分析结果"""
        try:
            # 尝试提取JSON
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(0)
                return json.loads(json_text)
            else:
                # 如果没有找到JSON，返回基础解析
                return {
                    "primary_cognitive_trap": "认知偏差分析",
                    "confidence_score": 0.7,
                    "emotional_state": "需要进一步分析",
                    "core_issue": response_text[:200] + "..." if len(response_text) > 200 else response_text,
                    "breakthrough_insight": "需要深度认知转换",
                    "recommended_prescription": "P01"
                }
        except Exception as e:
            print(f"⚠️ AI分析结果解析失败: {e}")
            return {}
    
    def _combine_results(self, rule_matches: List[Dict], ai_analysis: Dict, user_input: str) -> Dict:
        """结合规则匹配和AI分析结果"""
        if not rule_matches and not ai_analysis:
            return None
        
        # 确定主要诊断结果
        if rule_matches:
            best_match = rule_matches[0]
            prescription_id = best_match["rule"].get("prescription_id", "P01")
            confidence = min(best_match["score"] / 20, 1.0)
        else:
            prescription_id = ai_analysis.get("recommended_prescription", "P01")
            confidence = ai_analysis.get("confidence_score", 0.7)
        
        # AI分析可以调整置信度
        if ai_analysis and "confidence_score" in ai_analysis:
            ai_confidence = ai_analysis["confidence_score"]
            # 结合规则匹配和AI置信度
            confidence = (confidence + ai_confidence) / 2
        
        # 加载药方信息
        prescription_info = self.get_prescription_info(prescription_id)
        
        # 生成认知突破洞察
        breakthrough = (
            ai_analysis.get("breakthrough_insight") or 
            self.generate_breakthrough_insight(best_match["rule"] if rule_matches else {}, prescription_info)
        )
        
        return {
            "primary_prescription": {
                "id": prescription_id,
                "display_name": prescription_info.get("display_name", "认知重构药方"),
                "confidence": confidence,
                "impact_score": prescription_info.get("impact_score", 5),
                "category": prescription_info.get("category", "unknown")
            },
            "matched_symptoms": self.extract_matched_symptoms(user_input, best_match["rule"] if rule_matches else {}),
            "cognitive_breakthrough": breakthrough,
            "ai_analysis": ai_analysis.get("core_issue", ""),
            "related_prescriptions": prescription_info.get("related_prescriptions", [])
        }
    
    def _fallback_diagnosis(self, user_input: str) -> Optional[Dict]:
        """回退诊断（当AI失败时）"""
        # 简单的关键词匹配作为回退
        fallback_rules = {
            "合伙人": {"prescription_id": "P20", "name": "创始人冲突认知解码器"},
            "技术": {"prescription_id": "P01", "name": "技术至上偏见解毒剂"},
            "用户": {"prescription_id": "P54", "name": "用户画像精准化剂"},
            "执行": {"prescription_id": "P14", "name": "执行力认知重构剂"}
        }
        
        for keyword, rule_info in fallback_rules.items():
            if keyword in user_input:
                return {
                    "primary_prescription": {
                        "id": rule_info["prescription_id"],
                        "display_name": rule_info["name"],
                        "confidence": 0.6,
                        "impact_score": 7,
                        "category": "fallback"
                    },
                    "matched_symptoms": [f"检测到{keyword}相关问题"],
                    "cognitive_breakthrough": "需要进一步深度分析认知模式",
                    "ai_analysis": "基于关键词的基础匹配",
                    "related_prescriptions": []
                }
        
        return None
    
    def get_prescription_info(self, prescription_id: str) -> Dict:
        """获取药方信息"""
        if prescription_id in self.prescription_cache:
            return self.prescription_cache[prescription_id]
        
        # 搜索药方文件
        for category_dir in ["01_basics", "02_advanced", "03_team"]:
            category_path = KNOWLEDGE_BASE_DIR / category_dir
            if category_path.exists():
                for file_path in category_path.glob("*.md"):
                    if file_path.stem.startswith(prescription_id.replace("P", "P")):
                        info = self.parse_prescription_metadata(file_path)
                        self.prescription_cache[prescription_id] = info
                        return info
        
        # 默认信息
        default_info = {
            "display_name": f"认知重构药方{prescription_id}",
            "impact_score": 5,
            "category": "unknown",
            "related_prescriptions": []
        }
        
        self.prescription_cache[prescription_id] = default_info
        return default_info
    
    def parse_prescription_metadata(self, file_path: Path) -> Dict:
        """解析药方元数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简单的YAML前置元数据解析
            if content.startswith('---'):
                end_yaml = content.find('---', 3)
                if end_yaml > 0:
                    yaml_content = content[3:end_yaml]
                    metadata = {}
                    for line in yaml_content.split('\n'):
                        if ':' in line and not line.strip().startswith('#'):
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip().strip('"')
                    return metadata
        except Exception as e:
            print(f"⚠️ 解析药方元数据失败 {file_path}: {e}")
        
        return {}
    
    def extract_matched_symptoms(self, user_input: str, rule: Dict) -> List[str]:
        """提取匹配的症状"""
        symptoms = []
        keywords = rule.get("keywords", {})
        
        for keyword, weight in keywords.items():
            if keyword in user_input and weight >= 4:  # 高权重关键词
                symptoms.append(f"{keyword}相关问题")
        
        return symptoms[:3]  # 最多返回3个
    
    def generate_breakthrough_insight(self, rule: Dict, prescription_info: Dict) -> str:
        """生成认知突破洞察"""
        rule_id = rule.get("rule_id", "")
        
        # 预定义的突破洞察
        insights = {
            "RULE_TF01_KEVIN_CASE_ENHANCED": "原来问题不在人，而在认知系统的兼容性",
            "RULE_PM01_TECH_BIAS_ENHANCED": "原来用户要的不是更好的技术，而是更好的体验",
            "RULE_DB01_CONFIRMATION_BIAS": "原来我在寻找支持证据，而不是验证假设",
            "RULE_TF02_EXECUTION_GAP": "原来我在用学习逃避行动的不确定性"
        }
        
        return insights.get(rule_id, "原来我一直想错了关键问题")
    
    def test_connection(self) -> bool:
        """测试Gemini连接"""
        try:
            if not self.model:
                return False
            
            test_response = self.model.generate_content("测试连接")
            return bool(test_response.text)
            
        except Exception as e:
            print(f"❌ Gemini连接测试失败: {e}")
            return False

# 全局实例
_diagnosis_engine = None

def get_diagnosis_engine():
    """获取诊断引擎单例"""
    global _diagnosis_engine
    if _diagnosis_engine is None:
        _diagnosis_engine = DiagnosisEngine()
    return _diagnosis_engine
