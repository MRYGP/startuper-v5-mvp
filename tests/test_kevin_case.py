#!/usr/bin/env python3
"""
Kevin案例专项测试
核心功能：验证系统能否正确识别合伙人冲突问题，这是产品价值的试金石
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import unittest
import json
from utils.diagnosis_engine import DiagnosisEngine
from utils.demo_case_manager import DemoCaseManager

class TestKevinCase(unittest.TestCase):
    """Kevin案例专项测试类"""
    
    def setUp(self):
        """测试初始化"""
        self.diagnosis_engine = DiagnosisEngine()
        self.demo_manager = DemoCaseManager()
        
        # Kevin案例标准输入
        self.kevin_input_variations = [
            # 变体1：原始Kevin描述
            """我和我的技术合伙人在产品方向上产生了严重分歧，我认为应该专注B端企业客户，做项目管理SaaS，但他坚持要做C端的个人时间管理App。我们为此争论了6个月，项目基本停滞。最让我困惑的是，我明明有更多的市场调研数据支持B端方向，但他就是说服不了。现在我们的关系很紧张，投资人也开始质疑我们团队的执行力。""",
            
            # 变体2：更直接的合伙人冲突描述
            """我们三个合伙人现在已经闹掰了。我负责产品，技术合伙人负责开发，运营合伙人负责市场。但是我们在很多决策上都有分歧，特别是产品方向。每次开会都是争论，没有人能说服任何人。现在已经影响到了工作效率，团队士气也很低落。我开始怀疑是不是合伙人选择有问题。""",
            
            # 变体3：股权和决策权冲突
            """我和我的合伙人在股权分配和决策权上有很大争议。我们当初没有明确的决策机制，现在遇到重大问题时经常僵持不下。他觉得技术更重要，应该有更多话语权；我觉得商业决策需要更专业的判断。这种内耗已经持续了几个月，外部投资人都开始担心我们团队的稳定性。""",
            
            # 变体4：创始人理念冲突
            """我和联合创始人的价值观和经营理念出现了根本性分歧。他更倾向于追求快速增长和融资，我更希望稳健发展和盈利。这种分歧导致我们在战略制定、资源分配、人员招聘等各个方面都难以达成一致。现在我们的合作关系已经非常紧张，甚至在考虑分手的可能性。"""
        ]
        
        # 期望结果标准
        self.expected_results = {
            "prescription_id": "P20",
            "prescription_name_keywords": ["创始人", "冲突", "解码"],
            "min_confidence": 0.85,
            "category": "team",
            "cognitive_breakthrough_keywords": ["认知系统", "兼容性", "问题不在人"]
        }
    
    def test_kevin_case_basic_recognition(self):
        """测试基本Kevin案例识别"""
        print("\n🧪 测试1：Kevin案例基本识别")
        
        result = self.diagnosis_engine.diagnose(self.kevin_input_variations[0])
        
        # 断言：必须有诊断结果
        self.assertIsNotNone(result, "Kevin案例诊断失败：无法获取诊断结果")
        
        # 断言：必须识别为P20药方
        primary = result.get('primary_prescription', {})
        prescription_id = primary.get('id', '')
        self.assertEqual(prescription_id, "P20", 
                        f"Kevin案例诊断错误：期望P20，实际得到{prescription_id}")
        
        # 断言：置信度必须足够高
        confidence = primary.get('confidence', 0)
        self.assertGreaterEqual(confidence, self.expected_results["min_confidence"],
                               f"Kevin案例置信度不足：期望>={self.expected_results['min_confidence']:.0%}，实际{confidence:.0%}")
        
        print(f"✅ 基本识别测试通过：{prescription_id} (置信度: {confidence:.1%})")
    
    def test_kevin_case_all_variations(self):
        """测试Kevin案例所有变体"""
        print("\n🧪 测试2：Kevin案例变体识别")
        
        success_count = 0
        total_count = len(self.kevin_input_variations)
        
        for i, input_text in enumerate(self.kevin_input_variations):
            print(f"\n  测试变体 {i+1}/{total_count}:")
            
            result = self.diagnosis_engine.diagnose(input_text)
            
            if result:
                primary = result.get('primary_prescription', {})
                prescription_id = primary.get('id', '')
                confidence = primary.get('confidence', 0)
                
                if prescription_id == "P20" and confidence >= self.expected_results["min_confidence"]:
                    success_count += 1
                    print(f"  ✅ 变体{i+1}识别成功：{prescription_id} ({confidence:.1%})")
                else:
                    print(f"  ❌ 变体{i+1}识别失败：{prescription_id} ({confidence:.1%})")
            else:
                print(f"  ❌ 变体{i+1}诊断失败：无结果")
        
        # 断言：至少80%的变体识别成功
        success_rate = success_count / total_count
        self.assertGreaterEqual(success_rate, 0.8,
                               f"Kevin案例变体识别成功率不足：{success_rate:.1%} < 80%")
        
        print(f"\n✅ 变体识别测试通过：{success_count}/{total_count} ({success_rate:.1%})")
    
    def test_kevin_case_not_product_validation(self):
        """测试Kevin案例不会被误诊为产品验证问题"""
        print("\n🧪 测试3：避免误诊为产品验证问题")
        
        result = self.diagnosis_engine.diagnose(self.kevin_input_variations[0])
        
        # 断言：不应该是产品相关的药方ID（P01-P19通常是产品相关）
        primary = result.get('primary_prescription', {})
        prescription_id = primary.get('id', '')
        
        # 产品验证相关的药方ID列表
        product_validation_ids = ["P01", "P02", "P03", "P04", "P18", "P19"]
        
        self.assertNotIn(prescription_id, product_validation_ids,
                        f"Kevin案例被误诊为产品问题：{prescription_id}")
        
        print(f"✅ 避免误诊测试通过：正确识别为{prescription_id}而非产品验证问题")
    
    def test_kevin_case_cognitive_breakthrough(self):
        """测试Kevin案例认知突破点"""
        print("\n🧪 测试4：认知突破点质量")
        
        result = self.diagnosis_engine.diagnose(self.kevin_input_variations[0])
        
        cognitive_breakthrough = result.get('cognitive_breakthrough', '')
        self.assertIsNotNone(cognitive_breakthrough, "缺少认知突破点")
        self.assertGreater(len(cognitive_breakthrough), 10, "认知突破点过于简短")
        
        # 检查是否包含关键概念
        breakthrough_keywords = self.expected_results["cognitive_breakthrough_keywords"]
        contains_key_concept = any(keyword in cognitive_breakthrough for keyword in breakthrough_keywords)
        
        self.assertTrue(contains_key_concept,
                       f"认知突破点缺乏核心概念：{cognitive_breakthrough}")
        
        print(f"✅ 认知突破点测试通过：{cognitive_breakthrough}")
    
    def test_demo_case_kevin_special(self):
        """测试Demo案例中的Kevin特殊标记"""
        print("\n🧪 测试5：Demo案例Kevin特殊标记")
        
        kevin_case = self.demo_manager.get_kevin_case()
        
        self.assertIsNotNone(kevin_case, "未找到Kevin专用Demo案例")
        
        # 检查特殊标记
        meta = kevin_case.get('case_meta', {})
        self.assertTrue(meta.get('kevin_case_solution', False),
                       "Kevin Demo案例缺少kevin_case_solution标记")
        
        # 检查案例内容质量
        questions = kevin_case.get('six_questions_answers', {})
        self.assertGreater(len(questions), 0, "Kevin Demo案例缺少问题回答")
        
        print("✅ Kevin Demo案例特殊标记测试通过")
    
    def test_diagnosis_rules_kevin_specific(self):
        """测试诊断规则中的Kevin特定规则"""
        print("\n🧪 测试6：诊断规则Kevin特定配置")
        
        rules = self.diagnosis_engine.rules
        
        # 查找Kevin特定规则
        kevin_rule_found = False
        for category in rules.get("problem_categories", []):
            for rule in category.get("rules", []):
                if "KEVIN" in rule.get("rule_id", "").upper():
                    kevin_rule_found = True
                    
                    # 检查关键词配置
                    keywords = rule.get("keywords", {})
                    required_keywords = ["合伙人", "冲突", "分歧"]
                    
                    for keyword in required_keywords:
                        self.assertIn(keyword, keywords,
                                     f"Kevin规则缺少关键词：{keyword}")
                        self.assertGreaterEqual(keywords[keyword], 4,
                                              f"Kevin规则关键词权重不足：{keyword}={keywords[keyword]}")
                    
                    # 检查阈值设置
                    threshold = rule.get("threshold", 0)
                    self.assertGreaterEqual(threshold, 8,
                                          f"Kevin规则阈值过低：{threshold}")
                    
                    print(f"✅ 找到Kevin特定规则：{rule.get('rule_id')}")
                    break
        
        self.assertTrue(kevin_rule_found, "未找到Kevin特定诊断规则")
    
    def test_kevin_case_end_to_end(self):
        """端到端Kevin案例测试"""
        print("\n🧪 测试7：Kevin案例端到端验证")
        
        # 模拟完整用户流程
        user_input = self.kevin_input_variations[0]
        
        # 1. 诊断阶段
        result = self.diagnosis_engine.diagnose(user_input)
        self.assertIsNotNone(result, "端到端测试失败：诊断阶段")
        
        # 2. 验证核心指标
        primary = result.get('primary_prescription', {})
        
        prescription_id = primary.get('id')
        confidence = primary.get('confidence', 0)
        impact_score = primary.get('impact_score', 0)
        
        # 3. 全面验证
        self.assertEqual(prescription_id, "P20", "药方ID错误")
        self.assertGreaterEqual(confidence, 0.85, f"置信度不足：{confidence:.1%}")
        self.assertGreaterEqual(impact_score, 8, f"影响评级过低：{impact_score}")
        
        # 4. 验证相关药方推荐
        related = result.get('related_prescriptions', [])
        self.assertGreater(len(related), 0, "缺少相关药方推荐")
        
        print(f"✅ 端到端测试通过：")
        print(f"   药方ID: {prescription_id}")
        print(f"   置信度: {confidence:.1%}")
        print(f"   影响评级: {impact_score}/10")
        print(f"   相关药方: {len(related)}个")

def run_kevin_tests():
    """运行Kevin案例专项测试"""
    print("🔥 开始Kevin案例专项测试 - 产品价值验证的试金石")
    print("=" * 60)
    
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 添加所有Kevin测试
    test_methods = [
        'test_kevin_case_basic_recognition',
        'test_kevin_case_all_variations', 
        'test_kevin_case_not_product_validation',
        'test_kevin_case_cognitive_breakthrough',
        'test_demo_case_kevin_special',
        'test_diagnosis_rules_kevin_specific',
        'test_kevin_case_end_to_end'
    ]
    
    for method in test_methods:
        suite.addTest(TestKevinCase(method))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出总结
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 Kevin案例测试全部通过！产品核心价值得到验证！")
        print("✅ 系统已具备处理合伙人冲突问题的能力")
        print("✅ 可以正确区分团队问题和产品问题")
        print("✅ 认知突破点设计有效")
        print("✅ 产品已Ready for Prime Time！")
    else:
        print("❌ Kevin案例测试失败！需要立即修复！")
        print(f"失败测试数: {len(result.failures)}")
        print(f"错误测试数: {len(result.errors)}")
        print("🚨 这直接影响产品的核心商业价值！")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_kevin_tests()
    sys.exit(0 if success else 1)
