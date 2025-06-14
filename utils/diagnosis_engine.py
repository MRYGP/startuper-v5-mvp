"""
诊断引擎 - 核心诊断逻辑
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from config import DIAGNOSIS_RULES_PATH, KNOWLEDGE_BASE_DIR

class DiagnosisEngine:
    def __init__(self):
        self.rules = self.load_diagnosis_rules()
        self.prescription_cache = {}
    
    def load_diagnosis_rules(self) -> Dict:
        """加载诊断规则"""
        try:
            with open(DIAGNOSIS_RULES_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"problem_categories": []}
    
    def diagnose(self, user_input: str) -> Optional[Dict]:
        """执行诊断"""
        if not user_input or len(user_input) < 20:
            return None
        
        # 计算匹配分数
        matches = []
        
        for category in self.rules.get("problem_categories", []):
            for rule in category.get("rules", []):
                score = self.calculate_rule_score(user_input, rule)
                if score >= rule.get("threshold", 8):
                    matches.append({
                        "rule": rule,
                        "score": score,
                        "category": category.get("category_name", "")
                    })
        
        # 按得分排序
        matches.sort(key=lambda x: x["score"], reverse=True)
        
        if matches:
            best_match = matches[0]
            return self.format_diagnosis_result(best_match, user_input)
        
        return None
    
    def calculate_rule_score(self, user_input: str, rule: Dict) -> float:
        """计算规则匹配分数"""
        keywords = rule.get("keywords", {})
        total_score = 0
        
        for keyword, weight in keywords.items():
            # 简单的关键词匹配（可以后续优化为更智能的匹配）
            if keyword in user_input:
                total_score += weight
        
        # Kevin案例特殊处理
        if rule.get("rule_id") == "RULE_TF01_KEVIN_CASE":
            kevin_keywords = ["合伙人", "技术合伙人", "产品方向", "分歧", "争论"]
            kevin_matches = sum(1 for kw in kevin_keywords if kw in user_input)
            if kevin_matches >= 3:
                total_score *= 1.5  # Kevin案例加权
        
        return total_score
    
    def format_diagnosis_result(self, match: Dict, user_input: str) -> Dict:
        """格式化诊断结果"""
        rule = match["rule"]
        prescription_id = rule.get("prescription_id", "")
        
        # 加载对应的药方信息
        prescription_info = self.get_prescription_info(prescription_id)
        
        return {
            "primary_prescription": {
                "id": prescription_id,
                "display_name": prescription_info.get("display_name", "未知药方"),
                "confidence": min(match["score"] / 20, 1.0),  # 标准化为0-1
                "impact_score": prescription_info.get("impact_score", 5),
                "category": prescription_info.get("category", "unknown")
            },
            "matched_symptoms": self.extract_matched_symptoms(user_input, rule),
            "cognitive_breakthrough": self.generate_breakthrough_insight(rule, prescription_info),
            "related_prescriptions": prescription_info.get("related_prescriptions", [])
        }
    
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
        
        return {"display_name": f"药方{prescription_id}", "impact_score": 5}
    
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
                    # 这里应该用yaml库解析，简化版本
                    metadata = {}
                    for line in yaml_content.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip().strip('"')
                    return metadata
        except Exception:
            pass
        
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
            "RULE_TF01_KEVIN_CASE": "原来问题不在人，而在认知系统的兼容性",
            "RULE_PM01_TECH_BIAS": "原来用户要的不是更好的技术，而是更好的体验",
            "RULE_DB01_CONFIRMATION_BIAS": "原来我在寻找支持证据，而不是验证假设"
        }
        
        return insights.get(rule_id, "原来我一直想错了关键问题")
