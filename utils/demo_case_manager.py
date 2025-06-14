"""
Demo案例管理器 - 管理和加载Demo案例
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
import streamlit as st

class DemoCaseManager:
    def __init__(self):
        self.cases_cache = {}
        self.base_dir = Path(__file__).parent.parent
        self.demo_cases_dir = self.base_dir / "demo_cases"
        self.load_all_cases()
    
    def load_all_cases(self):
        """加载所有Demo案例"""
        try:
            if self.demo_cases_dir.exists():
                for file_path in self.demo_cases_dir.glob("case_*.json"):
                    case_id = file_path.stem
                    case_data = self.load_case_file(file_path)
                    if case_data:
                        self.cases_cache[case_id] = case_data
            
            print(f"加载了 {len(self.cases_cache)} 个Demo案例")
            
            # 如果没有加载到案例，创建默认案例
            if not self.cases_cache:
                self.create_default_cases()
                
        except Exception as e:
            print(f"加载Demo案例时出错: {e}")
            self.create_default_cases()
    
    def create_default_cases(self):
        """创建默认案例（用于测试）"""
        self.cases_cache = {
            "case_01_tech_supremacy": {
                "case_meta": {
                    "case_id": "case_01_tech_supremacy",
                    "case_name": "技术至上偏见陷阱",
                    "protagonist": "张铭",
                    "target_trap": "技术至上偏见",
                    "expected_prescription": "P01",
                    "difficulty_level": "medium",
                    "cognitive_impact_score": 9,
                    "user_group": "90%技术背景创业者"
                },
                "character_profile": {
                    "name": "张铭",
                    "age": 29,
                    "background": "前字节跳动算法工程师",
                    "current_venture": "智能简历筛选系统",
                    "personality": "技术信仰坚定，对产品技术优势盲目自信",
                    "pain_point": "技术领先但市场不买账"
                },
                "problem_summary": "算法准确率比竞品高30%，但HR觉得'太复杂了'，只有3家愿意试用",
                "cognitive_breakthrough": "原来我一直在解决我认为重要的问题，而不是用户真正需要解决的问题"
            },
            
            "case_02_team_conflict": {
                "case_meta": {
                    "case_id": "case_02_team_conflict", 
                    "case_name": "团队合伙人冲突认知陷阱",
                    "protagonist": "李华",
                    "target_trap": "团队认知偏差：镜子陷阱",
                    "expected_prescription": "P20",
                    "difficulty_level": "high",
                    "cognitive_impact_score": 10,
                    "kevin_case_solution": True,
                    "user_group": "有合伙人的创业团队"
                },
                "character_profile": {
                    "name": "李华",
                    "age": 34,
                    "background": "连续创业者，第二次创业",
                    "current_venture": "企业级SaaS协作平台",
                    "personality": "追求完美团队，相信'强强联合'逻辑",
                    "pain_point": "优秀的人组合在一起反而失败了"
                },
                "problem_summary": "三个大厂出身的合伙人，在产品方向上争论8个月无结果，最终团队解散",
                "cognitive_breakthrough": "原来我一直追求人员互补，而忽视了认知一致性"
            },
            
            "case_03_confirmation_bias": {
                "case_meta": {
                    "case_id": "case_03_confirmation_bias",
                    "case_name": "确认偏见陷阱", 
                    "protagonist": "陈佳",
                    "target_trap": "确认偏见：选择性信息收集",
                    "expected_prescription": "P02",
                    "difficulty_level": "high",
                    "cognitive_impact_score": 9,
                    "user_group": "过度相信自己判断的创业者"
                },
                "character_profile": {
                    "name": "陈佳",
                    "age": 31,
                    "background": "前麦肯锡咨询顾问",
                    "current_venture": "主打'健康轻食'的预制菜品牌",
                    "personality": "数据驱动决策，坚信专业分析能力",
                    "pain_point": "详细调研支持判断，但市场表现完全相反"
                },
                "problem_summary": "95%用户说'一定会买'，实际销售额崩盘，30%退货率",
                "cognitive_breakthrough": "原来我在寻找支持证据，而不是在验证假设"
            },
            
            "case_04_execution_gap": {
                "case_meta": {
                    "case_id": "case_04_execution_gap",
                    "case_name": "执行力认知gap陷阱",
                    "protagonist": "王磊", 
                    "target_trap": "知行分离：行动逃避症",
                    "expected_prescription": "P14",
                    "difficulty_level": "medium",
                    "cognitive_impact_score": 8,
                    "user_group": "知道很多但做不到的创业者"
                },
                "character_profile": {
                    "name": "王磊",
                    "age": 30,
                    "background": "前产品经理",
                    "current_venture": "职场技能培训课程平台",
                    "personality": "学习能力强，喜欢研究方法论，但执行力差",
                    "pain_point": "明明知道该怎么做，但总是做不到"
                },
                "problem_summary": "买了几十本书和课程，制定了详细计划，但两年只发了30篇文章",
                "cognitive_breakthrough": "原来我一直在用学习来逃避行动的不确定性和可能的失败"
            }
        }
    
    def load_case_file(self, file_path: Path) -> Optional[Dict]:
        """加载案例文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载案例文件错误 {file_path}: {e}")
            return None
    
    def get_case(self, case_id: str) -> Optional[Dict]:
        """获取特定案例"""
        return self.cases_cache.get(case_id)
    
    def get_all_cases(self) -> Dict:
        """获取所有案例"""
        return self.cases_cache
    
    def get_kevin_case(self) -> Optional[Dict]:
        """获取Kevin专用案例"""
        for case_id, case_data in self.cases_cache.items():
            if case_data.get('case_meta', {}).get('kevin_case_solution'):
                return {
                    'case_id': case_id,
                    'case_data': case_data
                }
        return None
    
    def get_case_by_trap_type(self, trap_type: str) -> List[Dict]:
        """根据陷阱类型获取案例"""
        results = []
        trap_type_lower = trap_type.lower()
        
        for case_id, case_data in self.cases_cache.items():
            target_trap = case_data.get('case_meta', {}).get('target_trap', '').lower()
            if trap_type_lower in target_trap:
                results.append({
                    'case_id': case_id,
                    'case_data': case_data
                })
        return results
    
    def get_cases_by_difficulty(self, difficulty: str) -> List[Dict]:
        """根据难度获取案例"""
        results = []
        for case_id, case_data in self.cases_cache.items():
            case_difficulty = case_data.get('case_meta', {}).get('difficulty_level', '')
            if case_difficulty == difficulty:
                results.append({
                    'case_id': case_id,
                    'case_data': case_data
                })
        return results
    
    def search_cases(self, query: str) -> List[Dict]:
        """搜索案例"""
        if not query:
            return []
        
        results = []
        query_lower = query.lower()
        
        for case_id, case_data in self.cases_cache.items():
            score = 0
            meta = case_data.get('case_meta', {})
            profile = case_data.get('character_profile', {})
            
            # 搜索案例名称
            if query_lower in meta.get('case_name', '').lower():
                score += 10
            
            # 搜索主角名称
            if query_lower in meta.get('protagonist', '').lower():
                score += 8
            
            # 搜索目标陷阱
            if query_lower in meta.get('target_trap', '').lower():
                score += 6
            
            # 搜索背景信息
            if query_lower in profile.get('background', '').lower():
                score += 4
            
            # 搜索痛点
            if query_lower in profile.get('pain_point', '').lower():
                score += 4
            
            # 搜索问题摘要
            if query_lower in case_data.get('problem_summary', '').lower():
                score += 3
            
            if score > 0:
                results.append({
                    'case_id': case_id,
                    'case_data': case_data,
                    'score': score
                })
        
        # 按相关性排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results
    
    def get_case_stats(self) -> Dict:
        """获取案例统计信息"""
        if not self.cases_cache:
            return {"total": 0, "by_difficulty": {}, "by_impact": {}}
        
        stats = {
            "total": len(self.cases_cache),
            "by_difficulty": {},
            "by_impact": {},
            "kevin_cases": 0
        }
        
        for case_data in self.cases_cache.values():
            meta = case_data.get('case_meta', {})
            
            # 按难度统计
            difficulty = meta.get('difficulty_level', '未知')
            stats["by_difficulty"][difficulty] = stats["by_difficulty"].get(difficulty, 0) + 1
            
            # 按认知冲击统计
            impact = meta.get('cognitive_impact_score', 5)
            impact_range = f"{impact//2*2}-{impact//2*2+1}分" if impact < 10 else "10分"
            stats["by_impact"][impact_range] = stats["by_impact"].get(impact_range, 0) + 1
            
            # Kevin案例统计
            if meta.get('kevin_case_solution'):
                stats["kevin_cases"] += 1
        
        return stats
    
    def validate_case_data(self, case_data: Dict) -> List[str]:
        """验证案例数据完整性"""
        errors = []
        
        # 检查必需字段
        required_fields = {
            'case_meta': ['case_id', 'case_name', 'protagonist', 'target_trap'],
            'character_profile': ['name', 'background', 'pain_point']
        }
        
        for section, fields in required_fields.items():
            if section not in case_data:
                errors.append(f"缺少 {section} 部分")
                continue
            
            for field in fields:
                if field not in case_data[section]:
                    errors.append(f"{section} 中缺少 {field} 字段")
        
        # 检查认知冲击分数
        impact_score = case_data.get('case_meta', {}).get('cognitive_impact_score')
        if impact_score is not None:
            if not isinstance(impact_score, int) or impact_score < 1 or impact_score > 10:
                errors.append("cognitive_impact_score 必须是1-10的整数")
        
        return errors
    
    def get_random_case(self, exclude_case_ids: List[str] = None) -> Optional[Dict]:
        """获取随机案例"""
        import random
        
        available_cases = {}
        for case_id, case_data in self.cases_cache.items():
            if not exclude_case_ids or case_id not in exclude_case_ids:
                available_cases[case_id] = case_data
        
        if not available_cases:
            return None
        
        random_case_id = random.choice(list(available_cases.keys()))
        return {
            'case_id': random_case_id,
            'case_data': available_cases[random_case_id]
        }
