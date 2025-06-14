#!/usr/bin/env python3
"""
诊断准确性测试
核心功能：验证整个诊断系统对各种创业认知陷阱的识别准确性
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import unittest
import json
from typing import Dict, List, Tuple
from utils.diagnosis_engine import DiagnosisEngine
from utils.demo_case_manager import DemoCaseManager

class TestDiagnosisAccuracy(unittest.TestCase):
    """诊断准确性测试类"""
    
    def setUp(self):
        """测试初始化"""
        self.diagnosis_engine = DiagnosisEngine()
        self.demo_manager = DemoCaseManager()
        
        # 标准测试案例集合
        self.test_cases = [
            # 技术至上偏见案例
            {
                "input": """我在字节做了3年推荐算法，技术很扎实。去年辞职创业，花了8个月开发了一套AI简历筛选系统。我们的算法比市面上的产品准确率高30%，但是推向市场后，几乎没有HR愿意付费使用。有些HR告诉我，他们觉得我们的系统'太复杂了'，他们更喜欢用简单的关键词搜索。""",
                "expected_prescription": "P01",
                "expected_category": "product",
                "test_name": "技术至上偏见"
            },
            
            # 确认偏见案例
            {
                "input": """我做了非常详细的市场调研，找了50个目标用户做深度访谈，95%的人都说'很需要这样的产品'，'一定会买'。我还分析了小红书上10万条相关笔记，所有数据都支持我的判断。但产品上线后，真实的销售数据让我崩溃：首月销售额只有预期的1/10，复购率不到15%。""",
                "expected_prescription": "P02",
                "expected_category": "decision",
                "test_name": "确认偏见"
            },
            
            # 执行力认知gap案例
            {
                "input": """我制定了很详细的计划：每周发布2篇深度文章，每月做1次免费直播，半年后推出付费课程。我还学了很多内容创业的方法论，买了十几门相关课程。但是两年多下来，我的执行情况惨不忍睹：文章断断续续发了不到30篇，直播只做了3次，付费课程到现在还没有推出。我明明知道坚持的重要性，也知道具体该怎么做，但就是做不到。""",
                "expected_prescription": "P14",
                "expected_category": "execution", 
                "test_name": "执行力认知gap"
            },
            
            # 合伙人冲突案例（Kevin案例变体）
            {
                "input": """我和两个合伙人一起做企业协作SaaS，我负责产品和融资，技术合伙人负责研发，运营合伙人负责市场。我们三个都是大厂出来的，履历很光鲜。但是从去年下半年开始，我们三个在很多关键决策上开始产生分歧。最终的结果是：我们在这些争议上消耗了大量时间和精力，产品既没有做到技术领先，也没有抢到市场先机。""",
                "expected_prescription": "P20",
                "expected_category": "team",
                "test_name": "合伙人冲突"
            },
            
            # 过度自信案例
            {
                "input": """我对这个项目非常有信心，我们的商业模式很清晰，团队执行力很强，市场需求也很明确。我预计3个月内就能完成产品开发，6个月内获得第一批付费用户，一年内实现盈亏平衡。但实际情况是，产品开发就花了8个月，用户获取比预期困难得多，现在已经一年半了还在烧钱。""",
                "expected_prescription": "P03",
                "expected_category": "decision",
                "test_name": "过度自信"
            }
        ]
        
        # 诊断质量标准
        self.quality_standards = {
            "min_confidence": 0.6,      # 最低置信度
            "target_accuracy": 0.8,     # 目标准确率
            "min_impact_score": 5       # 最低影响评级
        }
    
    def test_individual_case_accuracy(self):
        """测试单个案例诊断准确性"""
        print("\n🧪 测试1：单个案例诊断准确性")
        
        success_count = 0
        total_count = len(self.test_cases)
        
        for i, test_case in enumerate(self.test_cases):
            print(f"\n  测试案例 {i+1}/{total_count}: {test_case['test_name']}")
            
            result = self.diagnosis_engine.diagnose(test_case['input'])
            
            if result:
                primary = result.get('primary_prescription', {})
                prescription_id = primary.get('id', '')
                confidence = primary.get('confidence', 0)
                
                # 验证药方ID是否正确
                if prescription_id == test_case['expected_prescription']:
                    if confidence >= self.quality_standards['min_confidence']:
                        success_count += 1
                        print(f"  ✅ {test_case['test_name']}识别成功：{prescription_id} ({confidence:.1%})")
                    else:
                        print(f"  ⚠️ {test_case['test_name']}识别正确但置信度不足：{prescription_id} ({confidence:.1%})")
                else:
                    print(f"  ❌ {test_case['test_name']}识别错误：期望{test_case['expected_prescription']}，实际{prescription_id}")
            else:
                print(f"  ❌ {test_case['test_name']}诊断失败：无结果")
        
        accuracy = success_count / total_count
        print(f"\n📊 单案例准确率：{success_count}/{total_count} ({accuracy:.1%})")
        
        # 断言：准确率必须达到目标标准
        self.assertGreaterEqual(accuracy, self.quality_standards['target_accuracy'],
                               f"诊断准确率不达标：{accuracy:.1%} < {self.quality_standards['target_accuracy']:.1%}")
    
    def test_demo_cases_consistency(self):
        """测试Demo案例与诊断引擎的一致性"""
        print("\n🧪 测试2：Demo案例诊断一致性")
        
        all_cases = self.demo_manager.get_all_cases()
        consistency_count = 0
        total_demo_cases = 0
        
        for case_id, case_data in all_cases.items():
            # 获取案例的问题描述
            questions = case_data.get('six_questions_answers', {})
            if not questions:
                continue
                
            total_demo_cases += 1
            
            # 构建用户输入（使用第一个问题的回答）
            first_question = questions.get('question_1', {})
            user_input = first_question.get('answer', '')
            
            if len(user_input) < 50:  # 输入太短，跳过
                continue
            
            # 诊断
            result = self.diagnosis_engine.diagnose(user_input)
            
            if result:
                primary = result.get('primary_prescription', {})
                diagnosed_id = primary.get('id', '')
                
                # 获取期望的诊断结果
                expected_diagnosis = case_data.get('expected_diagnosis', {})
                expected_prescription = expected_diagnosis.get('primary_trap', '')
                
                # 简单的ID匹配（可能需要更复杂的映射逻辑）
                if self._match_prescription_ids(diagnosed_id, expected_prescription):
                    consistency_count += 1
                    print(f"  ✅ {case_id}诊断一致：{diagnosed_id}")
                else:
                    print(f"  ❌ {case_id}诊断不一致：期望{expected_prescription}，实际{diagnosed_id}")
        
        if total_demo_cases > 0:
            consistency_rate = consistency_count / total_demo_cases
            print(f"\n📊 Demo案例一致性：{consistency_count}/{total_demo_cases} ({consistency_rate:.1%})")
            
            # 断言：一致性应该达到合理水平
            self.assertGreaterEqual(consistency_rate, 0.6,
                                   f"Demo案例一致性过低：{consistency_rate:.1%}")
        else:
            print("  ⚠️ 未找到可测试的Demo案例")
    
    def test_confidence_distribution(self):
        """测试置信度分布合理性"""
        print("\n🧪 测试3：置信度分布合理性")
        
        confidences = []
        
        for test_case in self.test_cases:
            result = self.diagnosis_engine.diagnose(test_case['input'])
            if result:
                primary = result.get('primary_prescription', {})
                confidence = primary.get('confidence', 0)
                confidences.append(confidence)
        
        if confidences:
            avg_confidence = sum(confidences) / len(confidences)
            min_confidence = min(confidences)
            max_confidence = max(confidences)
            
            print(f"  📊 置信度统计：")
            print(f"     平均: {avg_confidence:.1%}")
            print(f"     最小: {min_confidence:.1%}")
            print(f"     最大: {max_confidence:.1%}")
            
            # 断言：置信度分布应该合理
            self.assertGreaterEqual(avg_confidence, 0.5, f"平均置信度过低：{avg_confidence:.1%}")
            self.assertGreaterEqual(min_confidence, 0.3, f"最低置信度过低：{min_confidence:.1%}")
            self.assertLessEqual(max_confidence, 1.0, f"最高置信度异常：{max_confidence:.1%}")
            
            print("  ✅ 置信度分布合理")
        else:
            self.fail("无法获取置信度数据")
    
    def test_edge_cases_handling(self):
        """测试边缘案例处理"""
        print("\n🧪 测试4：边缘案例处理")
        
        edge_cases = [
            # 空输入
            {"input": "", "expected_behavior": "reject"},
            # 过短输入
            {"input": "我有问题", "expected_behavior": "reject"},
            # 过长输入
            {"input": "很长的输入" * 200, "expected_behavior": "process"},
            # 无关内容
            {"input": "今天天气很好，我去公园散步了。看到很多花都开了，心情特别愉快。晚上和朋友一起吃了火锅，聊了很久关于旅行的话题。", "expected_behavior": "low_confidence"},
            # 混合多个问题
            {"input": "我的技术很强但是用户不买账，同时我和合伙人也有分歧，还有就是我总是拖延执行不了计划。", "expected_behavior": "process"}
        ]
        
        for i, edge_case in enumerate(edge_cases):
            print(f"  边缘案例 {i+1}: {edge_case['expected_behavior']}")
            
            result = self.diagnosis_engine.diagnose(edge_case['input'])
            
            if edge_case['expected_behavior'] == 'reject':
                self.assertIsNone(result, f"应该拒绝但返回了结果：{edge_case['input'][:20]}...")
                print("    ✅ 正确拒绝")
            elif edge_case['expected_behavior'] == 'process':
                self.assertIsNotNone(result, f"应该处理但返回None：{edge_case['input'][:20]}...")
                print("    ✅ 正常处理")
            elif edge_case['expected_behavior'] == 'low_confidence':
                if result:
                    confidence = result.get('primary_prescription', {}).get('confidence', 0)
                    self.assertLess(confidence, 0.7, f"无关内容置信度过高：{confidence:.1%}")
                    print(f"    ✅ 低置信度处理：{confidence:.1%}")
                else:
                    print("    ✅ 正确拒绝无关内容")
    
    def test_keyword_matching_robustness(self):
        """测试关键词匹配的鲁棒性"""
        print("\n🧪 测试5：关键词匹配鲁棒性")
        
        # 同一个问题的不同表达方式
        variations = [
            # 合伙人冲突的不同表达
            {
                "variations": [
                    "我和合伙人有分歧",
                    "我们创始人之间有矛盾",
                    "团队内部产生了冲突",
                    "合伙人关系出现问题"
                ],
                "expected_category": "team"
            },
            # 技术问题的不同表达
            {
                "variations": [
                    "技术很好但是没人用",
                    "产品功能强大但用户不买账",
                    "我们的算法很先进但市场反应冷淡",
                    "技术领先但是商业化困难"
                ],
                "expected_category": "product"
            }
        ]
        
        consistent_groups = 0
        total_groups = len(variations)
        
        for group in variations:
            diagnosed_categories = []
            
            for variation in group['variations']:
                result = self.diagnosis_engine.diagnose(variation)
                if result:
                    primary = result.get('primary_prescription', {})
                    prescription_id = primary.get('id', '')
                    category = self._get_prescription_category(prescription_id)
                    diagnosed_categories.append(category)
            
            # 检查同一组变体是否被归为相似类别
            if len(set(diagnosed_categories)) <= 2:  # 允许一定的变异
                consistent_groups += 1
                print(f"  ✅ 变体组一致性良好：{group['expected_category']}")
            else:
                print(f"  ⚠️ 变体组一致性较差：{diagnosed_categories}")
        
        consistency_rate = consistent_groups / total_groups
        print(f"\n📊 关键词匹配一致性：{consistent_groups}/{total_groups} ({consistency_rate:.1%})")
        
        self.assertGreaterEqual(consistency_rate, 0.7,
                               f"关键词匹配一致性不足：{consistency_rate:.1%}")
    
    def _match_prescription_ids(self, diagnosed_id: str, expected_description: str) -> bool:
        """匹配药方ID和描述（简化版本）"""
        # 这里需要更复杂的映射逻辑，暂时使用简单匹配
        mapping = {
            "技术至上偏见": "P01",
            "确认偏见": "P02", 
            "团队认知偏差": "P20",
            "执行力认知": "P14"
        }
        
        for description, prescription_id in mapping.items():
            if description in expected_description and diagnosed_id == prescription_id:
                return True
        
        return False
    
    def _get_prescription_category(self, prescription_id: str) -> str:
        """根据药方ID获取类别（简化版本）"""
        if prescription_id in ["P01", "P02", "P03", "P04", "P18", "P19"]:
            return "product"
        elif prescription_id in ["P20", "P56", "P57"]:
            return "team"
        elif prescription_id in ["P14"]:
            return "execution"
        else:
            return "advanced"

def run_diagnosis_accuracy_tests():
    """运行诊断准确性测试"""
    print("🎯 开始诊断准确性测试 - 系统整体质量验证")
    print("=" * 60)
    
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 添加所有准确性测试
    test_methods = [
        'test_individual_case_accuracy',
        'test_demo_cases_consistency',
        'test_confidence_distribution',
        'test_edge_cases_handling',
        'test_keyword_matching_robustness'
    ]
    
    for method in test_methods:
        suite.addTest(TestDiagnosisAccuracy(method))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出总结
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 诊断准确性测试全部通过！")
        print("✅ 系统诊断能力达到商业化标准")
        print("✅ 各类认知陷阱识别准确")
        print("✅ 置信度分布合理")
        print("✅ 边缘案例处理良好")
        print("✅ 关键词匹配鲁棒性良好")
    else:
        print("❌ 诊断准确性测试存在问题！")
        print(f"失败测试数: {len(result.failures)}")
        print(f"错误测试数: {len(result.errors)}")
        print("🚨 需要优化诊断算法和规则配置！")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_diagnosis_accuracy_tests()
    sys.exit(0 if success else 1)
